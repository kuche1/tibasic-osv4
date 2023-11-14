
import lib_tibasic

#info
#   unarchives anything

#input - Ans - string - name of var, prefixed with type

# Input: Ans is a string with the name of the variable to archive. The name needs a prefix byte to determine what type of variable it is. Some of them are: 
#
#  and      Real/Complex
# A         List
# B         Matrix
# C         Equation
# D         String
# [         Program/Protected program
# E         Program/Protected program
# F         Program/Protected program
# G         Picture
# H         GDB
# U         Appvar

# For example, to archive prgmTEST, any of these inputs will work: 
#
# "[TEST
# "ETEST
# "FTEST

with lib_tibasic.TiBasicLib(
        archive=False, # THIS MIST NEVER BE ARCHIVED
    ) as tb:

    tb.asm_prgm('''
EFD74AD604C0
EB4E234623
117884EDB0
12EFF142D8
78B7C8
EFD84FC9
''')
