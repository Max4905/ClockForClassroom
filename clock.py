import datetime
import sys
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog

import about
import class_schedule
import randrom_generater
import time_correction as time_correction_file
import widgets.ask_num
from ask_reminder import ask_reminder_dialog
from class_schedule import ClassSchedule
from window_tools import center_window

DEBUG=False
if '--debug' in sys.argv:
    DEBUG = True

w = tk.Tk()
w.title("时钟")
w.resizable(0,0)

w.tk.call('tk', 'scaling', w.tk.call('tk', 'scaling'))


date_format_labels = ['%Y-%m-%d', '%y-%m-%d', '%Y/%m/%d', '%y/%m/%d', '%Y.%m.%d', '%m.%d', '%y%m%d', '%Y%m%d', '%m%d']
font_size_options = ['22 16', '32 18', '36 20', '48 26', '72 36']
clock_color_options = ['#000000 #F0F0F0', '#FFFFFF #000000', '#F0F0F0 #10382E', '#F0F0F0 #09426C']
update_delay_choices = [100,500,1000,5000,10000,60000]
SCHEDULE_FILE = './class_schedule.json'

# 默认配置
default_clock_data = {
    'clock_font': ('Consolas', 22),
    'date_font': ('等线', 16),
    'reminder_font': ('等线', 14),
    'time_correction_seconds': 0,
    'use_12_hrs_clock': True,
    'show_seconds': True,
    'string_reminder': '',
    'clock_fg_color': "#000000",
    'clock_bg_color': '#F0F0F0',
    'window_close_action': 0,
    'window_title': '时钟'
}


CONFIG_FILE = 'clock.json'
clock_data = default_clock_data.copy()  # 先设为默认值

def read_class_schedule():
    try:
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            global schedule
            loaded_data = json.load(f)
            schedule = ClassSchedule(loaded_data)
    except FileNotFoundError:
        tkinter.messagebox.showinfo('文件不存在','找不到课表文件 class_schedule.json。无法显示课表。')
        with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
            f.write('{}')
        schedule = ClassSchedule(None)
    except json.JSONDecodeError as e:
        tkinter.messagebox.showerror('文件格式错误','无法正确读取课表文件。检查json语法，然后再试一次。')
        schedule = ClassSchedule(None)
    except Exception as e:
        tkinter.messagebox.showerror('发生错误','未知错误。'+str(e))
        schedule = ClassSchedule(None)

read_class_schedule()


required_keys = {
        'clock_font': (list, tuple),
        'date_font': (list, tuple),
        'reminder_font': (list, tuple),
        'time_correction_seconds': (int, float),
        'use_12_hrs_clock': bool,
        'show_seconds': bool,
        'string_reminder':str,
        'clock_fg_color': str,
        'clock_bg_color': str,
        'window_close_action': int,
        'window_title': str
}

import json
import os
from typing import Any, Dict, Optional, Callable, Union

