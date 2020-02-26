"""GUI

Module creates graphical user interface. It displays fields for data which are necessary to be collected. It also
provides default values for typical day at work: current date with hours 8:00 - 16:30. It is responsible for integration
document module with proper button, binding keys to methods (ENTER - save data to file, ESC - close application) and
displaying message in case of error.

Modules used are: `datetime`, `sys`, `tkinter`, `tkinter.messagebox` and `Document`. It is required to provide them
before running application.

License:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import tkinter as tk
import tkinter.messagebox as msg
from datetime import datetime
from WorkTimeSaver.document import Document
import sys


class Gui(tk.Tk):
    """
    A class containing methods used to create GUI and make interactions between its elements. It is child of tkinter.Tk
    class.

    ...

    Attributes
    ----------
    variables : dict
        a dictionary storing variables from tkinter entry fields (needed to obtain data when submitted)

    Methods
    -------
    form_gui()
        uses class methods to shape GUI
    submit()
        processes entered data
    get_data()
        loads data from entries and returns them in proper form
    convert_data(start, end)
        converts strings with date and hour to datetime objects
    clear_form()
        clears all application entries
    create_label(message, row, column)
        creates label with passed text and binds it to GUI in set location (row, column)
    create_entry(name, row, column, default='')
        creates entry field with default value and binds it to GUI in set location (row, column)
    bind_keys()
        binds ENTER key to submit method and ESC to close
    close()
        shutdowns application
    """

    def __init__(self, title, size):
        """Sets basic settings for GUI, creates it and binds keys to submit, close methods

        Parameters
        ----------
        title : str
            name of application displayed on bar
        size : str
            size of application window in form 'widthxheight'
        """

        super().__init__()
        self.title(title)
        self.geometry(size)
        self.resizable(0, 0)
        self.variables = {}
        self.form_gui()
        self.bind_keys()

    def form_gui(self):
        """Uses class methods to shape GUI"""

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
        """Submits entered data

        Loads and processes data from entries then adds new record to file if they are correct. Proper message is
        displayed and form cleared. *_ to ignore unused argument from ENTER key bind.
        """

        dates = self.get_data()
        if dates:
            salary = Document(*dates).process_file()
            msg.showinfo('Success', f'Record added. In current month you have earned {salary} before tax. Keep going.')
            self.clear_form()

    def get_data(self):
        """Gets data from entries and returns them in proper format

        Returns
        -------
        tuple
            two elements tuple with datetime objects representing beginning and end of work
        False
            when passed data were incorrect
        """

        date = self.variables['date'].get()
        start_hour = self.variables['start'].get()
        end_hour = self.variables['end'].get()
        return self.convert_data(f'{date} {start_hour}', end_hour)

    def convert_data(self, start, end):
        """Converts strings with date, time to datetime objects. In case of error message is displayed.

        Parameters
        ----------
        start : str
            beginning of work - string with date and hour (expected format '%d.%m.%y %H:%M')
        end : str
            end of work hour (expected format '%H:%M')

        Returns
        -------
        tuple
            two elements tuple with datetime objects representing beginning and end of work
        False
            when passed data were incorrect
        """

        try:
            start = datetime.strptime(start, '%d.%m.%y %H:%M')
            end = datetime.strptime(end, '%H:%M')
            return start, end
        except ValueError:
            msg.showerror('Error', 'Date and hour should be in correct format "dd.mm.yy", "hh:mm", e.g. 26.02.20 19:30')
            return False

    def clear_form(self):
        """Clears all application entries by setting variables values to '' """

        for variable in self.variables.values():
            variable.set('')

    def create_label(self, message, row, column):
        """Creates label with passed text and binds it to GUI in set location (row, column)

        Parameters
        ----------
        message : str
            text which will be displayed
        row : int
            row location for Tkinter Grid Manager specifies where label will be displayed
        column : int
            column location for Tkinter Grid Manager specifies where label will be displayed
        """

        tk.Label(self, text=message, font='none 10').grid(row=row, column=column, padx=12, pady=2)

    def create_entry(self, name, row, column, default=''):
        """Creates entry field

        Sets for it default value and binds it to GUI in set location (row, column) then populate variables dictionary
        with entry name and corresponding variable (tkinter.StringVar)

        Parameters
        ----------
        name : str
            name of entry - text added to variables dictionary as key
        row : int
            row location for Tkinter Grid Manager specifies where entry will be displayed
        column : int
            column location for Tkinter Grid Manager specifies where entry will be displayed
        default : str, optional
            text value displayed in entry (default is '')
        """

        content = tk.StringVar(self, value=default)
        tk.Entry(self, width=10, textvariable=content).grid(row=row, column=column, padx=10, pady=2, sticky='W')
        self.variables[name] = content

    def bind_keys(self):
        """Binds ENTER key to submit method and ESC to close"""

        self.bind('<Return>', self.submit)
        self.bind('<Escape>', self.close)

    def close(self, *_):
        """Shutdowns application, *_ to ignore unused argument from ESC key bind"""

        self.destroy()
        sys.exit()
