
import tibasiclib

# turn off the calculator
# when the calc is powered on functionality will be resumed
# as if nothing happened (opposed to as being restarted)

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.call('zpwroff', asm=True)
