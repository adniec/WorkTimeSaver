"""Salary Module

Module responsible for storing time spent by employee at work in current month. According to this time and basic
information included, e.g. hourly rate, overtime, currency, exchange rate calculation of salary is performed. It deducts
unpaid food breaks from total time and taxes from final amount. It also covers method needed for month summary which
will be logged to file.

License:
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class Salary:
    """
    A class with methods needed to perform calculation of salary in current month.

    ...

    Attributes
    ----------
    rate : int
        money earned per hour
    currency : str
        name of salary currency
    is_exchanged : bool
        True if salary should be exchanged to another currency and saved to file otherwise False
    worktime : int
        number of minutes spent at work in current month
    days_at_work : int
        number of days spent at work in current month

    Methods
    -------
    sum_up()
        returns string with summarization of month - days, hours, salary (exchanged) with and without tax
    calculate_salary()
        returns tuple with salary on normal rate and overtime rate
    update_work(minutes)
        adds passed minutes (deducted free break) to worktime attribute and increase number of days_at_work
    deduct_tax(salary)
        from passed tuple with salary deduct tax for normal rate and extra hours then returns total earning
    exchange_currency(amount)
        multiplies set amount by currency rate and returns it in string with its name
    get_currency()
        returns string with currency of salary
    """

    def __init__(self):
        """Covers crucial data needed for salary calculation."""

        self.rate = 250
        self.currency = 'NOK'
        self.is_exchanged = True
        self.worktime = 0
        self.days_at_work = 0

    def __repr__(self):
        return f'<Salary {self.rate}{self.currency} per hour. Worktime {self.worktime} minutes>'

    def __str__(self):
        return self.sum_up() + \
               '\n------------------------------------------------------------------------------------\n'

    def sum_up(self):
        """Summarize month

        Returns
        -------
        str
            a string with information about days spent at work, number of hours, salary before tax and salary after
            tax. It also includes exchanged currency values when is_exchanged attribute is set to True.
        """

        salary = self.calculate_salary()
        deducted = self.deduct_tax(salary)
        e1, e2 = '', ''
        if self.is_exchanged:
            e1 = f' ({self.exchange_currency(sum(salary))})'
            e2 = f' ({self.exchange_currency(deducted)})'
        return f'{self.days_at_work}\t\t\t\t{self.worktime // 60}:{self.worktime % 60:02}h\n\t\t\t\t{sum(salary):.2f}' \
            f'{self.currency}{e1}\nAfter tax:\t\t\t{deducted:.2f}{self.currency}{e2}\n'

    def calculate_salary(self):
        """Calculates salary according to set monthly hour limit on normal rate and bonus multiplier

        Returns
        -------
        tuple
            a tuple with salary on normal rate and extra hours rate
        """

        hours = self.worktime / 60
        overtime = 162.5
        bonus_percent = 1.5
        extra = 0
        if hours > overtime:
            extra = hours - overtime
            hours -= extra
        return (hours * self.rate, extra * self.rate * bonus_percent)

    def update_work(self, minutes):
        """Updates worktime with minutes deducted by free break according to set conditions, increases days_at_work

        Parameters
        ----------
        minutes : int
            number of minutes spent at work in one day
        """

        unpaid_break = 30
        break_after = 240
        if minutes > break_after:
            minutes -= unpaid_break
        self.worktime += minutes
        self.days_at_work += 1

    def deduct_tax(self, salary):
        """Deducts standard and extra tax from given salary

        Parameters
        ----------
        salary : tuple
            a tuple with salary on normal rate and extra hours rate

        Returns
        -------
        int
            total salary after tax deduction
        """

        standard = 0.23
        overtime = 0.35
        return salary[0] * (1 - standard) + salary[1] * (1 - overtime)

    def exchange_currency(self, amount):
        """Exchanges salary to set currency

        Parameters
        ----------
        amount : int
            total salary which will be exchanged

        Returns
        -------
        str
            salary multiplied by exchange currency rate with currency name
        """

        rate = 0.41
        currency = 'PLN'
        return f'{amount * rate:.2f}{currency}'

    def get_currency(self):
        """Returns string with currency of salary"""

        return self.currency
