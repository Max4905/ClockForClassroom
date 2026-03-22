import tkinter as tk
from tkinter import ttk, font


class FontSelector:
    def __init__(self, root, title="选择字体"):
        self.root = root
        self.root.title(title)
        self.root.geometry("400x300")
        self.result = None

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 获取系统字体列表
        self.font_families = list(font.families())
        self.font_families.sort()

        # 预设的字号列表
        self.font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

        # 创建变量
        self.font_var = tk.StringVar(value=self.font_families[0] if self.font_families else "Arial")
        self.size_var = tk.IntVar(value=12)
        self.bold_var = tk.BooleanVar(value=False)
        self.italic_var = tk.BooleanVar(value=False)

        # 创建控件
        self.create_widgets(main_frame)

        # 创建预览标签
        self.preview_label = ttk.Label(main_frame, text="AaBbCc 字体示例",
                                       font=(self.font_var.get(), self.size_var.get()))
        self.preview_label.grid(row=3, column=0, columnspan=4, pady=15, sticky=tk.W)

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)

        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

        # 绑定事件以更新预览
        self.font_var.trace('w', self.update_preview)
        self.size_var.trace('w', self.update_preview)
        self.bold_var.trace('w', self.update_preview)
        self.italic_var.trace('w', self.update_preview)

        # 设置窗口行为
        self.root.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def create_widgets(self, parent):
        """创建界面控件"""
        # 字体选择
        ttk.Label(parent, text="字体:").grid(row=0, column=0, sticky=tk.W, pady=5)
        font_combo = ttk.Combobox(parent, textvariable=self.font_var,
                                  values=self.font_families, width=30)
        font_combo.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

        # 字号选择
        ttk.Label(parent, text="字号:").grid(row=1, column=0, sticky=tk.W, pady=5)
        size_combo = ttk.Combobox(parent, textvariable=self.size_var,
                                  values=self.font_sizes, width=10)
        size_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))

        # 样式选择
        ttk.Label(parent, text="样式:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Checkbutton(parent, text="加粗", variable=self.bold_var).grid(row=2, column=1, sticky=tk.W, padx=5)
        ttk.Checkbutton(parent, text="斜体", variable=self.italic_var).grid(row=2, column=2, sticky=tk.W)

    def update_preview(self, *args):
        """更新字体预览"""
        # 构建字体样式字符串
        font_weight = "bold" if self.bold_var.get() else "normal"
        font_slant = "italic" if self.italic_var.get() else "roman"

        # 更新预览标签
        self.preview_label.config(font=(self.font_var.get(), self.size_var.get(), font_weight, font_slant))

    def get_font(self):
        """获取当前选择的字体设置"""
        font_weight = "bold" if self.bold_var.get() else "normal"
        font_slant = "italic" if self.italic_var.get() else "roman"

        return (self.font_var.get(), self.size_var.get(), font_weight, font_slant)

    def on_ok(self):
        """确定按钮回调"""
        self.result = self.get_font()
        self.root.destroy()

    def on_cancel(self):
        """取消按钮回调"""
        self.result = None
        self.root.destroy()


def select_font(parent=None, title="选择字体"):
    """
    打开字体选择对话框

    参数:
        parent: 父窗口，如果为None则创建新的Tk实例
        title: 窗口标题

    返回:
        如果用户点击确定，返回字体元组 (字体名, 字号, 加粗状态, 斜体状态)
        如果用户取消，返回None
    """
    if parent is None:
        root = tk.Tk()
    else:
        root = tk.Toplevel(parent)

    selector = FontSelector(root, title)
    root.wait_window()

    return selector.result


def select_font_sync(parent=None, title="选择字体"):
    """
    同步版本的字体选择器（更简单的实现）

    返回:
        字体元组 (字体名, 字号, 加粗状态, 斜体状态)
    """
    if parent is None:
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
    else:
        root = parent

    # 创建选择对话框
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.transient(root)
    dialog.grab_set()

    # 获取系统字体
    font_families = list(font.families())
    font_families.sort()

    # 预设字号
    font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]

    # 创建变量
    font_var = tk.StringVar(value=font_families[0] if font_families else "Arial")
    size_var = tk.IntVar(value=12)
    bold_var = tk.BooleanVar(value=False)
    italic_var = tk.BooleanVar(value=False)

    # 结果变量
    result = None

    def update_preview():
        """更新预览"""
        weight = "bold" if bold_var.get() else "normal"
        slant = "italic" if italic_var.get() else "roman"
        preview_label.config(font=(font_var.get(), size_var.get(), weight, slant))

    def on_ok():
        nonlocal result
        weight = "bold" if bold_var.get() else "normal"
        slant = "italic" if italic_var.get() else "roman"
        result = (font_var.get(), size_var.get(), weight, slant)
        dialog.destroy()

    def on_cancel():
        nonlocal result
        result = None
        dialog.destroy()

    # 创建控件
    main_frame = ttk.Frame(dialog, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 字体选择
    ttk.Label(main_frame, text="字体:").grid(row=0, column=0, sticky=tk.W, pady=5)
    font_combo = ttk.Combobox(main_frame, textvariable=font_var,
                              values=font_families, width=30)
    font_combo.grid(row=0, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))

    # 字号选择
    ttk.Label(main_frame, text="字号:").grid(row=1, column=0, sticky=tk.W, pady=5)
    size_combo = ttk.Combobox(main_frame, textvariable=size_var,
                              values=font_sizes, width=10)
    size_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(5, 0))

    # 样式选择
    ttk.Label(main_frame, text="样式:").grid(row=2, column=0, sticky=tk.W, pady=5)
    ttk.Checkbutton(main_frame, text="加粗", variable=bold_var,
                    command=update_preview).grid(row=2, column=1, sticky=tk.W, padx=5)
    ttk.Checkbutton(main_frame, text="斜体", variable=italic_var,
                    command=update_preview).grid(row=2, column=2, sticky=tk.W)

    # 预览标签
    preview_frame = tk.LabelFrame(main_frame,text='预览')
    preview_label = ttk.Label(preview_frame, text="AaBbCc 字体示例")
    preview_frame.grid(row=3, column=0, columnspan=4, pady=15, sticky=tk.W)

    # 按钮
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=4, column=0, columnspan=4, pady=10)

    ttk.Button(button_frame, text="确定", command=on_ok).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="取消", command=on_cancel).pack(side=tk.LEFT, padx=5)

    # 绑定事件
    font_var.trace('w', lambda *args: update_preview())
    size_var.trace('w', lambda *args: update_preview())

    # 初始化预览
    update_preview()

    # 等待窗口关闭
    dialog.wait_window()

    return result


# 使用示例
if __name__ == "__main__":
    # 示例1: 使用类的方式
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 打开字体选择器
    font_tuple = select_font(root, "请选择字体")

    if font_tuple:
        print(f"选择的字体: {font_tuple}")
        print(f"  字体名: {font_tuple[0]}")
        print(f"  字号: {font_tuple[1]}")
        print(f"  加粗: {font_tuple[2]}")
        print(f"  斜体: {font_tuple[3]}")

        # 创建一个示例标签使用选择的字体
        example_root = tk.Tk()
        example_root.title("字体示例")

        label = tk.Label(
            example_root,
            text="这是一个使用所选字体的示例文本",
            font=font_tuple
        )
        label.pack(padx=20, pady=20)

        tk.Button(example_root, text="关闭", command=example_root.destroy).pack(pady=10)
        example_root.mainloop()
    else:
        print("用户取消了字体选择")

    # 示例2: 使用同步版本
    print("\n使用同步版本:")
    font_tuple2 = select_font_sync(None, "请选择字体2")
    if font_tuple2:
        print(f"选择的字体: {font_tuple2}")
