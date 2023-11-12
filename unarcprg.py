
import tibasiclib

# input: Ans - string - program name (eg notes)

with tibasiclib.TiBasicLib(
        archive=False,
    ) as tb:

    tb.raw('"E"+Ans') # TODO see if se can remove the second `"`
    tb.call('zunarc', asm=True)
