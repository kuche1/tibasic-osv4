
import tibasiclib

# returns free bytes

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zgetmem', asm=True)
    tb.raw(f'Ans->{tb.VAR_RET_NUM[0]}')
