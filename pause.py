
import lib_tibasic

with lib_tibasic.TiBasicLib() as tb:

    tb.print_str('"-PRESS ANY KEY-"')
    tb.raw('Repeat Ans')
    tb.raw('getKey')
    tb.raw('End')
