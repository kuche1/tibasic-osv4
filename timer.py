
import tibasiclib

with tibasiclib.TiBasicLib(
    ) as tb:

    lbl_reset = tb.get_label()
    lbl_show = tb.get_label()
    lbl_exit = tb.get_label()
    lbl_main_loop = tb.get_label()

    vn_start = tb.get_var_num()
    vn_now = tb.get_var_num()

    tb.utime_sec(vn_start)

    tb.raw(f'Lbl {lbl_main_loop}')
    tb.raw(f'Menu("**TIMER**","RESET",{lbl_reset},"SHOW",{lbl_show},"EXIT",{lbl_exit}')

    tb.raw(f'Lbl {lbl_reset}')
    tb.utime_sec(vn_start)
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_show}')
    tb.utime_sec(vn_now)
    tb.raw(f'{vn_now}-{vn_start}->{vn_now}')
    tb.printstr('TIME PASSED:')
    tb.printvar(vn_now)
    tb.printstr('SECOND(S)')
    tb.press_any_key()
    tb.raw(f'Goto {lbl_main_loop}')

    tb.raw(f'Lbl {lbl_exit}')
