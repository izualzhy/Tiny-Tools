#!/usr/bin/env python
# -*- coding=utf-8 -*-


# --------------------------------------------------------------------------
##
# @Synopsis  decorator for sort_method function
#
# @Param sort_func sort method
#
# @Returns what sort_method function returns
# ----------------------------------------------------------------------------
def drawable(sort_func):
    def _drawable_sort(*args, **kwargs):
        args[0].pre_drawing(sort_func.__name__)
        r = sort_func(*args, **kwargs)
        args[0].post_drawing()
        return r
    return _drawable_sort


# --------------------------------------------------------------------------
##
# @Synopsis  implemenation of insert sort, with curse drawing.
#
# @Param drawable_list the list to be sorted, with drawing API.
#
# @Returns
# ----------------------------------------------------------------------------
@drawable
def insert_sort(drawable_list):
    for i, number in enumerate(drawable_list.get_numbers()):
        drawable_list.set_active(i)
        drawable_list.set_pivot(i)
        j = i
        while j > 0 and drawable_list.compare_with_pivot(j - 1):
            drawable_list.set_value(j, drawable_list.get_value(j - 1))
            j -= 1
        drawable_list.clear_pivot()
        drawable_list.set_sorted(i)
        drawable_list.set_value(j, number)


# --------------------------------------------------------------------------
##
# @Synopsis  implemenation of bubble sort, with curse drawing.
#
# @Param drawable_list the list to be sorted, with drawing API.
#
# @Returns
# ----------------------------------------------------------------------------
@drawable
def bubble_sort(drawable_list):
    drawable_list_len = len(drawable_list.get_numbers())
    for i in range(drawable_list_len - 1):
        drawable_list.set_active(0)
        for j in range(drawable_list_len - 1 - i):
            if drawable_list.compare(j, j + 1):
                drawable_list.swap_values(j, j + 1)
        drawable_list.set_sorted(drawable_list_len - 1 - i)
    drawable_list.set_sorted(0)


# --------------------------------------------------------------------------
##
# @Synopsis  implemenation of quick sort, with curse drawing.
#
# @Param drawable_list the list to be sorted, with drawing API.
#
# @Returns
# ----------------------------------------------------------------------------
@drawable
def quick_sort(drawable_list):
    _quick_sort(drawable_list, 0, len(drawable_list.get_numbers()) - 1)


def _quick_sort(drawable_list, left, right):
    if left <= right:
        drawable_list.set_active(left)
        drawable_list.set_pivot(left)
        key = drawable_list.get_value(left)
        low = left
        high = right
        while (low < high):
            while low < high and drawable_list.compare_with_pivot(high):
                high -= 1
            drawable_list.set_value(low, drawable_list.get_value(high))
            while low < high and not drawable_list.compare_with_pivot(low):
                low += 1
            drawable_list.set_value(high, drawable_list.get_value(low))
        drawable_list.clear_pivot()
        drawable_list.set_sorted(low)
        drawable_list.set_value(low, key)
        _quick_sort(drawable_list, left, low - 1)
        _quick_sort(drawable_list, low + 1, right)
