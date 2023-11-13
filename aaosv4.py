#! /usr/bin/env python3

import tibasiclib

CMDS_ALL = []
CMDS_ALL.append(CMDS_BATTERY := ['BATTERY', 'B', 'b'])
CMDS_ALL.append(CMDS_DATE_GET := ['DATE:GET', 'DG', 'D'])
CMDS_ALL.append(CMDS_DATE_SET := ['DATE:SET', 'DS'])
CMDS_ALL.append(CMDS_EXIT := ['EXIT', 'E', 'e'])
CMDS_ALL.append(CMDS_MEMORY := ['MEMORY', 'M'])
CMDS_ALL.append(CMDS_RASPISANIE := ['RASPISANIE', 'R'])
CMDS_ALL.append(CMDS_TIME_GET := ['TIME:GET', 'T'])
CMDS_ALL.append(CMDS_TIME_SET := ['TIME:SET', 'TS'])
CMDS_ALL.append(CMDS_TIMER := ['TIMER', 'TI'])

with tibasiclib.TiBasicLib(
        archive=False,
    ) as tb:

    lbl_main_menu = tb.get_label()

    with tb.whiletrue(lbl_main_menu):

        command = tb.get_var_str()
        tb.input(command, '>>')

        with tb.iff(f'length({command})=0'): # avoid errors related to `=` down the line
            tb.continuee(lbl_main_menu)

        # with tb.iff(f'{command}="b"|{command}="B"|{command}="battery"'):
        with tb.if_var_equ_strs(command, CMDS_BATTERY):
            tb.call('getbtry')
            # returns battery level
            # 0:4 <-> low:high

            low_bound = tb.get_var_num()
            high_bound = tb.get_var_num()

            tb.raw(f'{tb.var_ret}*20->{low_bound}')
            tb.raw(f'{low_bound}+20->{high_bound}')

            tb.printstr('battery between')
            tb.printvar(low_bound)
            tb.printstr('and')
            tb.printvar(high_bound)
            tb.printstr('percent')

            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_DATE_GET):
            date = tb.get_var_str()
            tb.date_get(date)
            tb.printvar(date)
            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_DATE_SET):
            year = tb.get_var_num()
            month = tb.get_var_num()
            day = tb.get_var_num()

            tb.input(year, 'YEAR: ')
            tb.input(month, 'MONTH: ')
            tb.input(day, 'DAY: ')

            tb.date_set(year, month, day)

            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_EXIT):
            # TODO implement tb.breakk(lbl_main_menu)
            tb.raw('Goto BR')

            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_MEMORY):
            tb.call('getmem')
            # returns free bytes

            free_mem = tb.get_var_num()
            tb.raw(f'{tb.var_ret}->{free_mem}')

            tb.printstr('free memory:')
            tb.printvar(free_mem)

            tb.continuee(lbl_main_menu)
        
        with tb.if_var_equ_strs(command, CMDS_RASPISANIE):
            tb.call('rspsnie')

            tb.continuee(lbl_main_menu)
        
        with tb.if_var_equ_strs(command, CMDS_TIME_GET):
            time = tb.get_var_str()
            tb.time_get(time)
            tb.printvar(date)
            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_TIME_SET):
            hour = tb.get_var_num()
            minute = tb.get_var_num()
            second = tb.get_var_num()

            tb.input(hour, 'HOUR: ')
            tb.input(minute, 'MINUTE: ')
            tb.raw(f'0->{second}')

            tb.time_set(hour, minute, second)

            tb.continuee(lbl_main_menu)

        with tb.if_var_equ_strs(command, CMDS_TIMER):
            tb.call('timer')
            tb.continuee(lbl_main_menu)

        # TODO prgmNOTES

        # TODO prgmOFF

        tb.printstr('unknown action:')
        tb.printvar(command)
        tb.printstr('here is the list of actions:')
        tb.printstr(' '.join(['='.join(cmds) for cmds in CMDS_ALL]))

    tb.raw('Lbl BR')
