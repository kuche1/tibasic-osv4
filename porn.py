
import lib_tibasic

with lib_tibasic.TiBasicLib() as tb:

    # constants

    NUMBER_OF_DATA_VARS = 16 * 3
    DATA_IN_DATA_VAR = 16

    DATA_VARS = [f'[list]POD{tb.encode_to_2char(var_idx)}' for var_idx in range(NUMBER_OF_DATA_VARS)]

    # main

    tb.call('porn0')
    for var in DATA_VARS:
        tb.print(var)
        tb.del_var(var)
        tb.call('pause')
