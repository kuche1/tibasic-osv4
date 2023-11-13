
import tibasiclib

# return in Ans

with tibasiclib.TiBasicLib(
        archive=False, # must be false, otherwise the return value will be lost
    ) as tb:

    tb.asm_prgm('''
EFE542EF9247EF5641EFBF4AC9
''')
