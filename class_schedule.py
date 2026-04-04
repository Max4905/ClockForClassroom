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
    schedule_dict = {'Monday':['a','b','c']}
    schedule_object = ClassSchedule(schedule_dict)
    print(schedule_object.get_current_schedule('Monday'))
    w = tk.Tk()
    schedule_object.get_current_schedule_frame(w,'Monday').pack(side='right')
    w.mainloop()