class ConfigManager:
    """
    配置管理器，提供默认值、类型校验和文件持久化。

    用法:
        default = {"volume": 70, "theme": "dark"}
        type_rules = {"volume": int, "theme": str}
        config = ConfigManager("settings.json", default, type_rules)
        print(config["volume"])          # 70
        config["volume"] = 80            # 自动保存（可选）
        config.save()                    # 手动保存
    """

    def __init__(
        self,
        file_path: str,
        default_config: Dict[str, Any],
        type_rules: Optional[Dict[str, Union[type, Callable]]] = None,
        auto_save: bool = False
    ):
        """
        参数:
            file_path: 配置文件路径
            default_config: 默认配置字典（所有键的默认值）
            type_rules: 类型规则字典，键为配置项名，值为期望的类型或校验函数
            auto_save: 每次修改后是否自动保存到文件
        """
        self.file_path = file_path
        self.default_config = default_config.copy()
        self.type_rules = type_rules or {}
        self.auto_save = auto_save
        self._data = self.default_config.copy()
        self.load()

    # -------------------- 核心方法 --------------------
    def load(self) -> None:
        """从文件加载配置，合并默认值并进行类型校验"""
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            if not isinstance(loaded, dict):
                raise ValueError("配置文件根内容不是字典")

            # 合并：用户配置覆盖默认值
            merged = {**self.default_config, **loaded}
            # 类型校验和清理
            validated = self._validate(merged)
            self._data = validated
        except (json.JSONDecodeError, OSError, ValueError) as e:
            print(f"加载配置文件失败: {e}，将使用默认配置")

    def save(self) -> bool:
        """将当前配置保存到文件，返回是否成功"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
            return True
        except OSError as e:
            print(f"保存配置文件失败: {e}")
            return False

    def saveas(self,file):
        def save(self) -> bool:
            """将当前配置保存到文件，返回是否成功"""
            try:
                with open(file, 'w', encoding='utf-8') as f:
                    json.dump(self._data, f, indent=4, ensure_ascii=False)
                return True
            except OSError as e:
                print(f"保存配置文件失败: {e}")
                return False

    def _validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据 type_rules 校验配置项，返回清洗后的字典。
        - 如果值类型不符，使用默认值替换并发出警告。
        - 对于缺失的必要键，自动从默认配置补充。
        """
        validated = {}
        # 先确保所有默认键都存在
        for key, default_value in self.default_config.items():
            if key in data:
                value = data[key]
            else:
                value = default_value

            # 类型检查
            if key in self.type_rules:
                rule = self.type_rules[key]
                if isinstance(rule, type):
                    if not isinstance(value, rule):
                        print(f"警告: 配置项 '{key}' 应为 {rule.__name__} 类型，实际为 {type(value).__name__}，使用默认值 {default_value}")
                        value = default_value
                elif callable(rule):  # 自定义校验函数，应返回 (是否有效, 修正后的值)
                    try:
                        is_valid, corrected = rule(value)
                        if not is_valid:
                            print(f"警告: 配置项 '{key}' 校验失败，使用默认值 {default_value}")
                            value = default_value
                        else:
                            value = corrected
                    except Exception:
                        print(f"警告: 配置项 '{key}' 校验函数异常，使用默认值 {default_value}")
                        value = default_value
            validated[key] = value

        # 额外处理用户配置中多余的合法项目（可选，这里直接忽略）
        return validated

    # -------------------- 字典接口 --------------------
    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        # 可选：对单个值进行类型检查
        if key in self.type_rules:
            rule = self.type_rules[key]
            if isinstance(rule, type) and not isinstance(value, rule):
                raise TypeError(f"配置项 '{key}' 应为 {rule.__name__} 类型，无法设置为 {type(value).__name__}")
        self._data[key] = value
        if self.auto_save:
            self.save()

    def __delitem__(self, key: str) -> None:
        # 删除键会恢复默认值（而非真正删除）
        if key in self.default_config:
            self._data[key] = self.default_config[key]
        else:
            del self._data[key]
        if self.auto_save:
            self.save()

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"ConfigManager({self.file_path})"

    # -------------------- 额外便捷方法 --------------------
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def update(self, other: Dict[str, Any]) -> None:
        """批量更新配置，会进行类型校验"""
        for k, v in other.items():
            self[k] = v

    def reset_to_default(self) -> None:
        """重置所有配置到默认值"""
        self._data = self.default_config.copy()
        if self.auto_save:
            self.save()

    def reload(self) -> None:
        """重新从文件加载（放弃未保存的更改）"""
        self.load()
clock_data = ConfigManager(CONFIG_FILE,default_clock_data,required_keys)

window_is_open = True
def on_closing():
    global window_is_open
    window_is_open = False
    if save_config_before_exit.get():
        clock_data.save()
    w.destroy()
    print('窗口关闭')
    exit()

chosen_font_name = ()
use_12_hour_clock = tk.BooleanVar(value=clock_data['use_12_hrs_clock'])
show_seconds = tk.BooleanVar(value=clock_data['show_seconds'])
weekday_mode = tk.StringVar(value='short')
date_mode = tk.StringVar(value='%Y-%m-%d')
window_mode = tk.IntVar(value=0)
font_size = tk.StringVar(value=str(clock_data['clock_font'][1])+' '+str(clock_data['date_font'][1]))
clock_color = tk.StringVar(value=clock_data['clock_fg_color']+' '+clock_data['clock_bg_color'])
clock_string_reminder = tk.StringVar(value=clock_data['string_reminder'])
current_window_mode = window_mode.get()
window_close_action = tk.IntVar(value=clock_data['window_close_action'])
save_config_before_exit = tk.BooleanVar(value=True)
update_delay_ms = tk.IntVar(value=500)
w.title(clock_data['window_title'])

