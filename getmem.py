
import tibasiclib

# returns free bytes

with tibasiclib.TiBasicLib(
    program_name='getmem',
    ) as tb:

    tb.call('zgetmem', asm=True)
    tb.raw(f'Ans->{tb.var_ret}')
