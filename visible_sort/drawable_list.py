#!/usr/bin/env python
# -*- coding=utf-8 -*-

import time
import curses
import logging
import setting


# --------------------------------------------------------------------------
##
# @Synopsis a list with apis for sort method, which implements the specific
#           drawing status. The elements which has been sorted will show in
#           a different color:GREEN. Operation like compare causes "twinkle"
#           between two elements.
# ----------------------------------------------------------------------------
class DrawableList(object):
    def __init__(self, scr, numbers):
        logging.info("DrawableList::__init__")
        self.__numbers = numbers
        self.__scr = scr
        self.__sorted_indexes = []
        self.__max_scr_height, self.__max_scr_width = self.__scr.getmaxyx()
        self.__draw_list()
        self.__draw_help_message()
        self.__pivot = None

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the list of numbers
    #
    # @Returns return the list of numbers
    # ----------------------------------------------------------------------------
    def get_numbers(self):
        return self.__numbers

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the value of element
    #
    # @Param index the index of elment in numbers
    #
    # @Returns return the value of element
    # ----------------------------------------------------------------------------
    def get_value(self, index):
        return self.__numbers[index]

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  set the value of element and draw the element
    #
    # @Param index the index of element
    # @Param value the value will be setted
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def set_value(self, index, value):
        self.__numbers[index] = value
        self.__draw_item(index)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  swap two elements and draw the two elements
    #
    # @Param left_hand
    # @Param right_hand
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def swap_values(self, left_hand, right_hand):
        self.__numbers[left_hand], self.__numbers[right_hand] = \
            self.__numbers[right_hand], self.__numbers[left_hand]
        self.__draw_item(left_hand)
        self.__draw_item(right_hand)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  refresh numbers and draw them
    #
    # @Param numbers the numbers to be setted
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def refresh_list(self, numbers):
        self.__numbers = numbers
        self.__draw_list()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  mark the element which has been sorted, bcz we want to draw the
    #            sorted elemnets in different color:GREEN
    # @Param index the index of element
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def set_sorted(self, index):
        logging.info("set_sorted:%d", index)
        self.__sorted_indexes.append(index)
        self.__draw_item(index)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  draw the whole numbers
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_list(self):
        logging.info("__draw_list:%s", self.__numbers)
        for index in range(len(self.__numbers)):
            self.__draw_item(index)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  draw single element, if it's sorted, green color will be used.
    #
    # @Param index the index of element
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_item(self, index):
        index_draw_pos = self.__get_pos(index)
        index_draw_str = self.__get_str(index)
        curse_color_number = 1 if index in self.__sorted_indexes else 0
        self.__scr.addstr(
            index_draw_pos[0],
            index_draw_pos[1],
            index_draw_str,
            curses.color_pair(curse_color_number))
        self.__scr.refresh()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  erase item from screen
    #
    # @Param index the index of element
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __erase_item(self, index):
        index_draw_pos = self.__get_pos(index)
        index_draw_str = self.__get_str(index)
        self.__scr.addstr(
            index_draw_pos[0],
            index_draw_pos[1],
            ' ' * len(index_draw_str))
        self.__scr.refresh()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the pos of elment, I prefer to draw the list in the center of screen.
    #
    # @Param index the index of element
    #
    # @Returns the pos of element
    # ----------------------------------------------------------------------------
    def __get_pos(self, index):
        return (
            ((self.__max_scr_height - len(self.__numbers)) >> 1) + index,
            self.__max_scr_width >> 1)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the str of element, I perfer to use the number itself.
    #            maybe string like '++++++' is better.
    #
    # @Param index the index of element
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __get_str(self, index):
        return str(self.__numbers[index])

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the pos of pivot.
    #            pivot is needed by some sort method like quick sort, which will be drawed too.
    # @Returns   the pos of pivot
    # ----------------------------------------------------------------------------
    def __get_pivot_pos(self):
        return (
            (self.__max_scr_height >> 1), (self.__max_scr_width >> 1) + 5)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  get the str of pivot.
    #            pivot is needed by some sort method like quick sort, which will be drawed too.
    # @Returns   the str of pivot
    # ----------------------------------------------------------------------------
    def __get_pivot_str(self):
        return str(self.__pivot)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  set the pivot
    #
    # @Param index the index of elements which voted to be a pivot
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def set_pivot(self, index):
        logging.info("set_pivot:%d", index)
        self.__pivot = self.__numbers[index]
        self.__draw_pivot()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  draw the pivot, pos in the right-middle of the screen
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_pivot(self):
        if self.__pivot:
            pivot_draw_pos = self.__get_pivot_pos()
            pivot_draw_str = self.__get_pivot_str()
            self.__scr.addstr(pivot_draw_pos[0], pivot_draw_pos[1], pivot_draw_str)
            self.__scr.refresh()
        else:
            logging.warn("__draw_pivot pivot is None")

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  clear the pivot memeber and erase the pivot from the screen
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def clear_pivot(self):
        logging.info("clear_pivot")
        self.__erase_pivot()
        self.__pivot = None

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  erase the pivot from the screen
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __erase_pivot(self):
        if self.__pivot:
            pivot_draw_pos = self.__get_pivot_pos()
            pivot_draw_str = self.__get_pivot_str()
            self.__scr.addstr(pivot_draw_pos[0], pivot_draw_pos[1], ' ' * len(pivot_draw_str))
            self.__scr.refresh()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  set the element active, which will twinkle on the screen
    #
    # @Param index the index of active element
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def set_active(self, index):
        logging.info('set_active:%d', index)
        for i in range(setting.twinkle_times << 1):
            if i % 2:
                self.__draw_item(index)
            else:
                self.__erase_item(index)
            time.sleep(setting.twinkle_interval)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  compare with the pivot, the numbers to be compared will twinkle.
    #
    # @Param index the index of element compared with pivot
    #
    # @Returns True if the element is greater than pivot
    # ----------------------------------------------------------------------------
    def compare_with_pivot(self, index):
        logging.info("compare_with_pivot:%d", index)
        for i in range(setting.twinkle_times << 1):
            time.sleep(setting.twinkle_interval)
            if i % 2:
                self.__draw_item(index)
            else:
                self.__erase_item(index)
        return self.__numbers[index] > self.__pivot

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  compare two elements, the numbers to be compared will twinkle.
    #
    # @Param left_hand
    # @Param right_hand
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def compare(self, left_hand, right_hand):
        logging.info("compare:%d %d", left_hand, right_hand)
        for i in range(setting.twinkle_times << 1):
            time.sleep(setting.twinkle_interval)
            if i % 2:
                self.__draw_item(left_hand)
                self.__draw_item(right_hand)
            else:
                self.__erase_item(left_hand)
                self.__erase_item(right_hand)
        return self.__numbers[left_hand] > self.__numbers[right_hand]

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  before showing the process of sort method,
    #            do something like draw the title
    #
    # @Param sort_method_name
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def pre_drawing(self, sort_method_name):
        self.__scr.clear()
        self.__draw_list()
        self.__draw_title(sort_method_name)
        self.__draw_help_message()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  draw the title on middle-top of the screen
    #
    # @Param sort_method_name title
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_title(self, sort_method_name):
        pos_x = (self.__max_scr_width - len(sort_method_name)) >> 1
        pos_y = 2
        self.__scr.addstr(pos_y, pos_x, sort_method_name, curses.A_BOLD)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  after showing the process of sort method,
    #            do something like clear the title, show the quit message.
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def post_drawing(self):
        self.__draw_quit_message()
        self.__scr.getch()
        self.__sorted_indexes = []
        self.__scr.clear()
        self.__draw_list()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  show the quit message
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_quit_message(self):
        quit_message = "press any key to return."
        pos_x = (self.__max_scr_width - len(quit_message)) >> 1
        pos_y = ((self.__max_scr_height + len(self.__numbers)) >> 1) + 1
        self.__scr.addstr(pos_y, pos_x, quit_message, curses.A_BOLD)
        self.__scr.refresh()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  show the help info.
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __draw_help_message(self):
        help_messages = [
            '1. The elements sorted show in green.',
            '2. The two numbers comparing will twinkle.',
            '3. The pivot, if have, will show in right-middle pos']
        pos_x = (self.__max_scr_width - len(help_messages[0])) >> 1
        pos_y = ((self.__max_scr_height + len(self.__numbers)) >> 1) + 1
        for i in range(len(help_messages)):
            pos_y += 1
            curse_color_number = 1 if i == 0 else 0
            self.__scr.addstr(pos_y, pos_x, help_messages[i], curses.color_pair(curse_color_number))
        contact_message = 'producted by http://yingshin.github.io, contact:zhy198606@gmail.com'
        self.__scr.addstr(
            self.__max_scr_height - 1,
            self.__max_scr_width - len(contact_message) - 1,
            contact_message)
