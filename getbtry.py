
import tibasiclib

# returns battery level
# 0:4 <-> low:high
# output: tb.VAR_RET_NUM[0]

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zgetbtry', asm=True)
    tb.raw(f'Ans->{tb.VAR_RET_NUM[0]}')
