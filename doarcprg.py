
import tibasiclib

# input: Ans - string - program name (eg notes)

with tibasiclib.TiBasicLib(
        archive=False, # THIS MIST NEVER BE ARCHIVED
    ) as tb:

    tb.raw('"E"+Ans') # TODO see if se can remove the second `"`
    tb.call('zdoarc', asm=True)
