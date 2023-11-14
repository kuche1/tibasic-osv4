#! /usr/bin/env python3

import tibasiclib

with tibasiclib.TiBasicLib(
        archive=False,
    ) as tb:

    lbl_main_menu = tb.get_label()
    lbl_main_menu_break = tb.get_label()

    with tb.whiletrue(lbl_main_menu):

        # menu title

        vls_menu_title = tb.gen_var_lstr()

        with tb.scope():
            vls_time = tb.gen_var_lstr()
            tb.time_get(vls_time)

            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high
            # output: tb.VAR_RET_NUM[0]

            v_battery = tb.get_var_num()
            tb.raw(f'{tb.VAR_RET_NUM[0]}->{v_battery}')

            tb.digit_to_lchar(v_battery, v_battery)

            tb.lst_cat(vls_menu_title, vls_time, '{' + tb.LCHAR_SPACE +','+ v_battery +','+ tb.LCHAR_SLASH +','+ tb.LCHAR_4 + '}')

        # menu labels

        lbl_battery = tb.get_label()
        lbl_date_get = tb.get_label()
        lbl_date_set = tb.get_label()
        lbl_exit = tb.get_label()
        lbl_memory = tb.get_label()
        lbl_notes = tb.get_label()
        lbl_poweroff = tb.get_label()
        # lbl_raspisanie = tb.get_label()
        lbl_time_get = tb.get_label()
        lbl_time_set = tb.get_label()
        lbl_timer = tb.get_label()
        lbl_test = tb.get_label()
        lbl_porn = tb.get_label()

        tb.menu(
            vls_menu_title,
            [
                '"* EXIT"',
                '"NOTES"',
                '"TIMER"',
                '"PORN"',
                '"BATTERY"',
                '"MEMORY"',
                '"POWEROFF"',
                '"DATE:GET"',
                '"DATE:SET"',
                # '"RASPISANIE"',
                '"TIME:GET"',
                '"TIME:SET"',
                '"TEST"',
            ],
            [
                lbl_exit,
                lbl_notes,
                lbl_timer,
                lbl_porn,
                lbl_battery,
                lbl_memory,
                lbl_poweroff,
                lbl_date_get,
                lbl_date_set,
                # lbl_raspisanie,
                lbl_time_get,
                lbl_time_set,
                lbl_test,
            ]
        )

        tb.label(lbl_porn)
        with tb.scope():
            tb.call('porn')
        tb.goto(lbl_main_menu)

        tb.label(lbl_battery)
        with tb.scope():

            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high

            # low_bound = tb.get_var_num()
            low_bound = tb.get_var_num_stack()
            high_bound = tb.get_var_num()

            tb.raw(f'{tb.VAR_RET_NUM[0]}*20->{low_bound}')
            tb.raw(f'{low_bound}+20->{high_bound}')

            tb.print_str('"BATTERY BETWEEN"')
            tb.print(low_bound)
            tb.print_str('"AND"')
            tb.print(high_bound)
            tb.print_str('"PERCENT"')

            tb.press_any_key()
        tb.goto(lbl_main_menu) # has to be here so that the `scope onexit` functionality executes

        tb.label(lbl_date_get)
        with tb.scope():
            date = tb.gen_var_lstr()
            tb.date_get(date)
            tb.print(date)

            tb.press_any_key()
        tb.goto(lbl_main_menu)

        tb.label(lbl_date_set)
        with tb.scope():
            year = tb.get_var_num()
            month = tb.get_var_num()
            day = tb.get_var_num()

            tb.input(year,  '"YEAR: "')
            tb.input(month, '"MONTH: "')
            tb.input(day,   '"DAY: "')

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
            tb.raw(f'{tb.VAR_RET_NUM[0]}->{free_mem}')

            tb.print_str('"FREE MEMORY:"')
            tb.print(free_mem)

            tb.press_any_key()
        tb.goto(lbl_main_menu)

        tb.label(lbl_notes)
        with tb.scope():
            tb.call('notes')
        tb.continuee(lbl_main_menu)

        tb.label(lbl_poweroff)
        with tb.scope():
            tb.call('pwroff')
        tb.continuee(lbl_main_menu)
        
        # tb.label(lbl_raspisanie)
        # with tb.scope():
        #     tb.call('rspsnie')
        # tb.goto(lbl_main_menu)
        
        tb.label(lbl_time_get)
        with tb.scope():
            time = tb.gen_var_lstr()
            tb.time_get(time)
            tb.print(time)
            tb.press_any_key()
        tb.goto(lbl_main_menu)

        tb.label(lbl_time_set)
        with tb.scope():
            hour = tb.get_var_num()
            minute = tb.get_var_num()
            second = tb.get_var_num()

            tb.input(hour,   '"HOUR: "')
            tb.input(minute, '"MINUTE: "')
            tb.raw(f'0->{second}')

            tb.time_set(hour, minute, second)

        tb.goto(lbl_main_menu)

        tb.label(lbl_timer)
        with tb.scope():
            tb.call('timer')
        tb.continuee(lbl_main_menu)

        tb.label(lbl_test)
        with tb.scope():
            tb.print('"hi"')
            tb.press_any_key()
        tb.continuee(lbl_main_menu)

    tb.label(lbl_main_menu_break)
