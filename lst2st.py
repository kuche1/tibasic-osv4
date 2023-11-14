
import lib_tibasic
from lib_character_map import CHARACTER_MAP

# info
#   converts list to string

# input : tb.VAR_ARG_LIST[0]
# output: tb.VAR_RET_STR[0]
# trash : tb.VAR_TRASH_NUM[0]

with lib_tibasic.TiBasicLib(
        archive=False, # this fnc is used way too often
    ) as tb:

    vl_in = tb.VAR_ARG_LIST[0]
    vs_out = tb.VAR_RET_STR[0]
    vn = tb.VAR_TRASH_NUM[0]

    tb.raw('" "')
    tb.raw(f'For({vn},1,dim({vl_in}))')
    tb.raw(f'Ans+sub("{CHARACTER_MAP}",{vl_in}({vn}),1)')
    tb.raw('End')

    ##### This is the code that handles what hapens if the str length is 0, however this time I won't allow for such cases
    ##### if strlen is 0 then this is the caller's fault
    # tb.raw('If length(Ans)=0')
    # tb.raw('Then')
    # tb.raw(f'""->{vs_out}')
    # tb.raw('Else')
    # tb.raw(f'sub(Ans,2,length(Ans)-1)->{vs_out}')
    # tb.raw('End')

    tb.raw(f'sub(Ans,2,length(Ans)-1)->{vs_out}')
