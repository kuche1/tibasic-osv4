
import tibasiclib

# return in Ans

with tibasiclib.TiBasicLib(
    program_name='getmem',
    dependencies=[
        'zgetmem',
    ]
    ) as tb:

    tb.call('zgetmem', asm=True)
