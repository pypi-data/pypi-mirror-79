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

    @classmethod
    @Timer.interval(minutes=1)
    def Timer(cls, interval):
        start = time.time()
        foo = 3
        while True:
            try:
                print(cls.__doc__)
                100 / foo
            except Exception as e:
                foo = 3
                Timer(interval=interval, start=start, is_error=True, exception=e)
                continue
            foo -= 1
            Timer(interval=1, start=start, EXTRA='Extra information goes here')

    # @classmethod
    # def Slicer(cls, **kwargs):
        # if 'input_data' in kwargs and isinstance(kwargs['input_data'], list):
            # method = getattr(ContainerSlicer, 'split_list')
            # src = kwargs['input_data']
        # elif 'input_data' in kwargs and isinstance(kwargs['input_data'], dict):
            # method = getattr(ContainerSlicer, 'split_dict')
            # src = kwargs['input_data']
        # elif 'number' in kwargs and type(kwargs['number']) in [str, int]:
            # method = getattr(ContainerSlicer, 'split_number')
            # src = kwargs['number']
        # else:
            # raise ValueError(f'Invalid type or error input! {kwargs}')
        # results = method(**kwargs)
        # print(f'{"":=^90}')
        # print(f'Input:\n\t{src}')
        # print(f'Results:\n\t{results}')
        # print(f'Amount: {len(results)}')
        # print(f'{"":-^90}')
        # for index, result in enumerate(results):
            # print(f'slice {index} | len == {len(result)} | {result}')
        # print(f'{"":=^90}')

    # ## ################## Demo a: split list  ################## ##
    # demo(input_data=[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], slice_length=4)
    # ## ################## Demo a: split list  ################## ##

    # ## ################## Demo b: split dict  ################## ##
    # input_data = {
        # '1': {'name': 'Ajax', 'age': 25},
        # '2': {'name': 'Roni', 'age': 29},
        # '3': {'name': 'Jeffrey', 'age': 34},
        # '4': {'name': 'Josh', 'age': 33},
        # '5': {'name': 'Kevin', 'age': 26},
        # '6': {'name': 'Jeque', 'age': 23},
        # '7': {'name': 'Amy', 'age': 32},
        # '8': {'name': 'May', 'age': 49},
        # '9': {'name': 'Ronnie', 'age': 22},
    # }
    # demo(input_data=input_data, slice_length=2)
    # ## ################## Demo b: split dict  ################## ##

    # ## ################## Demo c: split a number ################## ##
    # demo(number=40, slice_length=7)
    # ## ################## Demo c: split a number ################## ##
