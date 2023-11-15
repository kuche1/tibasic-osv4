#! /usr/bin/env python3

import lib_tibasic

with lib_tibasic.TiBasicLib(
        archive=False,
    ) as tb:

    lbl_main_menu = tb.gen_label()
    lbl_main_menu_break = tb.gen_label()

    with tb.whiletrue(lbl_main_menu):

        # menu title

        vls_menu_title = tb.gen_var_lstr() # TODO also add the free memory

        with tb.scope():
            # get time

            vls_time = tb.gen_var_lstr()
            tb.time_get(vls_time)

            # get battery

            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high
            # output: tb.VAR_RET_NUM[0]

            v_battery = tb.gen_var_num()
            tb.raw(f'{tb.VAR_RET_NUM[0]}->{v_battery}')

            tb.digit_to_lchar(v_battery, v_battery)

            # get mem

            tb.call('getmem')
            # output: tb.VAR_RET_NUM[0]

            vn_memory = tb.gen_var_num()
            tb.raw(f'{tb.VAR_RET_NUM[0]}->{vn_memory}')
            tb.raw(f'int({vn_memory}/1024->{vn_memory}') # now in KiB, rounded down; value should be between 16 and 0

            vls_memory = tb.gen_var_lstr()

            tb.num0to99_to_lstr(vls_memory, vn_memory)

            # glue together

            tb.lst_cat(
                vls_menu_title,
                vls_time,
                '{'
                    + tb.pychar_to_lchar(' ') +','+ v_battery +','+ tb.pychar_to_lchar('/') +','+ tb.pychar_to_lchar('4')
                    +','+ tb.pychar_to_lchar(' ')
                + '}'
            )

            tb.lst_cat(vls_menu_title, vls_menu_title, vls_memory)

            tb.lst_cat(
                vls_menu_title,
                vls_menu_title,
                '{'
                    + tb.pychar_to_lchar('/') +','+ tb.pychar_to_lchar('2') +','+ tb.pychar_to_lchar('4') +','+ tb.pychar_to_lchar('K')
                + '}'
            )

        # menu labels

        lbl_battery = tb.gen_label()
        lbl_date_get = tb.gen_label()
        lbl_date_set = tb.gen_label()
        lbl_exit = tb.gen_label()
        lbl_memory = tb.gen_label()
        lbl_notes = tb.gen_label()
        lbl_poweroff = tb.gen_label()
        # lbl_raspisanie = tb.gen_label()
        lbl_time_get = tb.gen_label()
        lbl_time_set = tb.gen_label()
        lbl_timer = tb.gen_label()
        lbl_test = tb.gen_label()
        lbl_porn = tb.gen_label()
        lbl_garbage_collect = tb.gen_label()

        tb.menu(
            vls_menu_title,
            [
                '"NOTES"',
                '"TIMER"',
                '"PORN"',
                '"GC"',
                '"POWEROFF"',
                '"DATE:GET"',
                '"DATE:SET"',
                '"BATTERY"',
                '"MEMORY"',
                # '"RASPISANIE"',
                '"TIME:GET"',
                '"TIME:SET"',
                '"TEST"',
            ],
            [
                lbl_notes,
                lbl_timer,
                lbl_porn,
                lbl_garbage_collect,
                lbl_poweroff,
                lbl_date_get,
                lbl_date_set,
                lbl_battery,
                lbl_memory,
                # lbl_raspisanie,
                lbl_time_get,
                lbl_time_set,
                lbl_test,
            ]
        )
        tb.goto(lbl_exit)

        tb.label(lbl_garbage_collect)
        tb.garbage_collect()
        tb.goto(lbl_main_menu)

        tb.label(lbl_porn)
        with tb.scope():
            tb.call('porn')
        tb.goto(lbl_main_menu)

        tb.label(lbl_battery)
        with tb.scope():

            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high

            # low_bound = tb.gen_var_num()
            low_bound = tb.gen_var_num()
            high_bound = tb.gen_var_num()

            tb.raw(f'{tb.VAR_RET_NUM[0]}*20->{low_bound}')
            tb.raw(f'{low_bound}+20->{high_bound}')

            tb.print_str('"BATTERY BETWEEN"')
            tb.print(low_bound)
            tb.print_str('"AND"')
            tb.print(high_bound)
            tb.print_str('"PERCENT"')

            tb.call('pause')
        tb.goto(lbl_main_menu) # has to be here so that the `scope onexit` functionality executes

        tb.label(lbl_date_get)
        with tb.scope():
            date = tb.gen_var_lstr()
            tb.date_get(date)
            tb.print(date)

            tb.call('pause')
        tb.goto(lbl_main_menu)

        tb.label(lbl_date_set)
        with tb.scope():
            year = tb.gen_var_num()
            month = tb.gen_var_num()
            day = tb.gen_var_num()

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

            free_mem = tb.gen_var_num()
            tb.raw(f'{tb.VAR_RET_NUM[0]}->{free_mem}')

            tb.print_str('"FREE MEMORY:"')
            tb.print(free_mem)

            tb.call('pause')
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
            tb.call('pause')
        tb.goto(lbl_main_menu)

        tb.label(lbl_time_set)
        with tb.scope():
            hour = tb.gen_var_num()
            minute = tb.gen_var_num()
            second = tb.gen_var_num()

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
            tb.call('pause')
        tb.continuee(lbl_main_menu)

    tb.label(lbl_main_menu_break)
