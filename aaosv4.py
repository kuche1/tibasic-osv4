#! /usr/bin/env python3

import tibasiclib

CMDS_ALL = []
CMDS_ALL.append(CMDS_BATTERY := ['BATTERY', 'B', 'b'])
CMDS_ALL.append(CMDS_EXIT := ['EXIT', 'E', 'e'])
CMDS_ALL.append(CMDS_MEMORY := ['MEMORY', 'M'])
CMDS_ALL.append(CMDS_RASPISANIE := ['RASPISANIE', 'R'])

with tibasiclib.TiBasicLib(
    program_name='aaosv4', # TODO automate this
    dependencies=[
        'getbtry',
        'getmem',
        'rspsnie',
    ],
    archive=False,
    ) as tb:

    main_menu = 'main menu'

    with tb.whiletrue(main_menu):

        command = 'Str0'
        tb.inputstr(command, '>>')

        with tb.iff(f'length({command})=0'): # avoid errors related to `=` down the line
            tb.continuee(main_menu)

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

            tb.continuee(main_menu)

        with tb.if_var_equ_strs(command, CMDS_EXIT):
            # TODO implement tb.breakk(main_menu)
            tb.raw('Goto BR')

            tb.continuee(main_menu)

        with tb.if_var_equ_strs(command, CMDS_MEMORY):
            tb.call('getmem')
            # returns free bytes

            free_mem = tb.get_var_num()
            tb.raw(f'{tb.var_ret}->{free_mem}')

            tb.printstr('free memory:')
            tb.printvar(free_mem)

            tb.continuee(main_menu)
        
        with tb.if_var_equ_strs(command, CMDS_RASPISANIE):
            tb.call('rspsnie')

            tb.continuee(main_menu)

        # TODO prgmNOTES

        # TODO prgmOFF

        # TODO prgmTIME

        # TODO prgmTIMESET

        tb.printstr('unknown action:')
        tb.printvar(command)
        tb.printstr('here is the list of actions:')
        tb.printstr(' '.join(['='.join(cmds) for cmds in CMDS_ALL]))

    tb.raw('Lbl BR')
