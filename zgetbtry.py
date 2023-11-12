
import tibasiclib

# return in Ans
# 0:4 <-> low:high

with tibasiclib.TiBasicLib(
        archive=False,
    ) as tb:

    tb.asm_prgm('''
EF6F4C3D280A78FE1E
3805
EF21521808
EFB3503E042001AF
EF8C47EFBF4AC9
''')
