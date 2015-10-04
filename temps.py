# !/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from operator import itemgetter


class Temps:
    """
    Class that tracks temperatures, Appends temperatures to
    a list as tuples (str_clock, float_temp)
    """

    def __init__(self, hist_len=1440):
        """
        Init method for Temps-class. Optional argument
        is the length of the history(int) which defaults
        to 1440(one val for each minute in a day.
        """
        self._history_length = hist_len
        self._temps = []

    def store_val(self, val):
        """
        Store a temperature inside the class, val will be
        stored as a float inside a tuple. Returns nothing
        """
        if len(self._temps) >= self._history_length:
            del self._temps[0]
        self._temps.append((time.strftime('%H:%M'), float(val)))

    def get_high_temp(self):
        """
        Returns the highest stored temperature as
        a float. If there are no stored values returns
        None.
        """
        return None if self.is_empty() else max(self._temps, key=itemgetter(1))[1]

    def get_low_temp(self):
        """
        Returns the lowest stored temperature as
        a float. If there are no stored values returns
        None.
        """
        return None if self.is_empty() else min(self._temps, key=itemgetter(1))[1]

    def get_current_temp(self):
        """
        Get the last temperature stored in this class.
        Returns a tuple with a clock as a string and
        temperature as a float. ex: ("13:37", 6.67).
        If there are no stored values returns None.
        """
        return None if self.is_empty() else self._temps[-1]

    def get_average_temp(self):
        """
        Returns the average temperature from all
        values stored inside this object. Returns
        None if we have no values
        """
        return None if self.is_empty() \
            else sum(temp[1] for temp in self._temps) / len(self._temps)

    def is_empty(self):
        """
        If this function returns True it means
        we have no recorded data. The list
        has length of 0.
        """
        return not self._temps

    def __str__(self):
        return str(self._temps)


def main():
    """
    this function is only used for testing
    """
    #temps = Temps(1)
    temps = Temps()
    #for i in range(1440):
    #    temps.store_val(i)
    #temps.store_val(2.0)
    #temps.store_val(23.3)
    #temps.store_val(23.2)
    #temps.store_val(23.343)
    temps.store_val(-34.40)
    #temps.store_val(-34.40)
    temps.store_val(34.40)


    #print temps.is_empty()
    print temps

    print

    print 'min:', temps.get_low_temp()
    print 'max:', temps.get_high_temp()
    print 'temp now:', temps.get_current_temp()
    print "average :", temps.get_average_temp()


if __name__ == '__main__':
    main()