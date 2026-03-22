import tkinter as tk
import tkinter.ttk as ttk

def ask_reminder(master:tk.Tk|tk.Toplevel,text:str,title:str,value:str) -> str:
    w=tk.Toplevel(master)
    w.config(padx=10, pady=10)
    w.title(title)
    frame_text_entry=tk.Frame(w)
    tk.Label(frame_text_entry,text=text).pack(side='top')
    entry = ttk.Entry(frame_text_entry)
    entry.insert(0, value)
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    entry.focus_set()
    entry.pack(side='top',fill='x',padx=5,pady=5,expand=True)
    frame_text_entry.pack(side='top',fill='x')

    buttons=tk.Frame(w)
    tk.Button(buttons,text='确定').pack(side='left',padx=5,pady=5,expand=False,ipadx=20,ipady=0)
    tk.Button(buttons, text='取消').pack(side='left', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    buttons.pack(side='bottom',fill='none',padx=5,pady=5)

    #todo:返回部分

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clock")
    root.resizable(width=False, height=False)
    ask_reminder(root)
    root.mainloop()
