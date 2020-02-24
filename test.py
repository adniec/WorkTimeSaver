import unittest
from WorkTimeSaver.salary import Salary
from WorkTimeSaver.document import Record, Document
from datetime import datetime
from os import remove


class TestSalary(unittest.TestCase):

    def test_days_add(self):
        salary = Salary()
        for _ in range(20):
            salary.update_work(480)
        self.assertEqual(salary.worktime, 9000)
        self.assertEqual(salary.days_at_work, 20)

    def test_salary_calculation(self):
        salary = Salary()
        data = (
            (6000, (25000, 0)),
            (9750, (40625, 0)),
            (9810, (40625, 375)),
            (12000, (40625, 14062.5)),
            (15750, (40625, 37500))
        )

        for minutes, money in data:
            salary.worktime = minutes
            result = salary.calculate_salary()
            self.assertEqual(result, money)

    def test_tax_deduction(self):
        salary = Salary()
        data = (
            ((25000, 0), 19250),
            ((40625, 0), 31281.25),
            ((40625, 375), 31525),
            ((40625, 37500), 55656.25)
        )

        for money, expected in data:
            result = salary.deduct_tax(money)
            self.assertEqual(result, expected)

    def test_output(self):
        salary = Salary()
        salary.days_at_work = 20
        salary.worktime = 9750
        output = "20\t\t\t\t162:30h\n\t\t\t\t40625.00NOK (16656.25PLN)\nAfter tax:\t\t\t31281.25NOK (12825.31PLN)\n\n" \
                 "------------------------------------------------------------------------------------\n"
        self.assertEqual(str(salary), output)
        salary.is_exchanged = False
        output = "20\t\t\t\t162:30h\n\t\t\t\t40625.00NOK\nAfter tax:\t\t\t31281.25NOK\n\n----------------------------" \
                 "--------------------------------------------------------\n"
        self.assertEqual(str(salary), output)


class TestHandler(unittest.TestCase):

    def test_new_record(self):
        start = datetime(2020, 2, 15, 8, 0)
        end = datetime.strptime('18:25', '%H:%M')
        record = Record(start, end)
        expected = '15.02\t\t08:00-18:25\t10:25h'
        self.assertEqual(str(record), expected)

    def test_new_document(self):
        start = datetime(2020, 2, 15, 8, 0)
        end = datetime.strptime('18:25', '%H:%M')
        document = Document(start, end)
        expected = '<Document "2020.txt" with new record <Work day 15.02 from 08:00 to 18:25 hour>>'
        self.assertEqual(str(document), expected)

    def test_insertions_sum(self):
        data = [
            ('01.08', '08:00', '18:00', '10:00h'),
            ('02.08', '08:00', '16:20', '08:20h'),
            ('03.08', '08:00', '16:20', '08:20h'),
            ('04.08', '08:00', '16:30', '08:30h'),
            ('07.08', '08:00', '18:00', '10:00h'),
            ('08.08', '08:00', '20:00', '12:00h'),
            ('09.08', '08:00', '21:00', '13:00h'),
            ('10.08', '08:00', '18:00', '10:00h'),
            ('11.08', '08:00', '18:25', '10:25h'),
            ('14.08', '08:00', '23:30', '15:30h'),
            ('15.08', '08:00', '23:30', '15:30h'),
            ('16.08', '07:00', '23:15', '16:15h'),
            ('17.08', '08:00', '21:15', '13:15h'),
            ('18.08', '08:00', '18:00', '10:00h'),
            ('19.08', '08:00', '20:30', '12:30h'),
            ('20.08', '08:00', '19:30', '11:30h'),
            ('21.08', '08:00', '21:00', '13:00h'),
            ('22.08', '07:40', '22:30', '14:50h'),
            ('23.08', '07:50', '23:40', '15:50h'),
            ('24.08', '08:50', '19:45', '10:55h'),
            ('25.08', '07:50', '16:00', '08:10h'),
            ('27.08', '08:00', '18:00', '10:00h'),
            ('28.08', '08:00', '16:30', '08:30h'),
            ('29.08', '08:00', '15:30', '07:30h'),
            ('30.08', '08:00', '19:10', '11:10h'),
            ('31.08', '08:00', '00:00', '16:00h')
        ]
        lines = []

        for record in data:
            lines.append(f'{record[0]}\t\t{record[1]}-{record[2]}\t{record[3]}\n')
            start = datetime.strptime(f'{record[0]}.19 {record[1]}', '%d.%m.%y %H:%M')
            end = datetime.strptime(record[2], '%H:%M')
            document = Document(start, end)
            document.process_file()

        lines.extend((
            '26\t\t\t\t288:00h\n',
            '\t\t\t\t87687.50NOK (35951.88PLN)\n',
            'After tax:\t\t\t61871.88NOK (25367.47PLN)\n',
            '\n',
            '------------------------------------------------------------------------------------\n',
            '\n',
            '01.09\t\t08:00-18:25\t10:25h\n',
        ))

        start = datetime(2019, 9, 1, 8, 0)
        end = datetime.strptime('18:25', '%H:%M')
        document = Document(start, end)
        document.process_file()

        with open('2019.txt', 'r') as f:
            content = f.readlines()
        remove('2019.txt')
        self.assertEqual(content, lines)


if __name__ == '__main__':
    unittest.main()
