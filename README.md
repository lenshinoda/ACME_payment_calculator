# ACME PAYMENT CALCULATOR

_Exercise for IOET_

## Run it locally

Follow this steps to run locally

```sh
git clone https://github.com/lenshinoda/ACME_payment_calculator.git
cd ACME_payment_calculator/
python3 client.py
```

![](console.gif)

### Run with docker

```sh
git clone https://github.com/lenshinoda/ACME_payment_calculator.git
cd ACME_payment_calculator/
docker build -t acme-pay .
docker run --rm acme-pay
```

## Exercise

The company ACME offers their employees the flexibility to work the hours they want. They will pay for the hours worked based on the day of the week and time of day, according to the following table:

#### Monday - Friday

| Hours         | Cost   |
| ------------- | ------ |
| 00:01 - 09:00 | 25 USD |
| 09:01 - 18:00 | 15 USD |
| 18:01 - 00:00 | 20 USD |

#### Saturday and Sunday

| Hours         | Cost   |
| ------------- | ------ |
| 00:01 - 09:00 | 30 USD |
| 09:01 - 18:00 | 20 USD |
| 18:01 - 00:00 | 25 USD |

The goal of this exercise is to calculate the total that the company has to pay an employee, based on the hours they worked and the times during which they worked. The following abbreviations will be used for entering data:

| abb. | MO     | TU      | WE        | TH       | FR     | SA       | SU     |
| ---- | ------ | ------- | --------- | -------- | ------ | -------- | ------ |
| Day  | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday |

**Input:** the name of an employee and the schedule they worked, indicating the time and hours. This should be a .txt file with at least five sets of data. You can include the data from our two examples below.

**Output:** indicate how much the employee has to be paid

For example:

**Case 1:**

```
INPUT:
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00

OUTPUT:
The amount to pay RENE is: 215 USD
```

**Case 2:**

```
INPUT:
ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00

OUTPUT:
The amount to pay ASTRID is: 85 USD
```

## SOLUTION

In my solution, I use the Model-View-Controller pattern.

The [**_Model_**](src/model.py) stores all the information required to run the application like the path of the txt file and payment table.

The [**_View_**](src/view.py) stores the format of the output.

The [**_Controller_**](src/controller.py) is in charge of calculating the total wage for every employee according to data in the Model and displaying it to the stout.

Additionally, A file [client.py](client.py) was created to simulate a client request.

### Controller Logic

As we can see in the [exercise](#exercise), the only change between the hourly-wage-tables for the [weekday](#monday---friday) and the [weekend](#saturday-and-sunday) is an increment of $5 on weekends. So, the most convenient way to approach this is to calculate the wage for each day (multiplying the worked hours by the corresponding hourly wage) and add $5 to the hourly wage on weekends. The controller iterates each line of the [employee_schedule.txt](employee_schedule.txt) and prints the name of the employee and the total wage. The format of each line is:

| name   | =   | day-string    | ,   | day-string    | ,   | day-string    |
| ------ | --- | ------------- | --- | ------------- | --- | ------------- |
| ASTRID | =   | MO10:00-12:00 | ,   | TH12:00-14:00 | ,   | SU20:00-21:00 |

In each iteration the controller follows this steps:

- Split the line by "," and "=" to separate the name and each day-string.
- For each day-string calculate the worked hours and multiply by the corresponding hourly wage. If the day is ['SA', 'SU'] add $5 to the hourly wage.
- Get the total wage by adding all the daily wages.
- Print the total wage and the name of the employee according to the formant in [View](src/view.py).

## Test

The test is implemented in the file [test_controller.py](test_controller.py). This file looks for errors especially in edge cases.

For example, what happen what happen if the file has the invalid string '20:00-25:00':

```python
import unittest
import src.controller as ct

class Test_Controller(unittest.TestCase):
    def test_time_range_controller(self):
        self.assertEqual(ct.time_range_controller('00:00-09:00'), [0, 9])
        self.assertEqual(ct.time_range_controller('9:00-14:00'), [9, 14])
        self.assertEqual(ct.time_range_controller('12:00-24:00'), [12, 24])
        with self.assertRaises(SystemExit):
            ct.time_range_controller('20:00-25:00')
```

The time_range_controller function returns a list with the time range for example:

```python
time_range_controller('00:00-09:00') = [0, 9]
```
