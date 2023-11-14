
import tibasiclib

# returns battery level
# 0:4 <-> low:high

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zgetbtry', asm=True)
    tb.raw(f'Ans->{tb.VAR_RET_NUM[0]}')
