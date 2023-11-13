#! /usr/bin/env python3

import tibasiclib

CMD_BATTERY = 'BATTERY'
CMD_DATE_GET = 'DATE:GET'
CMD_DATE_SET = 'DATE:SET'
CMD_EXIT = 'EXIT'
CMD_MEMORY = 'MEMORY'
CMD_RASPISANIE = 'RASPISANIE'
CMD_TIME_GET = 'TIME:GET'
CMD_TIME_SET = 'TIME:SET'
CMD_TIMER = 'TIMER'

with tibasiclib.TiBasicLib(
        archive=False,
    ) as tb:

    lbl_main_menu = tb.get_label()
    lbl_main_menu_break = tb.get_label()

    with tb.whiletrue(lbl_main_menu):

        # menu title

        vs_menu_title = tb.get_var_str()

        with tb.scope():
            vs_date = tb.get_var_str()
            tb.date_get(vs_date)

            vs_time = tb.get_var_str()
            tb.time_get(vs_time)
            
            tb.raw(f'{vs_date}+" "+{vs_time}->{vs_menu_title}')

        # menu labels

        lbl_battery = tb.get_label()
        lbl_date_get = tb.get_label()
        lbl_date_set = tb.get_label()
        lbl_exit = tb.get_label()
        lbl_memory = tb.get_label()
        lbl_raspisanie = tb.get_label()
        lbl_time_get = tb.get_label()
        lbl_time_set = tb.get_label()
        lbl_timer = tb.get_label()

        tb.menu(
            vs_menu_title,
            [
                CMD_BATTERY,
                CMD_DATE_GET,
                CMD_DATE_SET,
                CMD_EXIT,
                CMD_MEMORY,
                CMD_RASPISANIE,
                CMD_TIME_GET,
                CMD_TIME_SET,
                CMD_TIMER,
            ],
            [
                lbl_battery,
                lbl_date_get,
                lbl_date_set,
                lbl_exit,
                lbl_memory,
                lbl_raspisanie,
                lbl_time_get,
                lbl_time_set,
                lbl_timer,
            ]
        )

        lbl_press_any_key = tb.get_label()

        # with tb.if_var_equ_strs(command, CMDS_BATTERY):
        with tb.scope():
            tb.label(lbl_battery)

            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high

            # low_bound = tb.get_var_num()
            low_bound = tb.get_var_num_stack()
            high_bound = tb.get_var_num()

            tb.raw(f'{tb.var_ret}*20->{low_bound}')
            tb.raw(f'{low_bound}+20->{high_bound}')

            tb.printstr('battery between')
            tb.printvar(low_bound)
            tb.printstr('and')
            tb.printvar(high_bound)
            tb.printstr('percent')
        tb.goto(lbl_press_any_key) # has to be here so that the `scope onexit` functionality executes

        # with tb.if_var_equ_strs(command, CMDS_DATE_GET):
        with tb.scope():
            tb.label(lbl_date_get)
            date = tb.get_var_str()
            tb.date_get(date)
            tb.printvar(date)
        tb.goto(lbl_press_any_key)

        # with tb.if_var_equ_strs(command, CMDS_DATE_SET):
        with tb.scope():
            tb.label(lbl_date_set)
            year = tb.get_var_num()
            month = tb.get_var_num()
            day = tb.get_var_num()

            tb.input(year, 'YEAR: ')
            tb.input(month, 'MONTH: ')
            tb.input(day, 'DAY: ')

            tb.date_set(year, month, day)

        tb.goto(lbl_main_menu)

        # with tb.if_var_equ_strs(command, CMDS_EXIT):
        with tb.scope():
            tb.label(lbl_exit)
            # TODO implement tb.breakk(lbl_main_menu)
        tb.goto(lbl_main_menu_break)

        # with tb.if_var_equ_strs(command, CMDS_MEMORY):
        with tb.scope():
            tb.label(lbl_memory)
            tb.call('getmem')
            # returns free bytes

            free_mem = tb.get_var_num()
            tb.raw(f'{tb.var_ret}->{free_mem}')

            tb.printstr('free memory:')
            tb.printvar(free_mem)

        tb.goto(lbl_press_any_key)
        
        # with tb.if_var_equ_strs(command, CMDS_RASPISANIE):
        with tb.scope():
            tb.label(lbl_raspisanie)
            tb.call('rspsnie')
        tb.goto(lbl_main_menu)
        
        # with tb.if_var_equ_strs(command, CMDS_TIME_GET):
        with tb.scope():
            tb.label(lbl_time_get)
            time = tb.get_var_str()
            tb.time_get(time)
            tb.printvar(date)
        tb.goto(lbl_press_any_key)

        # with tb.if_var_equ_strs(command, CMDS_TIME_SET):
        with tb.scope():
            tb.label(lbl_time_set)
            hour = tb.get_var_num()
            minute = tb.get_var_num()
            second = tb.get_var_num()

            tb.input(hour, 'HOUR: ')
            tb.input(minute, 'MINUTE: ')
            tb.raw(f'0->{second}')

            tb.time_set(hour, minute, second)

        tb.goto(lbl_main_menu)

        # with tb.if_var_equ_strs(command, CMDS_TIMER):
        with tb.scope():
            tb.label(lbl_timer)
            tb.call('timer')
        tb.goto(lbl_press_any_key)

        # TODO prgmNOTES

        # TODO prgmOFF

        with tb.scope():
            tb.label(lbl_press_any_key)
            tb.press_any_key()

    tb.label(lbl_main_menu_break)
