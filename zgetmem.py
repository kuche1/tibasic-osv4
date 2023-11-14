
import lib_tibasic

# return in Ans

with lib_tibasic.TiBasicLib(
        archive=False, # must be false, otherwise the return value will be lost
    ) as tb:

    tb.asm_prgm('''
EFE542EF9247EF5641EFBF4AC9
''')
