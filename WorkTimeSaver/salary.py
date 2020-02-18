class Salary:
    def __init__(self):
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
        salary = self.calculate_salary()
        deducted = self.deduct_tax(salary)
        e1, e2 = '', ''
        if self.is_exchanged:
            e1 = f' ({self.exchange_currency(sum(salary))})'
            e2 = f' ({self.exchange_currency(deducted)})'
        return f'{self.days_at_work}\t\t\t\t{self.worktime // 60}:{self.worktime % 60:02}h\n\t\t\t\t{sum(salary):.2f}' \
            f'{self.currency}{e1}\nAfter tax:\t\t\t{deducted:.2f}{self.currency}{e2}\n'

    def calculate_salary(self):
        hours = self.worktime / 60
        overtime = 162.5
        bonus_percent = 1.5
        extra = 0
        if hours > overtime:
            extra = hours - overtime
            hours -= extra
        return (hours * self.rate, extra * self.rate * bonus_percent)

    def update_work(self, minutes):
        unpaid_break = 30
        break_after = 240
        if minutes > break_after:
            minutes -= unpaid_break
        self.worktime += minutes
        self.days_at_work += 1

    def deduct_tax(self, salary):
        standard = 0.23
        overtime = 0.35
        return salary[0] * (1 - standard) + salary[1] * (1 - overtime)

    def exchange_currency(self, amount):
        rate = 0.41
        currency = 'PLN'
        return f'{amount * rate:.2f}{currency}'

    def get_currency(self):
        return self.currency
