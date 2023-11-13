
import tibasiclib

# info
#   converts string to list

# input : tb.var_arg_str_0
# output: tb.var_ret_list_0
# trash : tb.var_trash_num_0

with tibasiclib.TiBasicLib() as tb:

    vn = tb.var_trash_num_0
    vs = tb.var_arg_str_0
    vl_out = tb.var_ret_list_0

    # TODO lower case letters are missing
    tb.raw(f'seq(inString("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ :?[theta].,()",sub({vs},{vn},1)),{vn},1,length({vs}))->{vl_out}')
