
import lib_tibasic

# returns free bytes

# output: tb.VAR_RET_NUM[0]

with lib_tibasic.TiBasicLib(
    ) as tb:

    tb.call('zgetmem', asm=True)
    tb.raw(f'Ans->{tb.VAR_RET_NUM[0]}')
