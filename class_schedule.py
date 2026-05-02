import tkinter as tk
import tkinter.messagebox
import typing

class ClassSchedule:
    def __init__(self,schedule:dict|None):
        self.schedule=schedule
        if self.schedule is not None:
            try:
                for key, value in self.schedule.items():
                    if not isinstance(key, str):
                        raise TypeError(f"dict key {key!r} is not str")
                    if not isinstance(value, list):
                        raise TypeError(f"value for key {key!r} is not list")
                    for item in value:
                        if not isinstance(item, str):
                            raise TypeError(f"list element {item!r} is not str")
            except TypeError as e:
                tkinter.messagebox.showerror('读取课表文件时出错','未被预期的json结果。检查文件内容后重试。'+str(e))
    def get_current_schedule(self,weekday:typing.Literal['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']) -> list|None :
        if self.schedule is None:
            return None
        if weekday in self.schedule.keys():
            return self.schedule[weekday]
        else:
            return None
    def get_current_schedule_frame(self, master:tk.Tk|tk.Toplevel|tk.Frame, weekday:typing.Literal['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], padx:int=5,pady:int=5,fg_color:str= '#000000', bg_color:str= '#F0F0F0', font:tuple[str,int]=('等线','18')) -> tk.Frame | None:
        listed_font = list(font)
        italic_font=tuple(list(font)+['italic'])
        bold_font=tuple(list(font)+['bold'])
        if self.schedule is None:
            return None
        current_schedule = self.get_current_schedule(weekday)
        if current_schedule:
            frame = tk.Frame(master=master, bg=bg_color)
            for i in current_schedule:
                current_font = font
                if '*' in i:
                    current_font=italic_font
                elif '^' in i:
                    current_font=bold_font
                t=i.replace('*','').replace('^','')
                tk.Label(frame, text=t, fg=fg_color, bg=bg_color, font=current_font,padx=padx,pady=pady).pack(side='top')
            return frame
        else:
            return None

schedule_help_message = '''课表功能帮助信息
 - 文件的格式
文件名为 class_schedule.json，在与程序同一文件夹下。
使用json格式，星期的英文名作为key，课程名称的列表作为value。

 - 字体样式
在课程名称前面添加*，应用斜体；
在课程名称前面添加^，应用粗体。

 - 无法正常读取
检查是否使用了中文引号、逗号。
 '''
