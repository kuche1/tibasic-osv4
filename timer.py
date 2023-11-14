
import tibasiclib

with tibasiclib.TiBasicLib(
    ) as tb:

    lbl_reset = tb.gen_label()
    lbl_show = tb.gen_label()
    lbl_exit = tb.gen_label()
    lbl_main_loop = tb.gen_label()

    vn_start = tb.get_var_num_stack()
    vn_now = tb.get_var_num_stack()

    tb.utime_sec(vn_start)

    tb.raw(f'Lbl {lbl_main_loop}')

    tb.menu(
        '"**TIMER**"',
        [
            '"* EXIT"',
            '"RESET"',
            '"SHOW"',
        ],
        [
            lbl_exit,
            lbl_reset,
            lbl_show,
        ],
    )

    tb.raw(f'Lbl {lbl_reset}')
    tb.utime_sec(vn_start)
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_show}')
    tb.utime_sec(vn_now)
    tb.raw(f'{vn_now}-{vn_start}->{vn_now}')
    tb.print_str('"TIME PASSED:"')
    tb.print(vn_now)
    tb.print_str('"SECOND(S)"')
    tb.press_any_key()
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_exit}')
