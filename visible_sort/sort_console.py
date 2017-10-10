#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging
import traceback
import curses
import random
import copy
import drawable_list
import sort_method


# --------------------------------------------------------------------------
##
# @Synopsis  Sort console with menus, which shows the welcome page.
# ----------------------------------------------------------------------------
class SortConsole(object):
    # --------------------------------------------------------------------------
    ##
    # @Synopsis static method which will be used in with statement
    # ----------------------------------------------------------------------------
    @staticmethod
    def get_sort_console():
        return SortConsole()

    def __enter__(self):
        logging.info('__enter__')
        return self

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  make sure to run `curses.endwin`
    #
    # @Param t exception type
    # @Param value exception value
    # @Param trace exception trace
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __exit__(self, t, value, trace):
        logging.info('__exit__')
        curses.endwin()
        if not t:
            logging.warn(traceback.format_exception(t, value, trace))

    def __init__(self):
        # init log
        logging.basicConfig(
            filename='log.txt',
            filemode='w',
            level=logging.NOTSET,
            format='%(asctime)s - %(levelname)s: %(message)s')
        # init curses
        self.__scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.__scr.keypad(1)
        # terminal maybe not support curse invisibility
        try:
            curses.curs_set(False)
        except Exception as e:
            logging.error('Exception:%s\n%s' % (str(e), traceback.format_exc()))
        # init members
        self.__numbers = range(10)
        random.shuffle(self.__numbers)
        self.__running = True
        self.__drawable_list = drawable_list.DrawableList(self.__scr, self.__copy_numbers())
        self.__menu_names = [
            'InsertSort', 'QuickSort', 'BubbleSort', 'RefreshList', 'Quit']
        self.__menu_actions = [
            self.insert_sort,
            self.quick_sort,
            self.bubble_sort,
            self.refresh_list,
            self.quit]

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  run until ask to quit:
    #            show welcome page, wait for the keyboard input, then process on
    #            the shortcut key.
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def run(self):
        while self.__running:
            self.__show_welcom_win()
            shortcut_key = self.__scr.getch()
            self.__process_shortcut_key(shortcut_key)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  show welcome page, with menus and numbers to be sorted.
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __show_welcom_win(self):
        logging.info('__show_welcom_win:%s', self.__menu_names)
        top = 0
        left = 0
        self.__scr.addstr(top, left, "menus:")
        for index, menu in enumerate(self.__menu_names):
            top += 1
            left = 4
            shortcut_key_str = '[%s] ' % str(index)
            self.__scr.addstr(top, left, shortcut_key_str, curses.A_BOLD)
            left += len(shortcut_key_str)
            self.__scr.addstr(top, left, menu)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  process the shortcut key.choose the right process action from
    #            the self.__menu_actions
    # @Param shortcut_key keyboard input
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def __process_shortcut_key(self, shortcut_key):
        logging.info('shortcut_key:%c', chr(shortcut_key))
        index = shortcut_key - ord('0')
        if index in range(len(self.__menu_names)):
            self.__menu_actions[index]()

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  just for convenience to get the deepcopy of self.__numbers
    #
    # @Returns the deepcopy of self.__numbers
    # ----------------------------------------------------------------------------
    def __copy_numbers(self):
        return copy.deepcopy(self.__numbers)

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  action for menu "InsertSort"
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def insert_sort(self):
        logging.info('insert_sort')
        sort_method.insert_sort(self.__drawable_list)
        self.__drawable_list.refresh_list(self.__copy_numbers())

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  action for menu "QuickSort"
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def quick_sort(self):
        logging.info('quick_sort')
        sort_method.quick_sort(self.__drawable_list)
        self.__drawable_list.refresh_list(self.__copy_numbers())

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  action for menu "BubbleSort"
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def bubble_sort(self):
        logging.info('bubble_sort')
        sort_method.bubble_sort(self.__drawable_list)
        self.__drawable_list.refresh_list(self.__copy_numbers())

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  action for menu "RefreshList"
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def refresh_list(self):
        logging.info('refresh_list')
        random.shuffle(self.__numbers)
        self.__drawable_list.refresh_list(self.__copy_numbers())

    # --------------------------------------------------------------------------
    ##
    # @Synopsis  action for menu "Quit"
    #
    # @Returns
    # ----------------------------------------------------------------------------
    def quit(self):
        self.__running = False
