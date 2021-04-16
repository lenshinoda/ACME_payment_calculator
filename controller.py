import re
import sys
from model import path, hours, cost
from view import view_format


def file_controller(path):
    with open(path) as f:
        lines = f.readlines()
        employees = [x.strip() for x in lines]
    return employees


def time_range_controller(time):
    time_range = time.split('-')
    time_range = [int(x.split(":")[0]) for x in time_range]
    try:
        for i in time_range:
            if not 0 <= i <= 24:
                raise Exception
    except:
        print("Error: ", time, "is not a valid hour")
        sys.exit()
    return time_range


def time_intersection(range1, range2):
    min_range = max(range1[0], range2[0])
    max_range = min(range1[1], range2[1])
    intersection = max_range - min_range
    intersection = 0 if intersection < 0 else intersection
    return intersection


def get_amount_pay_per_day(day, hours, hours_cost):
    total_per_day = 0
    for key, value in hours_cost.items():
        if day in ['SU', 'SA']:
            key += 5
        total_per_day += key * \
            time_intersection(time_range_controller(hours), value)
    return total_per_day


def get_total(employee_string, hours_cost):
    employee_string = re.split(',|=', employee_string)
    total = 0
    for i in employee_string[1::]:
        total += get_amount_pay_per_day(i[0:2], i[2::], hours_cost)
    print(view_format.format(employee_string[0], total))


def client_controller():
    employees = file_controller(path)

    hours_cost = {cost[i]: time_range_controller(
        hours[i]) for i in range(len(cost))}

    for i in employees:
        get_total(i, hours_cost)


if __name__ == '__main__':
    print('Controller')
