
import lib_tibasic
import porn

with lib_tibasic.TiBasicLib(
        archive=True,
    ) as tb:

    for var in porn.DATA_VARS:
        chunk = porn.the_story[:porn.DATA_IN_DATA_VAR]
        porn.the_story = porn.the_story[len(chunk):]
        if len(chunk) == 0:
            break

        chunk = tb.pystr_to_lstr(chunk)
        # chunk = tb.pystr_to_str(chunk)

        tb.raw(f'{chunk}->{var}')
