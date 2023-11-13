
import tibasiclib
from lib_character_map import CHARACTER_MAP

# info
#   converts list to string

# input : tb.var_arg_list_0
# output: tb.var_ret_str_0
# trash : tb.var_trash_num_0

with tibasiclib.TiBasicLib() as tb:

    vl_in = tb.var_arg_list_0
    vs_out = tb.var_ret_str_0
    vn = tb.var_trash_num_0

    tb.raw('" "')
    tb.raw(f'For({vn},1,dim({vl_in}))')
    tb.raw(f'Ans+sub({CHARACTER_MAP},{vl_in}({vn}),1)')
    tb.raw('End')

    tb.raw('If length(Ans)=0')
    tb.raw('Then')
    tb.raw(f'""->{vs_out}')
    tb.raw('Else')
    tb.raw(f'sub(Ans,2,length(Ans)-1)->{vs_out}')
    tb.raw('End')