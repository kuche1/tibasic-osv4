
import tibasiclib

# turn off the calculator
# when the calc is powered on functionality will be resumed
# as if nothing happened (opposed to as being restarted)

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.asm_prgm('''
3E01D303FB76FDCB09A6C9
''')
