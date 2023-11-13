
import tibasiclib

# input: Ans - string - program name (eg notes)

with tibasiclib.TiBasicLib(
        archive=False, # THIS MIST NEVER BE ARCHIVED
    ) as tb:

    tb.raw('"E"+Ans')
    tb.call('zunarc', asm=True)
