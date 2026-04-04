import tkinter as tk
import webbrowser
from tkinter import ttk


def show_about():
    """显示关于界面的主函数"""
    # 创建顶层窗口
    about_win = tk.Toplevel()
    about_win.title("关于 Clock For Classroom")
    about_win.transient()


    # 创建 Notebook（标签页容器）
    notebook = ttk.Notebook(about_win)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # ---------- 第一个标签页：软件信息 ----------
    tab_info = ttk.Frame(notebook)
    notebook.add(tab_info, text="软件信息")

    # 使用 Text 组件展示关于文本（支持滚动条）
    text_frame = ttk.Frame(tab_info)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("微软雅黑", 10), height=10, width=20)
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 插入 about_text 内容
    about_text = '''Clock For Classroom v1.3.1
正式版 总计第8次更新

关于开发者
黄天敬泽
Max490545149@outlook.com

2026-03-31
'''
    text_widget.insert(tk.END, about_text)
    text_widget.configure(state=tk.DISABLED)  # 设置为只读

    # ---------- 第二个标签页：相关链接 ----------
    tab_links = ttk.Frame(notebook)
    notebook.add(tab_links, text="相关链接")

    # 链接容器
    links_frame = ttk.Frame(tab_links)
    links_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # 项目地址（可点击，带下划线）
    project_label = tk.Label(
        links_frame,
        text="项目地址：https://github.com/Max4905/ClockForClassroom",
        fg="blue",
        cursor="hand2",
        font=("微软雅黑", 10, "underline")   # 添加下划线
    )
    project_label.pack(anchor=tk.W, pady=5)
    project_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Max4905/ClockForClassroom"))

    # 说明文字（不可点击）
    desc_label = tk.Label(
        links_frame,
        text="如果连安卓都变得封闭，那么移动设备将不再拥有软件自由。",
        font=("微软雅黑", 10),
        wraplength=500,
        justify=tk.LEFT
    )
    desc_label.pack(anchor=tk.W, pady=(20, 5))

    # Keep Android Open 链接（可点击，带下划线）
    keep_label = tk.Label(
        links_frame,
        text="https://keepandroidopen.org/zh-CN/",
        fg="blue",
        cursor="hand2",
        font=("微软雅黑", 10, "underline")   # 添加下划线
    )
    keep_label.pack(anchor=tk.W, pady=5)
    keep_label.bind("<Button-1>", lambda e: webbrowser.open("https://keepandroidopen.org/zh-CN/"))

    # 关闭按钮
    btn_close = ttk.Button(about_win, text="关闭", command=about_win.destroy)
    btn_close.pack(pady=10)

    # 使窗口居中显示
    about_win.update_idletasks()
    width = about_win.winfo_width()
    height = about_win.winfo_height()
    x = (about_win.winfo_screenwidth() // 2) - (width // 2)
    y = (about_win.winfo_screenheight() // 2) - (height // 2)
    about_win.geometry(f"+{x}+{y}")

    # 设置窗口焦点
    about_win.grab_set()
    about_win.focus_set()
    about_win.wait_window()

if __name__ == "__main__":
    # 若直接运行此脚本，创建一个根窗口并调用关于界面
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    show_about()
    root.destroy()