# 时间日期有关
def get_current_time():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
def get_time_with_correction(is_12_hrs:bool = False, show_seconds:bool = False):
    if is_12_hrs:
        format_str = '%I:%M:%S %p' if show_seconds else '%I:%M %p'
    else:
        format_str = '%H:%M:%S' if show_seconds else '%H:%M'
    return datetime.datetime.fromtimestamp(time.time() + clock_data['time_correction_seconds']).strftime(format_str)
def get_current_date(format_type:str = "%Y-%m-%d"):
    return datetime.datetime.fromtimestamp(time.time()).strftime(format_type)
def get_weekday(date=None, format_type="short"):
    """
    获取指定日期的星期几字符串
    参数:
    date: 可选，datetime.date对象，默认为当天
    format_type: 返回格式
        "short": 周一、周二等（默认）
        "long": 星期一、星期二等
        "english": Monday, Tuesday等
        "number": 0-6（周一=0，周日=6）
        “none": 不返回任何内容
    返回:
    星期几的字符串或数字
    """
    if date is None:
        date = datetime.date.today()
    # 星期几索引（0=周一, 6=周日）
    weekday_index = date.weekday()
    if format_type == "short":
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        return weekdays[weekday_index]
    elif format_type == "long":
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return weekdays[weekday_index]
    elif format_type == "english":
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"]
        return weekdays[weekday_index]
    elif format_type == "number":
        return weekday_index + 1
    elif format_type == "none":
        return ''
    else:
        raise ValueError("不支持的格式类型，请使用' short ', ' long ', ' english '或' number '")

# 弹出窗口
def time_correction():
    global clock_data
    clock_data['time_correction_seconds'] = time_correction_file.ask_time_correction(w,clock_data['time_correction_seconds'],use_12_hrs=use_12_hour_clock.get())

# 通用对话框
def ask_font_size(default_size:int= 20, title:str = '选择字号', prompt:str = '选择字体大小', max_font_size:int = 144) -> int:
    scale_font_size = tk.IntVar(value=default_size)
    font_size = None

    font_size_win=tk.Toplevel(w,padx=10,pady=10)
    font_size_win.title(title)
    tk.Label(font_size_win,text = prompt).pack()
    tk.Scale(font_size_win,showvalue=True, from_=12, to=max_font_size, resolution=2, orient=tk.HORIZONTAL, variable=scale_font_size).pack(side='top', fill='x', expand=True, padx=5)

    def on_ok():
        nonlocal font_size
        font_size = scale_font_size.get()
        font_size_win.destroy()
    def on_cancel():
        nonlocal font_size
        font_size = default_size
        font_size_win.destroy()

    button_frame = tk.Frame(font_size_win,padx=5)
    tk.Button(button_frame,text='确定',command=on_ok).pack(side='left', fill='x', expand=False,padx=5,pady=5,ipadx=20)
    tk.Button(button_frame,text='取消',command=on_cancel).pack(side='right', fill='x', expand=False,padx=5,pady=5,ipadx=20)
    button_frame.pack(side='bottom', fill='none', expand=False, pady=5)

    font_size_win.transient(w)
    font_size_win.resizable(1,0)
    font_size_win.grab_set()
    center_window(w, font_size_win)

    font_size_win.protocol('WM_DELETE_WINDOW', on_cancel)

    font_size_win.wait_window()
    return font_size

# 菜单触发的操作
def change_window_alpha():
    global clock_data
    #alpha 0-1 float
    alpha=widgets.ask_num.ask_number(w,'选择窗口透明度','使用下方滑块更改时钟主窗口的透明度(%)。','透明度',default=w.attributes('-alpha')*100,min_num=40,max_num=100)/100
    clock_data['alpha']=alpha
    w.attributes('-alpha',alpha)
def change_clock_font_size():
    global clock_data
    new_font_size = ask_font_size(clock_data['clock_font'][1],prompt='选择时间部分的字号')
    if new_font_size is not None:
        clock_data['clock_font'] = ('Consolas', new_font_size)
    font_size.set('Changed')
