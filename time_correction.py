import tkinter as tk
import tkinter.ttk
import tkinter.messagebox
import datetime
import time
import threading
import typing


def get_time_str(correction:int=0,is_12_hrs:bool=False) -> str:
    if is_12_hrs:
        return datetime.datetime.fromtimestamp(time.time() + correction).strftime('%I:%M:%S %p')
    else:
        return datetime.datetime.fromtimestamp(time.time()+correction).strftime('%H:%M:%S')

def ask_time_correction(master:tk.Tk|tk.Toplevel,old_correction:int|None=None,use_12_hrs:bool=True):
    window_is_open = True
    time_correction=old_correction
    use_12_hour_clock = tk.BooleanVar(value=use_12_hrs)
    add_or_sub = tk.IntVar(master,value=1)

    def set_correction(num:str|int,add_sub:int=1,mode:typing.Literal['add','set']='set') -> None:
        nonlocal time_correction
        try:
            num = int(num)
            if num< -86400 or num> 86400:
                raise ValueError
        except ValueError:
            tkinter.messagebox.showwarning('错误的值','请输入一个整数作为时间校正值，保证数值不过大（小于等于 86400 ）、不小于零')
            return
        if mode=='add':
            time_correction += num*add_sub
        else:
            time_correction = num
        if abs(time_correction)>86400:
            tkinter.messagebox.showwarning('错误的值','时间校正值本身的绝对值不应超过86400')
            if time_correction<0:
                time_correction = -86400
            elif time_correction>0:
                time_correction = 86400
    w=tk.Toplevel(master)
    w.title('校准时间')
    w.config(padx=10, pady=10)
    w.transient(master)
    w.resizable(True,False)
    w.grab_set()
    main_time_frame = tkinter.ttk.Labelframe(w, text="时间")
    system_time_frame = tkinter.ttk.Labelframe(main_time_frame, text="系统时间")
    time_with_old_correction_frame = tkinter.ttk.Labelframe(main_time_frame, text="使用旧校正值的时间")
    time_with_new_correction_frame = tkinter.ttk.Labelframe(main_time_frame, text="使用新校正值的时间")
    system_time_frame.pack(fill='x',padx=15,pady=5)
    time_with_old_correction_frame.pack(fill='x',padx=15,pady=5)
    time_with_new_correction_frame.pack(fill='x',padx=15,pady=5)
    tk.Checkbutton(main_time_frame,text='使用12小时制',variable=use_12_hour_clock,onvalue=True,offvalue=False).pack(fill='x')
    main_time_frame.pack(fill='both',padx=15,pady=5)
    correction_label = tk.Label(w,text='当前校正值：'+str(time_correction)+' 秒')
    correction_label.pack(fill='x',padx=15,pady=5)

    system_time_label = tk.Label(system_time_frame,text='system_time',font=('Consolas',24))
    system_time_label.pack(fill='x')
    old_time_label = tk.Label(time_with_old_correction_frame,text='old_time',font=('Consolas',24))
    old_time_label.pack(fill='x')
    new_time_label = tk.Label(time_with_new_correction_frame,text='new_time',font=('Consolas',24,'bold'))
    new_time_label.pack(fill='x')

    change_correction_frame = tk.ttk.Labelframe(w,text='更改校正值')
    tk.Checkbutton(change_correction_frame,text='减小校正值',variable=add_or_sub,onvalue=-1,offvalue=1).pack(fill='x',expand=False,padx=5)
    entry_frame = tkinter.ttk.Labelframe(change_correction_frame,text='直接更改 输入秒数')
    entry = tk.ttk.Entry(entry_frame)
    entry.pack(side='left',fill='x',padx=5,pady=5,expand=True)
    tk.Button(entry_frame,text='设为校正值',command=lambda:set_correction(entry.get())).pack(side='right',fill='y',expand=False,padx=3)
    tk.Button(entry_frame,text='加入校正值',command=lambda:set_correction(entry.get(),add_or_sub.get(),'add')).pack(side='right',fill='y',expand=False,padx=3)
    tk.Button(entry_frame,text='归零校正值',command=lambda:set_correction(0)).pack(side='right',fill='y',expand=False,padx=3)
    entry_frame.pack(fill='x',padx=5,pady=5)
    second_frame = tk.ttk.Labelframe(change_correction_frame,text='秒控制')
    tk.Button(second_frame,text='1s',command=lambda:set_correction(1,add_or_sub.get(),'add')).pack(side='left',fill='y',expand=False,padx=5)
    tk.Button(second_frame, text='10s', command=lambda:set_correction(10,add_or_sub.get(), 'add')).pack(side='left', fill='y', expand=False,padx=5)
    tk.Button(second_frame, text='秒数归零', command=lambda: set_correction((int(time.time())+time_correction)%60,-1,'add')).pack(side='left',fill='y',expand=False,padx=5)
    second_frame.pack(side='left',fill='none',padx=5,pady=5)
    minute_frame = tk.ttk.Labelframe(change_correction_frame, text='分控制')
    tk.Button(minute_frame, text='1min', command=lambda: set_correction(60,add_or_sub.get(),'add')).pack(side='left', fill='y',expand=False, padx=5)
    tk.Button(minute_frame, text='10min', command=lambda: set_correction(600,add_or_sub.get(), 'add')).pack(side='left', fill='y',expand=False, padx=5)
    minute_frame.pack(side='left',fill='none', padx=5, pady=5)
    hour_frame = tk.ttk.Labelframe(change_correction_frame, text='小时控制')
    tk.Button(hour_frame, text='1hour', command=lambda: set_correction(3600, add_or_sub.get(), 'add')).pack(side='left',fill='y',expand=False,padx=5)
    tk.Button(hour_frame, text='10hours', command=lambda: set_correction(36000, add_or_sub.get(), 'add')).pack(side='left', fill='y', expand=False, padx=5)
    hour_frame.pack(side='left', fill='none', padx=5, pady=5)
    change_correction_frame.pack(fill='x',padx=5,pady=5)

    def update_time():
        system_time_label.config(text=get_time_str(correction=0,is_12_hrs=use_12_hour_clock.get()))
        old_time_label.config(text=get_time_str(correction=old_correction,is_12_hrs=use_12_hour_clock.get()))
        new_time_label.config(text=get_time_str(correction=time_correction,is_12_hrs=use_12_hour_clock.get()))
        correction_label.config(text='当前校正值：' + str(time_correction) + '秒')
        if window_is_open:
            w.after(500, update_time)
    update_time()

    def on_exit():
        nonlocal window_is_open
        window_is_open = False
        w.destroy()

    return_value = 0
    def on_ok():
        nonlocal return_value
        return_value = time_correction
        on_exit()
    def on_cancel():
        nonlocal return_value
        return_value = old_correction
        on_exit()

    buttons=tk.Frame(w)
    tk.Button(buttons,text='确定',command=on_ok).pack(side='right',fill='y',expand=False,padx=5,pady=5,ipadx=15)
    tk.Button(buttons,text='取消',command=on_cancel).pack(side='right',fill='y',expand=False,padx=5,pady=5,ipadx=15)
    buttons.pack(anchor='se', fill='none', expand=False)

    w.protocol("WM_DELETE_WINDOW", on_cancel)

    w.wait_window()
    return return_value

if __name__ == '__main__':
    root = tk.Tk()
    print(ask_time_correction(root,354))
    tk.mainloop()
