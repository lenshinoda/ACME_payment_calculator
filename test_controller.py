import unittest
import controller as ct
from model import hours, cost


class Test_Controller(unittest.TestCase):

    def test_time_range_controller(self):
        self.assertEqual(ct.time_range_controller('00:00-09:00'), [0, 9])
        self.assertEqual(ct.time_range_controller('9:00-14:00'), [9, 14])
        self.assertEqual(ct.time_range_controller('12:00-24:00'), [12, 24])
        with self.assertRaises(SystemExit):
            ct.time_range_controller('20:00-25:00')

    def test_time_intersection(self):
        self.assertEqual(ct.time_intersection([0, 9], [8, 9]), 1)
        self.assertEqual(ct.time_intersection([10, 12], [12, 19]), 0)
        self.assertEqual(ct.time_intersection([18, 24], [10, 20]), 2)

    def test_get_amount_pay_per_day(self):
        hours_cost = {
            cost[i]: ct.time_range_controller(hours[i]) for i in range(len(cost))
        }

        self.assertEqual(
            ct.get_amount_pay_per_day('MO', '00:00-24:00', hours_cost),
            480
        )
        self.assertEqual(
            ct.get_amount_pay_per_day('SA', '00:00-10:00', hours_cost),
            290
        )
        self.assertEqual(
            ct.get_amount_pay_per_day('SU', '00:00-24:00', hours_cost),
            600
        )

    def test_get_total(self):
        hours_cost = {
            cost[i]: ct.time_range_controller(hours[i]) for i in range(len(cost))
        }
        rene = 'RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00'
        astrid = 'ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00'
        self.assertEqual(ct.get_total(rene, hours_cost), ('RENE', 215))
        self.assertEqual(ct.get_total(astrid, hours_cost), ('ASTRID', 85))


if __name__ == '__main__':
    unittest.main()
