
import lib_tibasic

with lib_tibasic.TiBasicLib(
    ) as tb:

    lbl_reset = tb.gen_label()
    lbl_show = tb.gen_label()
    lbl_exit = tb.gen_label()
    lbl_main_loop = tb.gen_label()

    vn_start = tb.gen_var_num()
    vn_now = tb.gen_var_num()

    tb.utime_sec(vn_start)

    tb.raw(f'Lbl {lbl_main_loop}')

    tb.menu(
        '"**TIMER**"',
        [
            '"RESET"',
            '"SHOW"',
        ],
        [
            lbl_reset,
            lbl_show,
        ],
    )
    tb.goto(lbl_exit)

    tb.raw(f'Lbl {lbl_reset}')
    tb.utime_sec(vn_start)
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_show}')
    tb.utime_sec(vn_now)
    tb.raw(f'{vn_now}-{vn_start}->{vn_now}')
    tb.print_str('"TIME PASSED:"')
    tb.print(vn_now)
    tb.print_str('"SECOND(S)"')
    tb.call('pause')
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_exit}')
