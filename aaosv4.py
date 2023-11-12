#! /usr/bin/env python3

# usage: ./aaosv4.py

import tibasiclib

with tibasiclib.TiBasicLib(
    program_name='aaosv4', # TODO automate this
    dependencies=[
        'getbtry',
    ]
    ) as tb:

    main_menu = 'main menu'

    with tb.whiletrue(main_menu):

        command = 'Str0'
        tb.inputstr(command, '>>')

        with tb.iff(f'length({command})=0'): # avoid errors related to `=` down the line
            tb.continuee(main_menu)

        with tb.iff(f'{command}="b"|{command}="B"|{command}="battery"'):
            tb.call('getbtry')
            # return in Ans
            # 0:4 <-> low:high

            low_bound = tb.get_var_num()
            high_bound = tb.get_var_num()

            tb.raw(f'Ans*20->{low_bound}')
            tb.raw(f'{low_bound}+20->{high_bound}')

            tb.printstr('battery between')
            tb.printvar(low_bound)
            tb.printstr('and')
            tb.printvar(high_bound)
            tb.printstr('percent')

            tb.continuee(main_menu)

        tb.printstr('unknown action')
        tb.printvar(command)
