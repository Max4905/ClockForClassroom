import random
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
import os
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

def ask_reminder_dialog(master: tk.Tk | tk.Toplevel, original_value: str = '') -> str:
    # ---------- 历史记录相关函数 ----------
    history_file = "./reminder_history.txt"

    def save_to_history(text: str):
        if not text.strip():
            return
        lines = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                lines = [line.rstrip('\n') for line in f]
        if text not in lines:
            with open(history_file, 'a', encoding='utf-8') as f:
                f.write(text + '\n')

    def load_history() -> list:
        if not os.path.exists(history_file):
            return []
        with open(history_file, 'r', encoding='utf-8') as f:
            return [line.rstrip('\n') for line in f]

    def open_history_dialog(parent, set_callback):
        hist_win = tk.Toplevel(parent)
        hist_win.title("历史记录")
        hist_win.geometry("400x300")
        hist_win.transient(parent)
        hist_win.grab_set()

        frame = tk.Frame(hist_win)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        history_items = load_history()
        for item in history_items:
            listbox.insert(tk.END, item)

        def on_select():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                selected_text = listbox.get(index)
                set_callback(selected_text)
                hist_win.destroy()

        def on_double_click(event):
            on_select()

        listbox.bind('<Double-Button-1>', on_double_click)

        # ----- 新增：清空历史功能 -----
        def clear_history():
            if tkinter.messagebox.askyesno("确认清空", "确定要清空所有历史记录吗？此操作不可撤销。"):
                # 清空文件
                with open(history_file, 'w', encoding='utf-8') as f:
                    f.write('')
                # 清空列表框
                listbox.delete(0, tk.END)

        btn_frame = tk.Frame(hist_win)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        # 清空历史按钮放在最左侧，边距与其他按钮一致
        tk.Button(btn_frame, text="清空历史", command=clear_history).pack(side=tk.LEFT, padx=5, ipadx=20, ipady=0)
        tk.Button(btn_frame, text="确定", command=on_select).pack(side='right', padx=5, ipadx=20, ipady=0)
        tk.Button(btn_frame, text="取消", command=hist_win.destroy).pack(side='right', padx=5, ipadx=20, ipady=0)

        center_window(parent, hist_win)
        hist_win.wait_window()

    # ---------- 预设语句选择窗口 ----------
    def open_preset_dialog(parent, set_callback):
        preset_win = tk.Toplevel(parent)
        preset_win.title("预设语句")
        preset_win.geometry("500x350")
        preset_win.transient(parent)
        preset_win.grab_set()

        frame = tk.Frame(preset_win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        for item in encouraging_words:
            listbox.insert(tk.END, item)

        def on_select():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                selected_text = listbox.get(index)
                set_callback(selected_text)
                preset_win.destroy()

        def on_double_click(event):
            on_select()

        listbox.bind('<Double-Button-1>', on_double_click)

        btn_frame = tk.Frame(preset_win)
        btn_frame.pack(side='right', fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="确定", command=on_select).pack(side='right', padx=5, ipadx=20, ipady=0)
        tk.Button(btn_frame, text="取消", command=preset_win.destroy).pack(side='right', padx=5, ipadx=20, ipady=0)

        center_window(parent, preset_win)
        preset_win.wait_window()
    # -----------------------------------------

    w = tk.Toplevel(master)
    w.config(padx=10, pady=10)
    frame_text_entry = tk.Frame(w)
    tk.Label(frame_text_entry, text='输入的文本将会被显示到时钟窗口底部。\n不需要请留空以后按确定。\n多行文本分隔符请参阅下方菜单的选项。').pack(side='top')
    entry = ttk.Entry(frame_text_entry, width=50)
    random.shuffle(encouraging_words)
    i = 0
    if original_value != '':
        entry.insert(0, original_value)
    else:
        entry.insert(0, encouraging_words[i])
        i += 1
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    entry.focus_set()
    entry.pack(side='top', fill='x', padx=5, pady=5, expand=True)
    frame_text_entry.pack(side='top', fill='x')

    return_value = original_value

    def on_ok(event=None):
        nonlocal return_value
        raw_text = entry.get()
        save_to_history(raw_text)
        return_value = raw_text.replace(newline_escape_sequence.get(), '\n')
        keywords1 = ['7', '七', 'Max', 'max', 'beaver', 'Beaver', 'htjz', '黄天敬泽']
        keywords2 = ['gay', 'Gay', '南通', '男童', '男同', '南桐', '男娘']
        condition = any(kw in return_value for kw in keywords1) and any(kw in return_value for kw in keywords2)
        if condition:
            tkinter.messagebox.showerror('无效的值', '输入的文本似乎无效，请重试。')
            set_entry(original_value)
            return_value = original_value
            return
        w.destroy()

    def clear_entry():
        entry.delete(0, tk.END)

    def set_entry(content: str):
        clear_entry()
        entry.insert(tk.END, content)
        entry.select_range(0, tk.END)
        entry.icursor(tk.END)
        entry.focus_set()

    def random_entry():
        nonlocal i
        set_entry(encouraging_words[i])
        i += 1
        if i >= len(encouraging_words):
            i = 0

    newline_escape_sequence = tk.StringVar(value='/')

    opers = tk.Menu(w, tearoff=False)
    opers.add_command(label='清空', command=clear_entry)
    opers.add_command(label='还原', command=lambda: set_entry(original_value))
    opers.add_command(label='随机生成', command=random_entry)
    opers.add_separator()
    opers.add_command(label='历史记录', command=lambda: open_history_dialog(w, set_entry))
    opers.add_command(label='预设语句', command=lambda: open_preset_dialog(w, set_entry))


    newline_escape_menu = tk.Menu(w, tearoff=False)
    newline_escape_menu.add_radiobutton(label='/', variable=newline_escape_sequence)
    newline_escape_menu.add_radiobutton(label='\\', variable=newline_escape_sequence)
    newline_escape_menu.add_radiobutton(label='\\n', variable=newline_escape_sequence)

    buttons = tk.Frame(w)
    oper_mb = ttk.Menubutton(w, text='操作', menu=opers)
    oper_mb.config(menu=opers)
    oper_mb.pack(side='right', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    newline_mb = ttk.Menubutton(w, text='换行转义选项', menu=newline_escape_menu)
    newline_mb.config(menu=newline_escape_menu)
    newline_mb.pack(side='right', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    tk.Button(buttons, text='确定', command=on_ok).pack(side='left', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    tk.Button(buttons, text='取消', command=w.destroy).pack(side='left', padx=5, pady=5, expand=False, ipadx=20, ipady=0)
    buttons.pack(side='bottom', fill='none', padx=5, pady=5)

    entry.bind('<Return>', on_ok)
    w.bind('<Escape>', lambda e: w.destroy())

    w.transient(master)
    w.resizable(True, False)
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