def change_date_font_size():
    global clock_data
    new_font_size = ask_font_size(clock_data['date_font'][1],prompt='选择日期部分的字号')
    if new_font_size is not None:
        clock_data['date_font'] = ('等线', new_font_size)
    font_size.set('Changed')
def change_string_reminder(menu:tk.Menu):
    # --no-changes-later
    words = ask_reminder_dialog(w, clock_string_reminder.get())
    if words is not None:
        if '--no-changes-later' in words:
            words = words.replace('--no-changes-later','')
            menu.entryconfig(7, state=tk.DISABLED)
            print('disabled')

        clock_string_reminder.set(words)
        clock_data['string_reminder'] = words

    if clock_string_reminder.get() == '':
        reminder_label.pack_forget()
    else:
        reminder_label.pack(anchor='center', fill='x', expand=True)
def change_reminder_size():
    new_size = ask_font_size(default_size=clock_data['reminder_font'][1],prompt='选择显示在时钟底部的静态文本的字号大小',max_font_size=48)
    clock_data['reminder_font']=('等线', new_size)
    reminder_label.config(font=clock_data['reminder_font'])
def change_window_title():
    global clock_data
    initial_value = w.title()
    if w.title() == default_clock_data['window_title']:
        initial_value='学者的时钟'
    new_title=tkinter.simpledialog.askstring(title='调整窗口标题',prompt='在下方输入框里输入新的窗口标题。',initialvalue=initial_value, parent=w)
    if new_title is not None:
        w.title(new_title)
        clock_data['window_title'] = new_title
def refresh_schedule_color(not_exist:bool=False):
    global schedule_label
    if not not_exist:
        clock_frame.pack_forget()
        schedule_label.destroy()
    schedule_label = schedule.get_current_schedule_frame(master=clock_bg_frame,weekday=get_weekday(format_type='english'),fg_color=clock_data['clock_fg_color'],bg_color=clock_data['clock_bg_color'],padx=15)
    if schedule_label is not None:
        schedule_label.pack(side='right', fill='none', expand=False, pady=5)
    clock_frame.pack(anchor='center',fill='x',expand=True)
def restart_application():
    """重启整个时钟程序"""
    if tk.messagebox.askyesno("重启确认", "重启会关闭当前窗口并重新启动程序。\n是否继续？"):
        w.quit()
        w.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)
def exec_python_command():
    code=tkinter.simpledialog.askstring('执行命令','输入命令以运行。此功能仅供调试使用。')
    if code is not None:
        try:
            exec(code)
        except Exception as e:
            tkinter.messagebox.showerror('出现错误',e)


# 配置文件操作
def delete_config():
    if tkinter.messagebox.askyesno('确认删除配置文件','即将删除配置文件。此操作不可逆。\n点击“是”继续。\n配置文件删除后，软件将退出。'):
        os.remove(CONFIG_FILE)
        on_closing()
def save_config_as():
    file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.json', filetypes=(('json files', '*.json'),('txt files', '*.txt'),('all files', '*.*')))
    if file is not None:
        clock_data.saveas(file)
        file.close()

# 后台操作
def config_window_mode(mode:int,view_menu:tk.Menu|None = None):
    # 0 normal
    # 1 top
    # 2 top and hide title
    # 3 fullscreen
    # 4 zoomed
    global  current_window_mode
    if mode != current_window_mode:
        current_window_mode = mode
        def reset_window_mode():
            w.attributes('-topmost', False)
            w.attributes('-fullscreen', False)
            w.state('normal')
            w.overrideredirect(False)
            w.resizable(0,0)
            if view_menu is not None:
                view_menu.entryconfig(7, state=tk.NORMAL)
        if mode == 0:
            reset_window_mode()
        elif mode == 1:
            reset_window_mode()
            w.attributes('-topmost', True)
        elif mode == 2:
            reset_window_mode()
            w.attributes('-topmost', True)
            w.overrideredirect(True)
            if view_menu is not None:
                view_menu.entryconfig(7, state=tk.DISABLED)
        elif mode == 3:
            reset_window_mode()
            w.attributes('-fullscreen', True)
        elif mode == 4:
            reset_window_mode()
            w.resizable(1,1)
            w.state('zoomed')
            w.overrideredirect(False)
        else:
            raise ValueError
        if mode == 3 or mode == 4:
            place_schedule_frame()
        else:
            remove_schedule_frame()
        window_mode.set(mode)
