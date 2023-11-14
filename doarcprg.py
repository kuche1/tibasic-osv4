
import lib_tibasic

# input: Ans - string - program name (eg notes)

with lib_tibasic.TiBasicLib(
        archive=False, # THIS MIST NEVER BE ARCHIVED
    ) as tb:

    tb.raw('"E"+Ans') # TODO see if se can remove the second `"`
    tb.call('zdoarc', asm=True)
