
import tibasiclib

# returns free bytes

# output: tb.VAR_RET_NUM[0]

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zgetmem', asm=True)
    tb.raw(f'Ans->{tb.VAR_RET_NUM[0]}')
