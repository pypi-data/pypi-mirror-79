# Copyright (c) 2020 Ron Chang. All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import time

from .timer import Timer
from .slicer import Slicer
from .bar import Bar


class Demo:

    @classmethod
    @Timer.interval(minutes=1)
    def Timer(cls, interval):
        """
        @Timer.interval(minutes=1)
        def demo_timer(interval):
            start = time.time()
            foo = 3
            while True:
                try:
                    print('Do something here')
                    100 / foo
                except Exception as e:
                    foo = 3
                    Timer(interval=interval, start=start, is_error=True, exception=e)
                    continue
                foo -= 1
                Timer(interval=1, start=start, EXTRA='Extra information goes here')
        """
        start = time.time()
        foo = 3
        while True:
            try:
                print(cls.Timer.__doc__)
                100 / foo
            except Exception as e:
                foo = 3
                Timer(interval=interval, start=start, is_error=True, exception=e)
                continue
            foo -= 1
            Timer(interval=1, start=start, EXTRA='Extra information goes here')

    @classmethod
    def Slicer(cls):
        """
        demo_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        data_1 = Slicer.list(input_data=demo_1, container_length=2)
        print(data_1)

        demo_2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        data_2 = Slicer.list(input_data=demo_2, slice_length=4)
        print(data_2)

        demo_3 = {
            '1': {'name': 'Ajax', 'age': 25},
            '2': {'name': 'Roni', 'age': 29},
            '3': {'name': 'Jeffrey', 'age': 34},
            '4': {'name': 'Josh', 'age': 33},
            '5': {'name': 'Kevin', 'age': 26},
            '6': {'name': 'Jeque', 'age': 23},
            '7': {'name': 'Amy', 'age': 32},
            '8': {'name': 'May', 'age': 49},
            '9': {'name': 'Ronnie', 'age': 22},
        }
        data_3 = Slicer.dict(input_data=demo_2, slice_length=2)
        print(data_3)

        demo_4 = 40
        data_4 = Slicer.number(number=number, slice_length=7)
        print(data_4)
        """
        print(cls.Slicer.__doc__)
        demo_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        data_1 = Slicer.list(input_data=demo_1, container_length=2)
        print(data_1)

        demo_2 = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        data_2 = Slicer.list(input_data=demo_2, slice_length=4)
        print(data_2)

        demo_3 = {
            '1': {'name': 'Ajax', 'age': 25},
            '2': {'name': 'Roni', 'age': 29},
            '3': {'name': 'Jeffrey', 'age': 34},
            '4': {'name': 'Josh', 'age': 33},
            '5': {'name': 'Kevin', 'age': 26},
            '6': {'name': 'Jeque', 'age': 23},
            '7': {'name': 'Amy', 'age': 32},
            '8': {'name': 'May', 'age': 49},
            '9': {'name': 'Ronnie', 'age': 22},
        }
        data_3 = Slicer.dict(input_data=demo_3, slice_length=2)
        print(data_3)

        demo_4 = 40
        data_4 = Slicer.number(number=number, slice_length=7)
        print(data_4)

    @classmethod
    def Bar(cls):
        """
        amount = 147
        demo = '[THIS IS A DEMONSTRATION]'
        for count in range(1, amount+1):
            desc = f'{demo} | {count} of {amount}'
            Bar(count=count, amount=amount, desc=desc, info='test')
            time.sleep(0.01)
        """
        print(cls.Bar.__doc__)
        amount = 147
        demo = '[THIS IS A DEMONSTRATION]'
        for count in range(1, amount+1):
            desc = f'{demo} | {count} of {amount}'
            Bar(count=count, amount=amount, desc=desc, info='test')
            time.sleep(0.01)

