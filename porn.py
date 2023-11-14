
import lib_tibasic

with lib_tibasic.TiBasicLib() as tb:

    tb.call('porn0')
    for var_group in [['Str0', 'Str1', 'Str2', 'Str3', 'Str4'], ['Str5', 'Str6', 'Str7', 'Str8', 'Str9']]:
        for var in var_group:
            tb.print(var)
        tb.call('pause')
    
    for var in ['Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9']:
        tb.del_var(var)
