
import lib_tibasic

# turn off the calculator
# when the calc is powered on functionality will be resumed
# as if nothing happened (opposed to as being restarted)

with lib_tibasic.TiBasicLib(
    ) as tb:

    tb.asm_prgm('''
3E01D303FB76FDCB09A6C9
''')
