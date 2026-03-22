import random
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from window_tools import center_window

encouraging_words = ["学习不是填充空桶，而是点燃火焰。",
                     "拥有液泡的力量，胜利是必然的！",
                     "这是计划的一部分。",
                     "专注当下，让每一分钟的学习都产生价值。",
                     "学习如同登山，过程或许艰难，但山顶的风景值得一切。",
                     "今天的汗水，浇灌明天的果实。",
                     "给岁月以文明，而不是给文明以岁月。",
                     "只送大脑。",
                     "弱小和无知不是生存的障碍，傲慢才是。",
                     "前进，不择手段地前进！",
                     "快跑。傻孩子们，快跑啊——",
                     "藏好自己，做好清理。",
                     "\"自然选择\"号，前进四！",
                     "此后如竟没有炬火，我便是那唯一的光。",
                     "人生总会有一段特殊的黑暗时间，如果因为畏惧未来而驻足不前，那只会被永远困死在黑暗中。",
                     "人间的恶意，又怎能跟那最深处的绝望相比？",
                     "它或许没有照亮黑夜的能力，但它有不融入黑暗的勇气。",
                     "没关系的，都一样。",
                     "适当的低调没有问题，但不能一直把自己埋在尘土里，那样你的锋芒会生锈的。 ",
                     "山无处不在，只是登法不同。"
                     ]

def ask_reminder_dialog(master: tk.Tk | tk.Toplevel, original_value:str= '') -> str:
    w=tk.Toplevel(master)
    w.config(padx=10, pady=10)
    frame_text_entry=tk.Frame(w)
    tk.Label(frame_text_entry,text='输入的文本将会被显示到时钟窗口底部。\n不需要请留空以后按确定。\n多行文本分隔符请参阅下方菜单的选项。').pack(side='top')
    entry = ttk.Entry(frame_text_entry,width=50)
    random.shuffle(encouraging_words)
    i=0
    if original_value != '':
        entry.insert(0, original_value)
    else:
        entry.insert(0, encouraging_words[i])
        i+=1
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    entry.focus_set()
    entry.pack(side='top',fill='x',padx=5,pady=5,expand=True)
    frame_text_entry.pack(side='top',fill='x')

    return_value = original_value
    def on_ok(event=None):
        nonlocal return_value
        return_value = entry.get().replace(newline_escape_sequence.get(),'\n')
        keywords1 = ['7', '七', 'Max', 'max', 'beaver', 'Beaver','htjz','黄天敬泽']
        keywords2 = ['gay', 'Gay', '南通', '男童', '男同', '南桐','男娘']
        condition = any(kw in return_value for kw in keywords1) and any(kw in return_value for kw in keywords2)
        if condition:
            tkinter.messagebox.showerror('无效的值','输入的文本似乎无效，请重试。')
            set_entry(original_value)
            return_value = original_value
            return
        w.destroy()

    def clear_entry():
        entry.delete(0, tk.END)
    def set_entry(content:str):
        clear_entry()
        entry.insert(tk.END, content)
        entry.select_range(0, tk.END)
        entry.icursor(tk.END)
        entry.focus_set()
    def random_entry():
        nonlocal i
        set_entry(encouraging_words[i])
        i+=1
        if i>=len(encouraging_words):
            i=0

    newline_escape_sequence = tk.StringVar(value='/')

    opers=tk.Menu(w, tearoff=False)
    opers.add_command(label='清空', command=clear_entry)
    opers.add_command(label='还原', command=lambda: set_entry(original_value))
    opers.add_separator()
    opers.add_command(label='随机生成', command=random_entry)

    newline_escape_menu = tk.Menu(w, tearoff=False)
    newline_escape_menu.add_radiobutton(label='/',variable=newline_escape_sequence)
    newline_escape_menu.add_radiobutton(label='\\',variable=newline_escape_sequence)
    newline_escape_menu.add_radiobutton(label='\\n',variable=newline_escape_sequence)

    buttons=tk.Frame(w)
    tk.Button(buttons,text='确定', command=on_ok).pack(side='left',padx=5,pady=5,expand=False,ipadx=20,ipady=0)
    tk.Button(buttons, text='取消',command=w.destroy).pack(side='left', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    oper_mb=ttk.Menubutton(w,text='操作',menu=opers)
    oper_mb.config(menu=opers)
    oper_mb.pack(side='right', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    newline_mb = ttk.Menubutton(w,text='换行转义选项',menu=newline_escape_menu)
    newline_mb.config(menu=newline_escape_menu)
    newline_mb.pack(side='right', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    buttons.pack(side='bottom',fill='none',padx=5,pady=5)

    entry.bind('<Return>', on_ok)
    w.bind('<Escape>',lambda e: w.destroy())

    w.transient(master)
    w.resizable(True,False)
    w.grab_set()
    center_window(master, w)

    w.wait_window()
    return return_value

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clock")
    root.resizable(width=False, height=False)
    print(ask_reminder_dialog(root, 'aaa'))
    root.mainloop()
