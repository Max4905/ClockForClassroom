import datetime
import json
import os
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.simpledialog

import about
import randrom_generater
import time_correction as time_correction_file
from ask_reminder import ask_reminder_dialog
from class_schedule import ClassSchedule
from window_tools import center_window

w = tk.Tk()
w.title("时钟")
w.resizable(0,0)

about_text ='''Clock For Classroom v1.2
正式版 总计第7次更新

关于开发者
黄天敬泽
Max490545149@outlook.com

2026-03-15
'''

encouraging_words = ["学习不是填充空桶，而是点燃火焰。",
                     "拥有液泡的力量，胜利是必然的！",
                     "拥有液泡的力量，胜利是必然的！",
                     "这是计划的一部分。",
                     "专注当下，让每一分钟的学习都产生价值。",
                     "学习如同登山，过程或许艰难，但山顶的风景值得一切。",
                     "今天的汗水，浇灌明天的果实。",
                     "给岁月以文明，而不是给文明以岁月。",
                     "只送大脑。",
                     "弱小和无知不是生存的障碍，傲慢才是。",
                     "弱小和无知不是生存的障碍，傲慢才是。",
                     "前进，不择手段地前进！",
                     "快跑。傻孩子们，快跑啊——",
                     "藏好自己，做好清理。",
                     "\"自然选择\"号，前进四！"]

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

def validate_config(config):
    """验证配置是否合法，返回 (是否合法, 错误信息)"""
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
    for key, expected_type in required_keys.items():
        if key not in config:
            return False, f"缺少必要键: {key}"
        value = config[key]
        if not isinstance(value, expected_type):
            return False, f"键 {key} 的类型应为 {expected_type}，实际为 {type(value)}"
        # 对于字体元组，进一步检查长度和元素类型
        if key.endswith('_font'):
            if len(value) != 2:
                return False, f"字体配置 {key} 应为长度为2的序列，实际长度为 {len(value)}"
            if not isinstance(value[1], int):
                return False, f"字体大小必须为整数，但 {key}[1] 是 {type(value[1])}"
    return True, "校验通过"


CONFIG_FILE = 'clock.json'
clock_data = default_clock_data.copy()  # 先设为默认值

def load_config():
    global clock_data
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        # 校验配置
        is_valid, message = validate_config(loaded_data)
        if is_valid:
            clock_data = {**default_clock_data, **loaded_data}  # 合并，缺失项用默认值
            print("配置文件加载成功")
        else:
            tkinter.messagebox.showwarning("配置文件加载时出错",f"配置文件校验失败: {message}，将删除并重置")
            os.remove(CONFIG_FILE)  # 删除损坏的配置文件
            # 保持 clock_data 为默认值
    except FileNotFoundError:
        tkinter.messagebox.showinfo("无配置文件","配置文件不存在，使用默认配置")
        # 保持 clock_data 为默认值
    except (json.JSONDecodeError, OSError) as e:
        tkinter.messagebox.showwarning("配置文件加载时出错",f"读取配置文件时出错: {e}，将删除并重置")
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        # 保持 clock_data 为默认值
load_config()

def read_class_schedule():
    with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
        global schedule
        loaded_data = json.load(f)
        schedule = ClassSchedule(loaded_data)

read_class_schedule()

# 最后将当前配置写入文件（可选，如果希望立即生成默认配置文件）
def save_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(clock_data, f, indent=4, ensure_ascii=False)
save_config()

window_is_open = True
def on_closing():
    global window_is_open
    window_is_open = False
    if save_config_before_exit.get():
        with open('./clock.json', 'w', encoding='utf-8') as f:
            json.dump(clock_data, f, indent=4, ensure_ascii=False)
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

# 菜单触发的非窗口操作
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
            menu.entryconfig(6, state=tk.DISABLED)
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

# 配置文件操作
def delete_config():
    if tkinter.messagebox.askyesno('确认删除配置文件','即将删除配置文件。此操作不可逆。\n点击“是”继续。\n配置文件删除后，软件将退出。'):
        os.remove(CONFIG_FILE)
        on_closing()
def save_config_as():
    file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.json', filetypes=(('json files', '*.json'),('txt files', '*.txt'),('all files', '*.*')))
    if file is not None:
        json.dump(clock_data, file, indent=4, ensure_ascii=False)
        file.close()

