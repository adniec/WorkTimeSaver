import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime
from document import Document


class Gui(tk.Tk):

    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(0, 0)
        self.variables = {}
        self.form_gui()
        self.bind_keys()

    def form_gui(self):
        self.create_label('Fill the form to save your work day to file.', 0, 1)
        self.create_label('Date:', 1, 0)
        self.create_entry('date', 1, 1, datetime.now().strftime('%d.%m.%y'))
        self.create_label('From:', 2, 0)
        self.create_entry('start', 2, 1, '8:00')
        self.create_label('To:', 3, 0)
        self.create_entry('end', 3, 1, '16:30')
        tk.Button(self, text='Submit', width=6, command=self.submit).grid(row=4, column=1, pady=15, sticky='E')
        tk.Button(self, text='Exit', width=6, command=self.close).grid(row=4, column=2, pady=15, sticky='W')

    def submit(self, *_):
        dates = self.get_data()
        if dates:
            salary = Document(*dates).process_file()
            msg.showinfo('Success', f'Record added. In current month you have earned {salary} before tax. Keep going.')
            self.clear_form()

    def get_data(self):
        date = self.variables['date'].get()
        start_hour = self.variables['start'].get()
        end_hour = self.variables['end'].get()
        return self.convert_data(f'{date} {start_hour}', end_hour)

    def convert_data(self, start, end):
        try:
            start = datetime.strptime(start, '%d.%m.%y %H:%M')
            end = datetime.strptime(end, '%H:%M')
            return start, end
        except ValueError:
            msg.showerror('Error', 'Date and hour should be in correct format "dd.mm.yy", "hh:mm", e.g. 26.02.20 19:30')
            return False

    def clear_form(self):
        for variable in self.variables.values():
            variable.set('')

    def create_label(self, message, row, column):
        tk.Label(self, text=message, font='none 10').grid(row=row, column=column, padx=12, pady=2)

    def create_entry(self, name, row, column, default=''):
        content = tk.StringVar(self, value=default)
        tk.Entry(self, width=10, textvariable=content).grid(row=row, column=column, padx=10, pady=2, sticky='W')
        self.variables[name] = content

    def bind_keys(self):
        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)

    def close(self, *_):
        self.destroy()
        exit()
