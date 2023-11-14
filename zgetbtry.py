
import lib_tibasic

# return in Ans
# 0:4 <-> low:high

with lib_tibasic.TiBasicLib(
        archive=False, # must be false, otherwise the return value will be lost
    ) as tb:

    tb.asm_prgm('''
EF6F4C3D280A78FE1E
3805
EF21521808
EFB3503E042001AF
EF8C47EFBF4AC9
''')
