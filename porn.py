
import lib_tibasic

with lib_tibasic.TiBasicLib() as tb:

    # constants

    NUMBER_OF_DATA_VARS = tb.MENU_ITEMS_PER_PAGE * 12
    DATA_IN_DATA_VAR = tb.MENU_ITEM_LEN

    DATA_VARS = [f'[list]POD{tb.encode_to_2char(var_idx)}' for var_idx in range(NUMBER_OF_DATA_VARS)]

    # main

    tb.call('porn0')

    # tb.menu(
    #     '"PORN"',
    # )


    for var in DATA_VARS:

        # tb.menu(
        #     'PORN',
        #     [
        #         ...
        #     ],
        #     [
        #         ...
        #     ],
        # )

        tb.print(var)
        tb.del_var(var)
        tb.call('pause')
