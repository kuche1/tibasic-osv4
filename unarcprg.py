
import lib_tibasic

# input: Ans - string - program name (eg notes)

with lib_tibasic.TiBasicLib(
        archive=False, # THIS MIST NEVER BE ARCHIVED
    ) as tb:

    tb.raw('"E"+Ans')
    tb.call('zunarc', asm=True)