# 后台操作
def config_window_mode(mode:int,view_menu:tk.Menu):
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
            view_menu.entryconfig(7,state=tk.DISABLED)
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

# 工具
def show_random():
    randrom_generater.RandomWindow(w)

clock_bg_frame = tk.Frame(w, padx=15, pady=15, bg=clock_data['clock_bg_color'])
clock_frame = tk.Frame(clock_bg_frame, bg=clock_data['clock_bg_color'])
time_label = tk.Label(clock_frame, text="Time", font=clock_data['clock_font'], fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])
date_label = tk.Label(clock_frame, text="Date", font=clock_data['date_font'], fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])
reminder_label = tk.Label(clock_frame, text="Reminder", font=clock_data['reminder_font'], textvariable=clock_string_reminder, fg=clock_data['clock_fg_color'], bg=clock_data['clock_bg_color'])
schedule_label = schedule.get_current_schedule_frame(master=clock_frame,weekday=get_weekday(format_type='english'))
# reminder_label=tk.Label()
time_label.pack(anchor='center',fill='x',expand=True,pady=(0,5))
date_label.pack(anchor='center',fill='x',expand=True,pady=(0,5))
schedule_label.pack(anchor='center',fill='x',expand=True,pady=(0,5))
if clock_string_reminder.get() != '':
    reminder_label.pack(anchor='center', fill='x',expand=True)
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
    config_file_menu.add_command(label='立即保存配置文件',command=save_config)
    config_file_menu.add_command(label='配置文件另存为', command=save_config_as)
    # config_file_menu.add_separator()
    # config_file_menu.add_command(label='删除配置文件', command=delete_config,activebackground='red')
    clock_menu.add_cascade(label='配置文件操作', menu=config_file_menu)
    clock_menu.add_command(label='退出',command=on_closing)
    menu_bar.add_cascade(label='时钟', menu=clock_menu)
    view_menu = tk.Menu(menu_bar, tearoff=0)
    # noinspection PyTypeChecker
    view_menu.add_radiobutton(label='普通窗口',variable=window_mode,value=0)
    view_menu.add_radiobutton(label='置顶窗口',variable=window_mode,value=1)
    view_menu.add_radiobutton(label='桌面挂件',variable=window_mode,value=2)
    view_menu.add_radiobutton(label='最大化窗口',variable=window_mode,value=4)
    view_menu.add_radiobutton(label='全屏模式',variable=window_mode,value=3)
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
    menu_bar.add_cascade(label='显示', menu=view_menu)
    tools_menu = tk.Menu(menu_bar, tearoff=0)
    tools_menu.add_command(label='随机数生成器',command=show_random)
    menu_bar.add_cascade(label='工具', menu=tools_menu)
    help_menu=tk.Menu(menu_bar, tearoff=0)
    help_menu.add_command(label='关于本软件', command=about.show_about)
    troubleshoot_menu = tk.Menu(help_menu, tearoff=0)
    troubleshoot_menu.add_command(label='重置窗口大小',command= lambda: w.geometry(''))
    # troubleshoot_menu.add_command(label='重新加载配置文件',command=load_config)
    help_menu.add_cascade(label='故障排除', menu=troubleshoot_menu)
    menu_bar.add_cascade(label='帮助', menu=help_menu)
    # menu_bar.add_command(label='关于', command=lambda:tkinter.messagebox.showinfo('关于本软件',about_text))
put_menu()

def refresh_clock_and_window():
    current_time = get_time_with_correction(use_12_hour_clock.get(),show_seconds.get())
    current_date = get_current_date(format_type=date_mode.get())
    weekday = get_weekday(format_type=weekday_mode.get())
    date_str = current_date + ' ' + str(weekday)

    config_window_mode(window_mode.get(),view_menu)
    config_font_sizes(time_label,date_label)
    clock_data['use_12_hrs_clock']  = use_12_hour_clock.get()
    clock_data['show_seconds'] = show_seconds.get()

    time_label.config(text=current_time)
    date_label.config(text=date_str)

    w.after(update_delay_ms.get(),refresh_clock_and_window)

refresh_clock_and_window()

w.protocol("WM_DELETE_WINDOW", lambda: on_close_button(window_close_action))

tk.mainloop()
