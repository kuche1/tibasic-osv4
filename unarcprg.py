
import tibasiclib

# input: Ans - string - program name (eg notes)

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.raw('"E"+Ans') # we can probably remove the second `"` here but at some point in the future the way that the compiler works might
                      # be changed and this might break something
    tb.call('zunarc', asm=True)
