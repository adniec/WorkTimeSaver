"""Document Module

It includes methods mandatory to process text file and extend it with provided information about new record. Processing
file starts with going through its lines backwards. Work time is collected from next records as long as they are in
correct form or separator is met. Data are stored in Salary object. When month from last record is different than this
passed in date then summarization is added to file.

Modules used are: `datetime`, `re` and `salary`. It is required to provide them before running application.

It contains classes:

    * Record - formats string with new record according to set date.
    * Document - process text file and extends it with new record or summarization.

License:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import timedelta
import re
from WorkTimeSaver.salary import Salary


class Record:
    """
    A class representing new record.

    ...

    Attributes
    ----------
    date : str
        information about day and month of record in format dd.mm
    start : datetime.timedelta
        object storing beginning of work hour
    end : datetime.timedelta
        object storing end of work hour


    Methods
    -------
    __str__()
        returns string representing record
    get_hour(hour)
        returns string with hour (hh:mm) from timedelta object
    """

    def __init__(self, date, end_time):
        """
        Parameters
        ----------
        date : datetime.datetime
            datetime object with information about record date and hour - beginning of work
        end_time : datetime.datetime
            datetime object with hour - end of work
        """

        self.date = date.strftime('%d.%m')
        self.start = timedelta(hours=date.hour, minutes=date.minute)
        self.end = timedelta(hours=end_time.hour, minutes=end_time.minute)

    def __repr__(self):
        return f'<Work day {self.date} from {self.get_hour(self.start)} to {self.get_hour(self.end)} hour>'

    def __str__(self):
        return f'{self.date}\t\t{self.get_hour(self.start)}-{self.get_hour(self.end)}\t' \
            f'{self.get_hour(self.end - self.start)}h'

    def get_hour(self, hour):
        """Returns string with formated hour (hh:mm) from datetime.timedelta"""

        return f'{hour.seconds // 3600:02}:{hour.seconds // 60 % 60:02}'


class Document:
    """
    A class containing methods needed to process txt document.

    ...

    Attributes
    ----------
    document : str
        name (passed year in date and txt extension) of document where record will be stored
    month : int
        new record month number
    record : document.Record
        object storing data about new record
    salary : salary.Salary
        object responsible for salary calculation

    Methods
    -------
    process_file()
        sum time from records in file, adds new record (and summarization when criteria are met), returns salary
    sum_month(lines)
        updates Salary object with minutes from passed records in list
    get_info(pattern, line)
        according to passed pattern search information in line and returns it
    get_minutes(line)
        returns number of minutes at work stored in passed record
    get_month(line)
        returns month number from line
    get_lines()
        collects lines from file and return them reversed
    save_data(data)
        appends file with data
    """

    def __init__(self, date, end_time):
        """
        Parameters
        ----------
        date : datetime.datetime
            datetime object with information about record date and hour - beginning of work
        end_time : datetime.datetime
            datetime object with hour - end of work
        """

        self.document = str(date.year) + '.txt'
        self.month = date.month
        self.record = Record(date, end_time)
        self.salary = Salary()

    def __repr__(self):
        return f'<Document "{self.document}" with new record {self.record.__repr__()}>'

    def process_file(self):
        """Operates on file

        Gets file lines or False when it doesn't exists. Then iterates through them backward summing time as long as
        separator is met. When record from last file line is different than this stored in month attribute it saves
        summarization and replaces Salary object with new one (blank). It appends file with new record.

        Returns
        -------
        str
            salary before tax with its currency from lines summed up
        """

        lines = self.get_lines()
        if lines:
            self.sum_month(lines)
            month = self.get_month(list(self.get_lines())[0])
            if month != self.month:
                self.save_data(self.salary)
                self.salary = Salary()
        self.save_data(self.record)
        self.sum_month([str(self.record)])
        return f'{sum(self.salary.calculate_salary()):.2f}{self.salary.get_currency()}'

    def sum_month(self, lines):
        """Updates Salary object with time from list of file records as long as they contain proper values

        Parameters
        ----------
        lines : list
            a list with reversed records loaded from file
        """

        for line in lines:
            time = self.get_minutes(line)
            if not time:
                break
            self.salary.update_work(time)

    def get_info(self, pattern, line):
        """Receives information from line according to set pattern

        Parameters
        ----------
        pattern : str
            structure of needed information
        line : str
            file line where information will be searched for

        Returns
        -------
        str
            information corresponding to pattern
        False
            when information wasn't found
        """

        try:
            return re.search(pattern, line).group(1)
        except AttributeError:
            return False

    def get_minutes(self, line):
        """Receives number of minutes from file line

        Parameters
        ----------
        line : str
            file line where information about time will be searched for

        Returns
        -------
        int
            number of minutes spent at work from file record
        False
            when time wasn't found in passed line
        """

        result = self.get_info("\t(..:..)h", line)
        if result:
            time = result.split(":")
            return int(time[0]) * 60 + int(time[1])
        return False

    def get_month(self, line):
        """Receives number of month from file line

        Parameters
        ----------
        line : str
            file line where information about month will be searched for

        Returns
        -------
        int
            number of month from file record
        0
            when month wasn't found in passed line
        """

        result = self.get_info(".(..)\t", line)
        if result:
            return int(result)
        return 0

    def get_lines(self):
        """Collects lines from file

        Returns
        -------
        list
            a list with reversed file lines
        False
            when file doesn't exists
        """

        try:
            with open(self.document, 'r') as f:
                return reversed(f.readlines())
        except FileNotFoundError:
            return False

    def save_data(self, data):
        """Appends file with new information

        Parameters
        ----------
        data : object
            object (Record or Salary) with __str__ method allowing to print information to file
        """

        with open(self.document, 'a+') as f:
            print(data, file=f)
