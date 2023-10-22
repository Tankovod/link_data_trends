import tkinter
from datetime import datetime, timedelta
from tkinter.constants import BOTH

from src.panda import pd_view_data
from math import ceil
from src.database_func import pg_select_trends
from main import read_hosts_file
from src.types_.settings import LIMITER
from tkinter import messagebox, ttk

root = tkinter.Tk()
root.title('Связь с объектами (тренды)')


class ButtonObject:
    btn_s = []

    def __init__(self, text, height, width, padx, column, row):
        self.text: str
        self.height: int
        self.width: int
        self.padx: int
        self.column: int
        self.row: int


class ButtonSelect(ButtonObject):
    def __init__(self, text, height, width, padx, column, row):
        super().__init__(text, height, width, padx, column, row)

        self.button = tkinter.Button(text=text, height=height, width=width, padx=padx, command=self.change_bt_color,
                                     background='white')
        self.button.grid(column=column, row=row)

    def change_bt_color(self):
        if self.button.cget('background') == 'white':
            self.button.configure(background='green')
        else:
            self.button.configure(background='white')


class ShowTrends(ButtonObject):
    tkinter.Label(text='Период трендов, с').grid(column=LIMITER + 2, row=0)
    tkinter.Label(text='Период трендов, по').grid(column=LIMITER + 2, row=2)
    datetime_from = tkinter.Entry()
    datetime_from.grid(column=LIMITER + 2, row=1)
    datetime_from.insert(0, (datetime.now() - timedelta(days=3)).strftime('%d.%m.%Y|%H:%M'))
    datetime_to = tkinter.Entry()
    datetime_to.grid(column=LIMITER + 2, row=3)
    datetime_to.insert(0, datetime.now().strftime('%d.%m.%Y|%H:%M'))

    def __init__(self, text, height, width, padx, column, row):
        super().__init__(text, height, width, padx, column, row)
        self.button = tkinter.Button(text=text, height=height, width=width, padx=padx, command=self.show_pd_trends,
                                     background='white')
        self.button.grid(column=column, row=row)

    def show_pd_trends(self):
        def split_strftime(dt):
            d_t, lst = dt.get().strip().split('|'), []
            d = d_t[0].split('.')
            t = d_t[1].split(':')
            try:
                lst = [*map(lambda x: int(x), d + t)]
            except ValueError:
                messagebox.showinfo(message='Проверьте правильность введенных даты и времени')
            return lst

        dt_from = split_strftime(self.datetime_from)
        dt_to = split_strftime(self.datetime_to)

        trends = pg_select_trends(to_time=datetime(year=dt_to[2], month=dt_to[1], day=dt_to[0], hour=dt_to[3], minute=dt_to[4]),
                                  from_time=datetime(year=dt_from[2], month=dt_from[1], day=dt_from[0], hour=dt_from[3], minute=dt_from[4]),
                              object_trend_names=[i.button.cget('text') for i in self.btn_s if i.button.cget('background') == 'green'])

        data = [{'dt': i[2], 'name': i[1], 'ping': i[0]} for i in trends]
        pd_view_data(data)

# root.attributes('-alpha', 0.75)


objs = sorted(read_hosts_file('h.txt'), key=lambda x: x[1])
button_width, button_height = 13, 1
height = ceil(len(objs) / LIMITER)

objects_btn = []
for column in range(LIMITER):
    for num, obj in enumerate(objs[height * column:height * (column + 1)]):
        objects_btn.append(ButtonSelect(text=obj[1], height=button_height, width=button_width, padx=1, column=column, row=num))

ButtonObject.btn_s = objects_btn
ShowTrends(text='Показать тренды', height=button_height, width=button_width, padx=1, column=LIMITER + 2, row=4)

root.geometry(f'{button_width * LIMITER * 8 + button_width * 7}x{height * button_height * 26}+50+50')
root.wm_minsize(height=height * button_height * 26, width=button_width * LIMITER * 8 + button_width * 7)
root.mainloop()
