import unittest
import WorkTimeSaver.salary as s


class TestSalary(unittest.TestCase):

    def test_days_add(self):
        salary = s.Salary()
        for _ in range(20):
            salary.update_work(480)
        self.assertEqual(salary.worktime, 9000)
        self.assertEqual(salary.days_at_work, 20)

    def test_salary_calculation(self):
        salary = s.Salary()
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
        salary = s.Salary()
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
        salary = s.Salary()
        salary.days_at_work = 20
        salary.worktime = 9750
        output = "20\t\t\t\t162:30h\n\t\t\t\t40625.00NOK (16656.25PLN)\nAfter tax:\t\t\t31281.25NOK (12825.31PLN)\n\n" \
                 "------------------------------------------------------------------------------------\n"
        self.assertEqual(str(salary), output)
        salary.is_exchanged = False
        output = "20\t\t\t\t162:30h\n\t\t\t\t40625.00NOK\nAfter tax:\t\t\t31281.25NOK\n\n----------------------------" \
                 "--------------------------------------------------------\n"
        self.assertEqual(str(salary), output)


if __name__ == '__main__':
    unittest.main()