def config_font_sizes(in_time_label:tk.Label, in_date_label:tk.Label):
    if in_time_label['font'][1] != clock_data['clock_font'][1]:
        in_time_label.config(font=clock_data['clock_font'])
    if in_date_label['font'][1] != clock_data['date_font'][1]:
        in_date_label.config(font=clock_data['date_font'])
def config_clock_color(fg:str,bg:str):
    if clock_data['clock_fg_color'] != fg:
        clock_data['clock_fg_color'] = fg
        time_label.config(fg=clock_data['clock_fg_color'])
        date_label.config(fg=clock_data['clock_fg_color'])
        reminder_label.config(fg=clock_data['clock_fg_color'])
    if clock_data['clock_bg_color'] != bg:
        clock_data['clock_bg_color'] = bg
        clock_bg_frame.config(bg=clock_data['clock_bg_color'])
        time_label.config(bg=clock_data['clock_bg_color'])
        date_label.config(bg=clock_data['clock_bg_color'])
        reminder_label.config(bg=clock_data['clock_bg_color'])
        clock_frame.config(bg=clock_data['clock_bg_color'])
    if window_mode.get() == 3 or window_mode.get() == 4:
        refresh_schedule_color()


# 手动函数
def manual_change_clock_font_size(clock_font_size:int, date_font_size:int):
    global clock_data
    clock_data['clock_font'] = ('Consolas', clock_font_size)
    clock_data['date_font'] =  ('等线', date_font_size)

# 特殊
def on_close_button(action:tk.IntVar = window_close_action):
    # 0 exit
    # 1 min
    # 2 tray
    # 3 ask
    # 4 nothing

    clock_data['window_close_action'] = action.get()

    if action.get() == 0:
        on_closing()
    elif action.get() == 1:
        w.iconify()
    elif action.get() == 4:
        pass
    else:
        raise ValueError
def sync_close_action(action:int):
    global clock_data
    clock_data['window_close_action'] = action

def remove_schedule_frame():
    global schedule_label
    if schedule_label is not None:
        schedule_label.pack_forget()
def place_schedule_frame():
    global schedule_label
    if schedule_label is not None:
        clock_frame.pack_forget()
        schedule_label.pack(side='right', fill='none', expand=False, pady=5)
        clock_frame.pack(anchor='center', fill='x', expand=True)

# 工具
def show_random():
    randrom_generater.RandomWindow(w)

clock_bg_frame = tk.Frame(w, padx=15, pady=15, bg=clock_data['clock_bg_color'])
clock_frame = tk.Frame(clock_bg_frame, bg=clock_data['clock_bg_color'])
time_label = tk.Label(clock_frame, text="Time", font=clock_data['clock_font'], fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])
date_label = tk.Label(clock_frame, text="Date", font=clock_data['date_font'], fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])
reminder_label = tk.Label(clock_frame, text="Reminder", font=clock_data['reminder_font'], textvariable=clock_string_reminder, fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])

time_label.pack(anchor='center',fill='x',expand=True,pady=(0,5))
date_label.pack(anchor='center',fill='x',expand=True,pady=(0,5))
if clock_string_reminder.get() != '':
    reminder_label.pack(anchor='center', fill='x',expand=True)
refresh_schedule_color(True)
clock_frame.pack(anchor='center',fill='x',expand=True)
clock_bg_frame.pack(expand=True, anchor="center", fill='both')

