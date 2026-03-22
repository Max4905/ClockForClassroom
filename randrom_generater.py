import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import random
from window_tools import center_window

class RandomWindow(tk.Toplevel):
    """随机数生成器窗口"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.load_config()
        self.title("随机数生成器")
        self.minsize(300, 200)

        # --- 默认配置 ---
        self.min_val = 1
        self.max_val = 40
        self.exclude_set = set()           # 排除的数字集合
        self.number_count = 1              # 每次生成的个数
        self.font_size = 36                # 默认字号
        self.topmost = False
        self.history = []                  # 历史记录列表

        # --- 创建界面 ---
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill='both')

        self.number_label = tk.Label(
            self.main_frame,
            text="?",
            font=("Arial", self.font_size, "bold"),
            cursor="hand2"
        )
        self.number_label.pack(expand=True, pady=10)   # 上下留一点呼吸空间

        # 绑定点击事件：点击标签重新生成
        self.number_label.bind("<Button-1>", lambda e: self.generate_random())

        # 菜单栏
        self.create_menu()

        # 初始生成一个随机数
        self.generate_random()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # ========== 随机数菜单 ==========
        random_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="随机数", menu=random_menu)

        # 范围与排除（打开复合对话框）
        random_menu.add_command(label="范围与排除", command=self.set_range_and_exclude)
        # 生成个数
        random_menu.add_command(label="生成个数", command=self.set_number_count)
        # 历史记录
        random_menu.add_command(label="查看历史", command=self.show_history)
        random_menu.add_separator()

        # 退出
        random_menu.add_command(label="退出", command=self.quit_app)

        # ========== 显示菜单 ==========
        display_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="显示", menu=display_menu)

        # 字号（滑块）
        display_menu.add_command(label="字体大小", command=self.set_font_size_slider)

        # 窗口大小控制
        self.resize_var = tk.BooleanVar(value=False)
        display_menu.add_checkbutton(
            label="允许调整窗口大小",
            variable=self.resize_var,
            command=self.toggle_resizable
        )
        display_menu.add_command(label="重置窗口大小", command=self.reset_window_size)

    # ---------- 随机数菜单功能 ----------
    def set_range_and_exclude(self):
        """弹出对话框设置范围（滑块）和排除数字"""
        dialog = tk.Toplevel(self,padx=15,pady=5)
        dialog.title("设置范围与排除数字")
        dialog.transient(self)
        dialog.grab_set()

        # 绑定 Esc 键关闭对话框
        dialog.bind("<Escape>", lambda e: dialog.destroy())

        # ---- 最小值滑块 ----
        tk.Label(dialog, text="最小值：").pack(pady=(10, 0))
        min_var = tk.IntVar(value=self.min_val)
        min_slider = tk.Scale(
            dialog, from_=1, to=100, orient=tk.HORIZONTAL,
            variable=min_var, resolution=1, length=300
        )
        min_slider.pack(pady=5)

        # ---- 最大值滑块 ----
        tk.Label(dialog, text="最大值：").pack(pady=(10, 0))
        max_var = tk.IntVar(value=self.max_val)
        max_slider = tk.Scale(
            dialog, from_=1, to=100, orient=tk.HORIZONTAL,
            variable=max_var, resolution=1, length=300
        )
        max_slider.pack(pady=5)

        # 联动逻辑：最小值不能大于最大值
        def check_min_max(*args):
            if min_var.get() > max_var.get():
                max_var.set(min_var.get())
        min_var.trace_add("write", check_min_max)
        max_var.trace_add("write", check_min_max)

        # ---- 排除数字输入框 ----
        tk.Label(dialog, text="排除数字（逗号分隔）：").pack(pady=(10, 0))
        exclude_entry = ttk.Entry(dialog, width=40)
        exclude_entry.pack(pady=5)
        # 填入当前排除集
        exclude_entry.insert(0, ",".join(str(x) for x in sorted(self.exclude_set)))

        # ---- 按钮 ----
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        def apply():
            new_min = min_var.get()
            new_max = max_var.get()
            if new_min > new_max:
                messagebox.showerror("错误", "最小值不能大于最大值")
                return
            # 解析排除数字
            new_exclude = set()
            text = exclude_entry.get().strip()
            if text:
                for part in text.split(","):
                    part = part.strip()
                    if part == "":
                        continue
                    if part.lstrip('-').isdigit():
                        new_exclude.add(int(part))
                    else:
                        messagebox.showerror("错误", f"“{part}”不是有效的整数")
                        return
            # 更新配置
            self.min_val = new_min
            self.max_val = new_max
            self.exclude_set = new_exclude
            # 重新生成
            self.generate_random()
            dialog.destroy()

        btn_ok = tk.Button(btn_frame, text="确定", command=apply)
        btn_ok.pack(side="left", padx=10, ipadx=20, ipady=0)
        btn_cancel = tk.Button(btn_frame, text="取消", command=dialog.destroy)
        btn_cancel.pack(side="left", padx=10, ipadx=20, ipady=0)

        center_window(self,dialog)

    def set_number_count(self):
        """弹出滑块设置每次生成的随机数个数"""
        dialog = tk.Toplevel(self,padx=15,pady=5)
        dialog.title("设置生成个数")
        dialog.transient(self)
        dialog.grab_set()
        dialog.bind("<Escape>", lambda e: dialog.destroy())

        # 动态计算最大可用数字个数
        available = self.get_available_numbers()
        max_count = max(1, len(available))  # 至少为1

        tk.Label(dialog, text=f"每次生成个数（1~{max_count}）：").pack(pady=10)

        count_var = tk.IntVar(value=min(self.number_count, max_count))
        slider = tk.Scale(
            dialog, from_=1, to=max_count, orient=tk.HORIZONTAL,
            variable=count_var, resolution=1, length=250
        )
        slider.pack(pady=10)

        def apply():
            new_count = count_var.get()
            if new_count > max_count:
                messagebox.showerror("错误", f"最多只能生成 {max_count} 个不同的数字")
                return
            self.number_count = new_count
            self.generate_random()
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        btn_ok = tk.Button(btn_frame, text="确定", command=apply)
        btn_ok.pack(side="left", padx=10, ipadx=20, ipady=0)
        btn_cancel = tk.Button(btn_frame, text="取消", command=dialog.destroy)
        btn_cancel.pack(side="left", padx=10, ipadx=20, ipady=0)

        center_window(self,dialog)

    def get_available_numbers(self):
        """返回当前范围内未被排除的数字列表"""
        return [n for n in range(self.min_val, self.max_val + 1) if n not in self.exclude_set]

    def generate_random(self):
        """生成指定个数的随机数（考虑排除），更新显示，并记录历史"""
        available = self.get_available_numbers()
        if not available:
            self.number_label.config(text="无可用数字")
            self.history.append("无可用数字")
            return

        # 限制生成个数不超过可用数字总数
        count = min(self.number_count, len(available))
        # 随机抽取（可重复）
        if count == 1:
            chosen = random.choice(available)
            result_str = str(chosen)
        else:
            chosen_list = random.choices(available, k=count)
            result_str = ", ".join(str(x) for x in chosen_list)

        self.number_label.config(text=result_str, font=("Arial", self.font_size, "bold"))
        # 记录历史
        self.history.append(result_str)

    # ---------- 显示菜单功能 ----------
    def set_font_size_slider(self):
        """弹出滑块设置字号"""
        dialog = tk.Toplevel(self,padx=15,pady=5)
        dialog.title("字体大小")
        dialog.transient(self)
        dialog.grab_set()
        dialog.bind("<Escape>", lambda e: dialog.destroy())

        tk.Label(dialog, text="字号（12~72）：").pack(pady=10)

        size_var = tk.IntVar(value=self.font_size)
        slider = tk.Scale(
            dialog, from_=12, to=72, orient=tk.HORIZONTAL,
            variable=size_var, resolution=1, length=250
        )
        slider.pack(pady=10)

        def apply():
            new_size = size_var.get()
            self.font_size = new_size
            self.number_label.config(font=("Arial", self.font_size, "bold"))
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        btn_ok = tk.Button(btn_frame, text="确定", command=apply)
        btn_ok.pack(side="left", padx=10, ipadx=20, ipady=0)
        btn_cancel = tk.Button(btn_frame, text="取消", command=dialog.destroy)
        btn_cancel.pack(side="left", padx=10, ipadx=20, ipady=0)

        center_window(self,dialog)

    def toggle_resizable(self):
        """切换窗口大小调整能力"""
        if self.resize_var.get():
            self.resizable(True, True)
        else:
            self.resizable(False, False)

    def reset_window_size(self):
        """重置窗口大小为初始几何"""
        self.geometry('')

    # ---------- 历史记录 ----------
    def show_history(self):
        """弹出独立窗口显示随机数历史"""
        hist_win = tk.Toplevel(self,padx=15,pady=5)
        hist_win.title("随机数历史")
        hist_win.geometry("400x300")
        hist_win.transient(self)
        hist_win.grab_set()
        hist_win.bind("<Escape>", lambda e: hist_win.destroy())

        # 列表框
        listbox = tk.Listbox(hist_win, font=("Consolas", 10))
        listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # 滚动条
        scrollbar = tk.Scrollbar(hist_win)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        # 填入历史（倒序显示，最新的在上）
        for item in reversed(self.history):
            listbox.insert(tk.END, item)

        # 底部按钮
        btn_frame = tk.Frame(hist_win)
        btn_frame.pack(side="bottom", fill="x", pady=5)

        def clear_history():
            self.history.clear()
            listbox.delete(0, tk.END)

        btn_clear = tk.Button(btn_frame, text="清除历史", command=clear_history)
        btn_clear.pack(side="left", padx=10, ipadx=20, ipady=0)
        btn_close = tk.Button(btn_frame, text="关闭", command=hist_win.destroy)
        btn_close.pack(side="right", padx=10, ipadx=20, ipady=0)

    def get_config_file_path(self):
        """返回配置文件路径"""
        return './random_config.json'

    def save_config(self):
        """保存当前配置到 JSON 文件"""
        config = {
            "min_val": self.min_val,
            "max_val": self.max_val,
            "exclude_set": list(self.exclude_set),  # 转换为列表存储
            "number_count": self.number_count,
            "font_size": self.font_size,
            "topmost": self.topmost,
            "resizable": self.resize_var.get(),  # 窗口可调整状态
            "geometry": self.geometry()  # 保存窗口位置和大小
        }
        try:
            with open(self.get_config_file_path(), "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def load_config(self):
        """从 JSON 文件加载配置"""
        config_path = self.get_config_file_path()
        if not os.path.exists(config_path):
            return  # 无配置文件，使用默认值

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"读取配置失败: {e}")
            return

        # 安全更新配置（类型转换）
        if "min_val" in config:
            self.min_val = int(config["min_val"])
        if "max_val" in config:
            self.max_val = int(config["max_val"])
        if "exclude_set" in config and isinstance(config["exclude_set"], list):
            self.exclude_set = set(config["exclude_set"])
        if "number_count" in config:
            self.number_count = int(config["number_count"])
        if "font_size" in config:
            self.font_size = int(config["font_size"])
            self.number_label.config(font=("Arial", self.font_size, "bold"))
        if "topmost" in config:
            self.topmost = bool(config["topmost"])
            self.attributes('-topmost', self.topmost)
        if "resizable" in config:
            self.resize_var.set(bool(config["resizable"]))
            self.resizable(self.resize_var.get(), self.resize_var.get())
        if "geometry" in config:
            self.geometry(config["geometry"])

    # ---------- 退出 ----------
    def quit_app(self):
        """完全退出程序"""
        self.save_config()
        self.master.destroy()
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()   # 隐藏主窗口
    app = RandomWindow(root)
    app.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), app.destroy()))
    root.mainloop()
