#! /usr/bin/env python3

import tibasiclib

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
        # lbl_notes = tb.get_label()
        lbl_poweroff = tb.get_label()
        # lbl_raspisanie = tb.get_label()
        lbl_time_get = tb.get_label()
        lbl_time_set = tb.get_label()
        lbl_timer = tb.get_label()

        tb.menu(
            vs_menu_title,
            [
                '"BATTERY"',
                '"DATE:GET"',
                '"DATE:SET"',
                '"EXIT"',
                '"MEMORY"',
                # '"NOTES"',
                '"POWEROFF"',
                # '"RASPISANIE"',
                '"TIME:GET"',
                '"TIME:SET"',
                '"TIMER"',
            ],
            [
                lbl_battery,
                lbl_date_get,
                lbl_date_set,
                lbl_exit,
                lbl_memory,
                # lbl_notes,
                lbl_poweroff,
                # lbl_raspisanie,
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

        tb.label(lbl_memory)
        with tb.scope():
            tb.call('getmem')
            # returns free bytes

            free_mem = tb.get_var_num()
            tb.raw(f'{tb.var_ret}->{free_mem}')

            tb.printstr('free memory:')
            tb.printvar(free_mem)
        tb.goto(lbl_press_any_key)

        # tb.label(lbl_notes)
        # with tb.scope():
        #     tb.call('notes')
        # tb.continuee(lbl_main_menu)

        tb.label(lbl_poweroff)
        with tb.scope():
            tb.call('pwroff')
        tb.continuee(lbl_main_menu)
        
        # tb.label(lbl_raspisanie)
        # with tb.scope():
        #     tb.call('rspsnie')
        # tb.goto(lbl_main_menu)
        
        # with tb.if_var_equ_strs(command, CMDS_TIME_GET):
        with tb.scope():
            tb.label(lbl_time_get)
            time = tb.get_var_str()
            tb.time_get(time)
            tb.printvar(date)
        tb.goto(lbl_press_any_key)

        tb.label(lbl_time_set)
        with tb.scope():
            hour = tb.get_var_num()
            minute = tb.get_var_num()
            second = tb.get_var_num()

            tb.input(hour, 'HOUR: ')
            tb.input(minute, 'MINUTE: ')
            tb.raw(f'0->{second}')

            tb.time_set(hour, minute, second)

        tb.goto(lbl_main_menu)

        tb.label(lbl_timer)
        with tb.scope():
            tb.call('timer')
        tb.continuee(lbl_main_menu)

        # TODO prgmNOTES

        with tb.scope():
            tb.label(lbl_press_any_key)
            tb.press_any_key()

    tb.label(lbl_main_menu_break)