def put_menu():
    global view_menu
    menu_bar = tk.Menu(w)
    w.config(menu=menu_bar)
    clock_menu = tk.Menu(menu_bar, tearoff=0)
    clock_menu.add_command(label='校正时间',command=time_correction)
    clock_menu.add_separator()
    clock_mode_menu = tk.Menu(clock_menu, tearoff=0)
    clock_mode_menu.add_checkbutton(label='使用12小时制', onvalue=True, offvalue=False, variable=use_12_hour_clock)
    clock_mode_menu.add_checkbutton(label='显示读秒', onvalue=True, offvalue=False, variable=show_seconds)
    clock_menu.add_cascade(label='时间格式设置', menu=clock_mode_menu)
    update_delay_menu = tk.Menu(clock_menu, tearoff=0)
    for i in update_delay_choices:
        update_delay_menu.add_radiobutton(label=str(i),variable=update_delay_ms, value=i)
    clock_menu.add_cascade(label='更新频率 (ms)', menu=update_delay_menu)
    date_mode_menu = tk.Menu(clock_menu, tearoff=0)
    for i in date_format_labels:
        date_mode_menu.add_radiobutton(label=i, variable=date_mode)
    date_mode_menu.add_radiobutton(label='不显示',variable=date_mode, value=' ')
    clock_menu.add_cascade(label='日期的表示方法', menu=date_mode_menu)
    week_mode_menu = tk.Menu(clock_menu, tearoff=0)
    week_mode_menu.add_radiobutton(label='短（周一）',variable=weekday_mode, value='short')
    week_mode_menu.add_radiobutton(label='长（星期一）',variable=weekday_mode, value='long')
    week_mode_menu.add_radiobutton(label='英语（Monday）',variable=weekday_mode, value='english')
    week_mode_menu.add_radiobutton(label='数字（1）',variable=weekday_mode, value='number')
    week_mode_menu.add_radiobutton(label='不显示',variable=weekday_mode, value='none')
    clock_menu.add_cascade(label='星期的表示方法', menu=week_mode_menu)
    clock_menu.add_separator()
    clock_menu.add_command(label='调整静态文本',command=lambda:change_string_reminder(clock_menu))
    clock_menu.add_command(label='调整窗口标题', command=change_window_title)
    clock_menu.add_separator()
    config_file_menu = tk.Menu(clock_menu, tearoff=0)
    config_file_menu.add_checkbutton(label='退出时保存设置', onvalue=True, offvalue=False, variable=save_config_before_exit)
    config_file_menu.add_command(label='立即保存配置文件',command=clock_data.save)
    config_file_menu.add_command(label='配置文件另存为', command=save_config_as)
    # config_file_menu.add_separator()
    # config_file_menu.add_command(label='删除配置文件', command=delete_config,activebackground='red')
    clock_menu.add_cascade(label='配置文件操作', menu=config_file_menu)
    clock_menu.add_command(label='退出',command=on_closing)
    menu_bar.add_cascade(label='时钟', menu=clock_menu)
    view_menu = tk.Menu(menu_bar, tearoff=0)
    # noinspection PyTypeChecker
    view_menu.add_radiobutton(label='普通窗口',variable=window_mode,value=0,command=lambda: config_window_mode(window_mode.get(),view_menu))
    view_menu.add_radiobutton(label='置顶窗口',variable=window_mode,value=1,command=lambda: config_window_mode(window_mode.get(),view_menu))
    view_menu.add_radiobutton(label='桌面挂件',variable=window_mode,value=2,command=lambda: config_window_mode(window_mode.get(),view_menu))
    view_menu.add_radiobutton(label='最大化窗口',variable=window_mode,value=4,command=lambda: config_window_mode(window_mode.get(),view_menu))
    view_menu.add_radiobutton(label='全屏模式',variable=window_mode,value=3,command=lambda: config_window_mode(window_mode.get(),view_menu))
    window_closing_menu = tk.Menu(view_menu, tearoff=0)
    window_closing_menu.add_radiobutton(label='退出软件',variable=window_close_action,value=0,command=lambda: sync_close_action(0))
    window_closing_menu.add_radiobutton(label='最小化窗口',variable=window_close_action,value=1,command=lambda: sync_close_action(1))
    window_closing_menu.add_radiobutton(label='最小化到托盘',variable=window_close_action,value=2,command=lambda: sync_close_action(2),state=tk.DISABLED)
    window_closing_menu.add_radiobutton(label='询问',variable=window_close_action,value=3,command=lambda: sync_close_action(3),state=tk.DISABLED)
    window_closing_menu.add_radiobutton(label='无操作',variable=window_close_action,value=4,command=lambda: sync_close_action(4))
    # window_closing_menu.add_separator()
    # window_closing_menu.add_checkbutton(label='禁止退出软件',variable=refuse_exit_action,onvalue=True,offvalue=False)
    view_menu.add_separator()
    view_menu.add_cascade(label='关闭按钮的功能',menu=window_closing_menu)
    view_menu.add_command(label='最小化窗口',command=w.iconify)
    font_size_menu = tk.Menu(view_menu, tearoff=0)
    for i in font_size_options:
        font_size_menu.add_radiobutton(label=i, variable=font_size, command=lambda: manual_change_clock_font_size(*map(int, font_size.get().split(' ')))
        )
    font_size_menu.add_separator()
    manual_font_size_settings_menu = tk.Menu(font_size_menu, tearoff=0)
    manual_font_size_settings_menu.add_command(label='时钟字号',command=change_clock_font_size)
    manual_font_size_settings_menu.add_command(label='日期、星期字号',command=change_date_font_size)
    font_size_menu.add_cascade(label='手动调整', menu=manual_font_size_settings_menu)
    font_size_menu.add_command(label='底部静态文本字号',command=change_reminder_size)
    clock_color_menu = tk.Menu(view_menu, tearoff=0)
    for i in clock_color_options:
        clock_color_menu.add_radiobutton(label=i, variable=clock_color, command=lambda:config_clock_color(*clock_color.get().split(' ')))
    view_menu.add_separator()
    view_menu.add_cascade(label='调整字号', menu=font_size_menu)
    view_menu.add_cascade(label='调整配色', menu=clock_color_menu)
    view_menu.add_command(label='调整窗口透明度', command=change_window_alpha)
    menu_bar.add_cascade(label='显示', menu=view_menu)
    schedule_menu = tk.Menu(menu_bar, tearoff=0)
    schedule_menu.add_radiobutton(label='最大化窗口',variable=window_mode,value=4,command=lambda: config_window_mode(window_mode.get(),view_menu))
    schedule_menu.add_command(label='显示课表',command=place_schedule_frame)
    schedule_menu.add_command(label='隐藏课表',command=remove_schedule_frame)
    schedule_menu.add_separator()
    schedule_menu.add_command(label='有关课表的帮助', command=lambda: tkinter.messagebox.showinfo('帮助信息',class_schedule.schedule_help_message))
    menu_bar.add_cascade(label='课表',menu=schedule_menu)
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label='随机数生成器',command=show_random,state=tk.DISABLED)
    menu_bar.add_cascade(label='工具', menu=tools_menu)
    help_menu=tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label='关于本软件', command=about.show_about)
    if DEBUG:
        help_menu.add_separator()
    troubleshoot_menu = tk.Menu(help_menu, tearoff=0)
    troubleshoot_menu.add_command(label='重置窗口大小',command= lambda: w.geometry(''))
    troubleshoot_menu.add_command(label='重启软件',command=restart_application)
    # troubleshoot_menu.add_command(label='重新加载配置文件',command=load_config)
    help_menu.add_cascade(label='故障排除', menu=troubleshoot_menu)
    if DEBUG:
        debug_menu = tk.Menu(help_menu, tearoff=0)
        debug_menu.add_command(label='运行命令',command=exec_python_command)
        help_menu.add_cascade(label='调试',menu=debug_menu)
    menu_bar.add_cascade(label='帮助', menu=help_menu)
    # menu_bar.add_command(label='关于', command=lambda:tkinter.messagebox.showinfo('关于本软件',about_text))
put_menu()

def refresh_clock_and_window():
    current_time = get_time_with_correction(use_12_hour_clock.get(),show_seconds.get())
    current_date = get_current_date(format_type=date_mode.get())
    weekday = get_weekday(format_type=weekday_mode.get())
    date_str = current_date + ' ' + str(weekday)

    # config_window_mode(window_mode.get(),view_menu)
    config_font_sizes(time_label,date_label)
    clock_data['use_12_hrs_clock']  = use_12_hour_clock.get()
    clock_data['show_seconds'] = show_seconds.get()

    time_label.config(text=current_time)
    date_label.config(text=date_str)

    w.after(update_delay_ms.get(),refresh_clock_and_window)

remove_schedule_frame()
refresh_clock_and_window()

w.protocol("WM_DELETE_WINDOW", lambda: on_close_button(window_close_action))

tk.mainloop()
