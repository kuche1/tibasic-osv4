
import tibasiclib

# returns free bytes

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zgetmem', asm=True)
    tb.raw(f'Ans->{tb.var_ret_num_0}')
