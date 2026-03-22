import tkinter as tk

def center_window(parent: tk.Tk | tk.Toplevel, child: tk.Toplevel):
    """
    将 child 窗口居中显示在 parent 窗口的中央。
    需要 child 已经完成初始布局（可调用 update_idletasks 刷新尺寸）。
    """
    child.update_idletasks()          # 确保获取正确的窗口尺寸
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    child_width = child.winfo_width()
    child_height = child.winfo_height()
    x = parent_x + (parent_width - child_width) // 2
    y = parent_y + (parent_height - child_height) // 2
    child.geometry(f"+{x}+{y}")
