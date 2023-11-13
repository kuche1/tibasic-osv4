
import tibasiclib

with tibasiclib.TiBasicLib(
    ) as tb:

    start = tb.get_var_num()
    end = tb.get_var_num()
    diff = tb.get_var_num()

    tb.utime_sec(start)

    tmp = tb.get_var_str()
    tb.input(tmp, 'PRESS ENTER')

    tb.utime_sec(end)

    tb.raw(f'{end}-{start}->{diff}')

    tb.printvar(diff)
