#!/usr/bin/env python
# -*- coding=utf-8 -*-


# import curses
# import logging
# import traceback
import sort_console


if __name__ == '__main__':
    with sort_console.SortConsole.get_sort_console() as visible_sort_console:
        visible_sort_console.run()
