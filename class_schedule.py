import tkinter as tk
import typing


class ClassSchedule:
    def __init__(self,schedule:dict):
        self.schedule=schedule
    def get_current_schedule(self,weekday:typing.Literal['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']) -> list|None :
        if weekday in self.schedule.keys():
            return self.schedule[weekday]
        else:
            return None
    def get_current_schedule_frame(self, master:tk.Tk|tk.Toplevel|tk.Frame, weekday:typing.Literal['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], padx:int=5,pady:int=5,fg_color:str= '#000000', bg_color:str= '#F0F0F0', font:tuple[str,int]=('等线','18')) -> tk.Frame | None:
        current_schedule = self.get_current_schedule(weekday)
        if current_schedule:
            frame = tk.Frame(master=master, bg=bg_color)
            for i in current_schedule:
                tk.Label(frame, text=i, fg=fg_color, bg=bg_color, font=font,padx=padx,pady=pady).pack(side='top')
            return frame
        else:
            return None



if __name__ == '__main__':
    schedule_dict = {
  "Monday": ["语文", "英语", "政治", "数学", "体活", "[音乐]", "物理", "班会", "辅导"],
  "Tuesday": ["语文", "数学", "英语", "阅表", "体育", "历史", "[美术]", "自习", "自习"],
  "Wednesday": ["英语", "物理", "体育", "生物", "数学", "数拓", "地理", "语文", "自习"],
  "Thursday": ["体育", "物理", "数学", "语文", "历史", "政治", "英听", "生物", "试官"],
  "Friday": ["英语", "数学", "物理", "语文", "地理", "政治", "体育", "自习", "辅导"]
}
    schedule_object = ClassSchedule(schedule_dict)
    print(schedule_object.get_current_schedule('Monday'))
    w = tk.Tk()
    schedule_object.get_current_schedule_frame(w,'Tuesday').pack(side='right')
    w.mainloop()
