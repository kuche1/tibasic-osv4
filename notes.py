
import tibasiclib

with tibasiclib.TiBasicLib() as tb:

    tb.input(tb.var_arg_str_0, 'idkman:')

    tb.call('st2lst')
    # input : tb.var_arg_str_0
    # output: tb.var_ret_list_0
    # trash : tb.var_trash_num_0

    tb.raw(f'{tb.var_ret_list_0}->{tb.var_arg_list_0}')

    tb.call('lst2st')
    # input : tb.var_arg_list_0
    # output: tb.var_ret_str_0
    # trash : tb.var_trash_num_0

    tb.printvar(tb.var_ret_str_0)

    tb.press_any_key()
