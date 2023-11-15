
# NOTE 1B and multibyte referes to python bytes, not ti84+ bytes
# so that we can easily index characters

# NOTE if you are to add new characters append them to the end so that we don't loose backwards compatibility
# if you are to add a 1B character, them we'll loose backwards compatibility for the multibyte chars (code will be moved by 1)
# oh well...

# TODO? add lower case letters?

numbers = '0123456789'
letters_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters_lower_case = 'abcdefghijklmnopqrstuvwxyz'
expansion_0 = ' /:?.,()<>!\'-'

CHARACTER_MAP_1B_CHARS = numbers + letters_capital + letters_lower_case + expansion_0
CHARACTER_MAP_MULTIBYTE_CHARS = '[theta]'
CHARACTER_MAP = CHARACTER_MAP_1B_CHARS + CHARACTER_MAP_MULTIBYTE_CHARS
