import tkinter as tk

def ask_number(master: tk.Tk | tk.Toplevel,
               title: str,
               prompt: str,
               label: str | None = None,
               min_num: int = 0,
               max_num: int = 100,
               default: int = 0) -> int:
    """
    弹出一个带滑动条的数字输入对话框。

    参数:
        master: 父窗口
        title: 对话框标题
        prompt: 提示文字
        label: 滑动条标签（可选）
        min_num: 最小值
        max_num: 最大值
        default: 默认值（会自动限制在 min_num 和 max_num 之间）

    返回:
        用户选择的值（确定时返回滑动条值，取消/关闭时返回默认值）
    """
    # 确保默认值在有效范围内
    default = max(min_num, min(default, max_num))

    w = tk.Toplevel(master, padx=10, pady=10)
    w.title(title)
    w.resizable(False, False)
    w.transient(master)
    w.grab_set()

    # 提示标签
    tk.Label(w, text=prompt).pack(pady=(0, 10))

    # 滑动条
    scale = tk.Scale(w,
                     from_=min_num,
                     to=max_num,
                     orient=tk.HORIZONTAL,
                     length=300,
                     resolution=1,
                     label=label)
    scale.set(default)          # 设置默认值
    scale.pack(pady=10)

    # 存放结果的变量
    result = default

    def on_ok():
        nonlocal result
        result = scale.get()
        w.destroy()

    def on_cancel():
        nonlocal result
        result = default
        w.destroy()

    # 按钮框架
    btn_frame = tk.Frame(w)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="确定", width=8, command=on_ok).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="取消", width=8, command=on_cancel).pack(side=tk.LEFT, padx=5)

    # 处理窗口直接关闭（点击 X）
    w.protocol("WM_DELETE_WINDOW", on_cancel)

    # 等待窗口关闭
    w.wait_window()

    return result


if __name__ == '__main__':
    root = tk.Tk()
    value = ask_number(root,
                       title='请输入数字',
                       prompt='请选择一个数值：',
                       label='数值',
                       min_num=0,
                       max_num=100,
                       default=50)
    print(f"用户选择了: {value}")
    # 注意：实际使用中不需要再调用 mainloop()，因为对话框已等待用户操作
    # 如果需要显示主窗口，可以调用 root.deiconify()
