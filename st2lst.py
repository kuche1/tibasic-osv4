
import tibasiclib
from lib_character_map import CHARACTER_MAP

# info
#   converts string to list

# input : tb.VAR_ARG_STR[0]
# output: tb.VAR_RET_LIST[0]
# trash : tb.VAR_TRASH_NUM[0]

with tibasiclib.TiBasicLib(
        archive=False, # this fnc is used way too often
    ) as tb:

    vs_in = tb.VAR_ARG_STR[0]
    vl_out = tb.VAR_RET_LIST[0]
    vn = tb.VAR_TRASH_NUM[0]

    tb.raw(f'seq(inString({CHARACTER_MAP},sub({vs_in},{vn},1)),{vn},1,length({vs_in}))->{vl_out}')
