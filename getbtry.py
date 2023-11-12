
import tibasiclib

# return in Ans
# 0:4 <-> low:high

with tibasiclib.TiBasicLib(
    program_name='getbtry',
    dependencies=[
        'zgetbtry',
    ]
    ) as tb:

    tb.call('zgetbtry', asm=True)
