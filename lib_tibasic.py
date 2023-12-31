
import subprocess
import inspect
import os
import hashlib
import shutil
import time
import sys

from lib_character_map import CHARACTER_MAP_1B_CHARS

# TODO
# check if the file ends with new line and if that is the case delete it
# try `expr(` for string to num conversion
# add parameters for input and output variables

# INFO
# ti84+ ROM: 404     KB
# ti84+ RAM:  24_015  B

def term(cmds:list, silent=False):
    if silent:
        stdout = subprocess.DEVNULL
        stderr = subprocess.DEVNULL
    else:
        stdout = None
        stderr = None

    subprocess.run(cmds, check=True, stdout=stdout, stderr=stderr)

def calc_hash(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest() # TODO sucks for big files

class ContextManager:
    def __init__(s, tibasicobj, on_exit):
        s.on_exit = on_exit
        s.tibasicobj = tibasicobj
    def __enter__(s):
        s.tibasicobj._create_new_scope()
        return s
    def __exit__(s, exc_type, exc_value, exc_traceback):
        if exc_type == None: # if no exceptions
            s.on_exit()
            s.tibasicobj._delete_last_scope()

class StackInfo:
    def __init__(s):
        s.in_use = False
        s.var_count = 0
        s.name = None
        s.allocated_lists = []

class TiBasicLib:

    ##########
    ########## constants
    ##########

    # display

    DISP_LEN_X = 16
    MENU_ITEMS_PER_PAGE = 4
    MENU_ITEM_LEN = 14

    # related to the character map

    DIGIT_TO_LCHAR = CHARACTER_MAP_1B_CHARS.index('0') + 1
    # add that much to a digit (so 0 to 9) and it will be valid to it's equivalent lchar

    # related to the encoding table

    # troublemaker: SS -> removing S
    ENCODE_TABLE = '0123456789ABCDEFGHIJKLMNOPQRTUVWXYZ'
    # if this crashes then we need to add some more characters (unlikely to happen)
    # also it's fine if some if these characters cause touble and we need to remove them

    # variables used for args, return, trash

    VAR_ARG_STR = ['Str9']
    VAR_ARG_LIST = ['L5']

    VAR_RET_NUM = ['Z']
    VAR_RET_STR = ['Str8']
    VAR_RET_LIST = ['L6']

    VAR_TRASH_NUM = ['Y']
    VAR_TRASH_STR = ['Str7', 'Str6', 'Str5', 'Str4', 'Str3']

    ##########
    ########## shared data over different instances
    ##########

    # stack

    stack_num = 0 # used for youngest stack
    stack_var_num = []
    stack_var_lstr = []

    ##########
    ########## functions
    ##########

    def __init__(s, archive=None):
        # get filename of caller
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        file = module.__file__
        file = os.path.basename(file)
        if file.endswith('.py'):
            file = file[:-3]
        program_name = file

        if len(program_name) > 8:
            raise Exception(f'invalid program name `{program_name}`; it needs to be less than or equal to 8 characters')

        s.program_name = program_name
        s.tibasic_source_file = f'/tmp/{s.program_name}.tib' # extension has to be `.tib` otherwise the compiler refuses to work
        s.compiled_file = f'/tmp/{s.program_name}.8xp'
        s.f = open(s.tibasic_source_file, 'w')
        s.previously_sent_file = f'/tmp/{s.program_name}-previously-sent' # needs tp be >8 characters long
        s.previously_sent_file_max_mtime_diff = 60 * 60 * 2 # in seconds

        s.archive = archive
        s.archive_if_that_big = 500 # (bytes)
                                    # if `s.archive` is set to None and if the compiled binary is at least this big it will be archived
                                    # note that this is not an accurate representation of the size the program will take on the calc

        s.context_manager = ContextManager(s, lambda:0)

        s.label_count = 0

    def __enter__(s):
        s.context_manager.__enter__()
        return s

    def __exit__(s, exc_type, exc_value, exc_traceback):
        s.context_manager.__exit__(exc_type, exc_value, exc_traceback)

        s.f.close()

        if exc_type == None: # if no exceptions

            # compile
            while True:
                #print(f'`{s.program_name}`: compiling')
                cmd = ['ti84cc']
                if s.archive:
                    cmd += ['-a']
                cmd += ['-o', s.compiled_file, s.tibasic_source_file]
                term(cmd)

                if s.archive == None:
                    compiled_binary_size = os.path.getsize(s.compiled_file)
                    #print(f'`{s.program_name}`: compiled binary size is `{compiled_binary_size}` bytes')
                    if compiled_binary_size >= s.archive_if_that_big:
                        #print(f'`{s.program_name}`: compiled binary size is >= `{s.archive_if_that_big}` bytes; archive flag will be set')
                        s.archive = True
                    else:
                        s.archive = False
                else:
                    break

            if os.path.isfile(s.previously_sent_file):
                skip = calc_hash(s.compiled_file) == calc_hash(s.previously_sent_file)
                skip = skip and (s.previously_sent_file_max_mtime_diff >= abs(time.time() - os.path.getmtime(s.previously_sent_file)))
            else:
                skip = False

            if skip:
                #print(f'`{s.program_name}`: skipping sending')
                pass
            else:
                # send to calc
                print(f'`{s.program_name}`: sending to calc')
                try:
                    # if anything happens try increasing the timeout
                    # bad  : 16
                    # good?: 32
                    term(['tilp', '--no-gui', '--silent', '--timeout', '32', s.compiled_file], silent=True)
                except subprocess.CalledProcessError:
                    print(f'ERROR: could not send `{s.program_name}`')
                    print('    this usually happens if you manually run TiLP2')
                    print('    try restarting your calculator')
                    sys.exit(1)
                else:
                    shutil.copyfile(s.compiled_file, s.previously_sent_file)

    ##########
    ########## asserts, checks, data extraction [updated]
    ##########

    # string

    def is_str(s, text):
        if text.startswith('"'):
            if text.endswith('"'):
                data = text[1:-1] # this sucks but otherwise we get infinite recursion
                assert '"' not in data, f'using `"` in a string is not allowed: `{text}`'
                return True
            assert False, f'strings that start with `"` but do not end with `"` are not considered valid: `{text}`'
        return False

    def is_var_str(s, var):
        return var in ['Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9']
    
    def is_var_lstr(s, var):
        return s.is_var_list(var)
    
    def extract_str_data(s, data):
        assert s.is_str(data)
        return data[1:-1]
    
    # list

    def is_list(s, var):
        return var.startswith('{') and var.endswith('}')

    def is_var_list(s, var):
        prefix = False

        if var in ['L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6']:
            return True

        if not var.startswith('[list]'):
            return False
        
        if var.endswith(')'): # it's an index of a list, not a list
            return False
        
        return True
    
    # num

    def is_var_num(s, var):
        if var in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            return True
        
        # TODO this sucks, it would be awesome if we could do it without copy-pasting
        for start in ['[list]', 'L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6']:
            if var.startswith(start):
                break
        else:
            return False

        # TODO we can improve the format checks

        return var.endswith(')')

    ##########
    ########## Output [updated]
    ##########

    # print

    def print(s, atom):
        if s.is_str(atom):
            return s.print_str(atom)

        if s.is_var_str(atom):
            return s.print_var_str(atom)

        if s.is_var_lstr(atom):
            return s.print_var_lstr(atom)

        if s.is_var_num(atom):
            return s.print_var_num(atom)
        
        assert False, f'could not determine type of `{atom}`'
    
    # TODO add a check for lower case letters
    # and turn them into upper case if a PM optimisation flag has been set
    def print_str(s, data):
        assert s.is_str(data)

        data = s.extract_str_data(data)

        while len(data) > s.DISP_LEN_X:
            chunk = data[:s.DISP_LEN_X]
            data = data[s.DISP_LEN_X:]

            s.raw(f'Disp "{chunk}') # save 1 char
        
        s.raw(f'Disp "{data}') # save 1 char

    def print_var_lstr(s, var):
        assert s.is_var_lstr(var)

        s.raw(f'{var}->{s.VAR_ARG_LIST[0]}')

        s.call('lst2st')
        # input : tb.VAR_ARG_LIST[0]
        # output: tb.VAR_RET_STR[0]
        # trash : tb.VAR_TRASH_NUM[0]

        s.print(s.VAR_RET_STR[0])

    def print_var_num(s, var):
        assert s.is_var_num(var)
        s.raw(f'Disp {var}')
    
    def print_var_str(s, var):
        assert s.is_var_str(var)
        s.raw(f'Disp {var}')

    ##########
    ########## Input [updated]
    ##########

    def input(s, store, prompt, ut14c=False): # TODO maybe we could rename `ut14c` to something less hardcoded
        if s.is_var_num(store):
            return s.input_var_num(store, prompt, ut14c=ut14c)
        elif s.is_var_str(store):
            return s.input_var_str(store, prompt, ut14c=ut14c)
        elif s.is_var_lstr(store):
            return s.input_var_lstr(store, prompt, ut14c=ut14c)
        else:
            assert False, f'unsupported data type of `{store}`'
    
    def input_var_num(s, var, prompt, ut14c=False):
        assert s.is_var_num(var)
        return s._input_raw(var, prompt, ut14c=ut14c)

    def input_var_str(s, var, prompt, ut14c=False):
        assert s.is_var_str(var)
        return s._input_raw(var, prompt, ut14c=ut14c)
    
    def input_var_lstr(s, var, prompt, ut14c=False): # TODO rename to input_var_lstr
        assert s.is_var_lstr(var)

        vs = s.VAR_TRASH_STR[0]
        s.input_var_str(vs, prompt, ut14c=ut14c)

        s.raw(f'{vs}->{s.VAR_ARG_STR[0]}')

        s.call('st2lst')
        # input : tb.VAR_ARG_STR[0]
        # output: tb.VAR_RET_LIST[0]
        # trash : tb.VAR_TRASH_NUM[0]

        s.raw(f'{s.VAR_RET_LIST[0]}->{var}')

    def _input_raw(s, raw, prompt, ut14c=False):
        if ut14c:
            ut14c = False
            s.print('"VVVVVVVVVVVVVVXX"') # TODO absolutely idiotic; adding some trimming wouldn't be bad
            return s._input_raw(raw, prompt, ut14c=ut14c)

        if s.is_str(prompt):
            data = s.extract_str_data(prompt)
            while len(data) > s.DISP_LEN_X:
                chunk = data[:s.DISP_LEN_X]
                data = data[s.DISP_LEN_X:]
                s.print(f'"{chunk}"')
            prompt = f'"{data}"' # cannot save 1 char here TODO or can we?
        elif s.is_var_str(prompt):
            pass
        else:
            assert False, f'unsupported data type of `{prompt}`'

        s.raw(f'Input {prompt},{raw}')

    ##########
    ########## Menu
    ##########

    def menu(s, title, options, labels):
        assert len(options) == len(labels)
  
        TRASH_VARS_USED_FOR_OPTIONS = s.VAR_TRASH_STR[:s.MENU_ITEMS_PER_PAGE]
        TRASH_VAR_USED_FOR_TITLE    = s.VAR_TRASH_STR[s.MENU_ITEMS_PER_PAGE]

        # if len(options) <= 7:
        #     if all([s.is_str(opt) and s.is_var_str(opt) for opt in options]):
        #         return s.menu_raw(title, options, labels)

        if s.is_var_lstr(title):
            s.raw(f'{title}->{s.VAR_ARG_LIST[0]}')

            s.call('lst2st')
            # input : tb.VAR_ARG_LIST[0]
            # output: tb.VAR_RET_STR[0]
            # trash : tb.VAR_TRASH_NUM[0]

            s.raw(f'{s.VAR_RET_STR[0]}->{TRASH_VAR_USED_FOR_TITLE}')

            title = TRASH_VAR_USED_FOR_TITLE
        
        elif s.is_str(title):
            pass
        elif s.if_var_str(title):
            pass
        else:
            assert False, f'unsupported data type of `{title}`'

        lbl_page_cur = s.gen_label()
        lbl_page_prev = lbl_page_cur

        lbl_exit = s.gen_label()

        while len(options):
            if len(options) <= s.MENU_ITEMS_PER_PAGE:
                lbl_page_next = lbl_page_cur
                str_next = '"X NEXT"'
            else:
                lbl_page_next = s.gen_label()
                str_next = '"* NEXT"'

            if lbl_page_prev == lbl_page_cur:
                str_prev = '"X PREV"'
            else:
                str_prev = '"* PREV"'

            s.label(lbl_page_cur)

            options_slice = options[:s.MENU_ITEMS_PER_PAGE]
            labels_slice  = labels [:s.MENU_ITEMS_PER_PAGE]

            for idx, opt in enumerate(options_slice):
                if s.is_str(opt):
                    pass
                elif s.is_var_str(opt):
                    pass
                elif s.is_var_list(opt):
                    s.raw(f'{opt}->{s.VAR_ARG_LIST[0]}')

                    s.call('lst2st')
                    # input : tb.VAR_ARG_LIST[0]
                    # output: tb.VAR_RET_STR[0]
                    # trash : tb.VAR_TRASH_NUM[0]

                    s.raw(f'{s.VAR_RET_STR[0]}->{TRASH_VARS_USED_FOR_OPTIONS[idx]}')

                    options_slice[idx] = TRASH_VARS_USED_FOR_OPTIONS[idx]
                else:
                    assert False, f'unsupported type of `{opt}`'

            s._menu_raw(
                title, # TODO? add page num
                ['"* EXIT"', str_prev,      str_next]      + options_slice,
                [lbl_exit,   lbl_page_prev, lbl_page_next] + labels_slice,
            )
            options = options[len(options_slice):]
            labels  = labels [len(labels_slice):]

            lbl_page_prev = lbl_page_cur
            lbl_page_cur = lbl_page_next
        
        s.label(lbl_exit) # TODO not optimal, we can optimize away this label

    def _menu_raw(s, title, options, labels):
        if s.is_str(title):
            data = s.extract_str_data(title)
            if len(data) > s.DISP_LEN_X:
                print(f'WARNING: menu title will clip `{title}`')
        elif s.is_var_str(title):
            pass
        else:
            assert False, f'unsupported type of `{title}`'
    
        assert len(options) <= 7
        for opt in options:
            if s.is_str(opt):
                data = s.extract_str_data(opt)
                if len(data) > s.MENU_ITEM_LEN:
                    print(f'WARNING: menu item will clip `{opt}`')
            elif s.is_var_str(opt):
                pass
            else:
                assert False, f'unsupported type of `{opt}`'

        labels = [lbl.upper() for lbl in labels]

        code = f'Menu({title}'
        for opt, lab in zip(options, labels, strict=True):
            code += f',{opt},{lab}'

        s.raw(code)

    ##########
    ########## control flow
    ##########

    def label(s, label):
        # TODO since we're doing this in an idiotic manner we can actually check
        # if a label has been declared twice (or a custom name has been given)
        label = label.upper()
        s.raw(f'Lbl {label}')

    def goto(s, label):
        label = label.upper()
        s.raw(f'Goto {label}')
    
    # TODO would be awesome if we could find a way to check if only 1 line of code is in the if
    # i vsu6tnost moje ako proverim kolko novi reda sa zapisani v faila sprqmo posledniq put
    def iff(s, cond):
        s.raw(f'If {cond}')
        s.raw('Then')
        return ContextManager(s, lambda:s.raw('End'))
    
    def if_var_equ_strs(s, var, strings):
        assert type(strings) == list
        cond = ''
        for string in strings:
            cond += f'{var}="{string}"|'
        if cond.endswith('|'):
            cond = cond[:-1]
        return s.iff(cond)

    def whiletrue(s, label):
        s.label(label)
        return ContextManager(s, lambda:s.goto(label))

    def continuee(s, label):
        s.goto(label)
    
    def call(s, program_name, asm=False, cd=None):

        dependencies = ['unarcprg', 'doarcprg'] + [program_name] # program name has to be the last item
        cds          = [None,       None]       + [cd]
        for file, cd in zip(dependencies, cds, strict=True):

            try:
                sys.path.append(cd)

                try:
                    dep_module = __import__(file) # note that python will take care of double includes
                except ModuleNotFoundError:
                    raise Exception(f'could not find program `{file}`')
            
            finally:
                del sys.path[-1]

            dep_tb = dep_module.tb # TODO this can crash (but it's a nice check)

        program_name = program_name.upper()

        if dep_tb.archive:
            s.raw(f'"{program_name}') # set Ans
            s.raw('prgmUNARCPRG')

        if asm:
            s.raw(f'Asm(', end='')
        s.raw(f'prgm{program_name}')

        if dep_tb.archive:
            s.raw(f'"{program_name}') # set Ans
            s.raw('prgmDOARCPRG')

    ##########
    ########## date and time [legacy]
    ##########

    def date_set(s, var_year, var_month, var_day):
        s.raw(f'setDate({var_year},{var_month},{var_day}')
    
    def time_set(s, var_hour, var_minute, var_second):
        s.raw(f'setTime({var_hour},{var_minute},{var_second}')
    
    def utime_sec(s, var_num):
        s.raw(f'startTmr->{var_num}')

    ##########
    ########## date and time [updated]
    ##########

    def date_get(s, var):
        if s.is_var_num(var):
            assert False, 'not implemented yet'

        elif s.is_var_str(var):
            return s.raw(f'getDtStr(3->{var}')

        elif s.is_var_lstr(var):
            s.date_get(s.VAR_TRASH_STR[0])

            s.raw(f'{s.VAR_TRASH_STR[0]}->{s.VAR_ARG_STR[0]}')

            s.call('st2lst')
            # input : tb.VAR_ARG_STR[0]
            # output: tb.VAR_RET_LIST[0]
            # trash : tb.VAR_TRASH_NUM[0]

            s.raw(f'{s.VAR_RET_LIST[0]}->{var}')

        else:
            assert False, f'unsupported data type of `{var}`'

    def time_get(s, var):
        if s.is_var_str(var):
            return s.raw(f'getTmStr(24->{var}')

        elif s.is_var_lstr(var):
            s.time_get(s.VAR_TRASH_STR[0])

            s.raw(f'{s.VAR_TRASH_STR[0]}->{s.VAR_ARG_STR[0]}')

            s.call('st2lst')
            # input : tb.VAR_ARG_STR[0]
            # output: tb.VAR_RET_LIST[0]
            # trash : tb.VAR_TRASH_NUM[0]

            s.raw(f'{s.VAR_RET_LIST[0]}->{var}')

        else:
            assert False, f'unsuported data type of `{var}`'

    ##########
    ########## variable generation, deletion and scopes
    ##########

    def gen_label(tb):
        ret = tb.encode_to_2char(tb.label_count)
        tb.label_count += 1
        return ret

    def _create_new_scope(s):
        s.stack_var_num.append(StackInfo())
        s.stack_var_lstr.append(StackInfo())
        s.stack_num += 1

    def _delete_last_scope(s):
        stack = s.stack_var_num[-1]
        if stack.in_use:
            for l in stack.allocated_lists:
                s.del_var(l)
        del s.stack_var_num[-1]

        stack = s.stack_var_lstr[-1] # TODO copy-paste
        if stack.in_use:
            for l in stack.allocated_lists:
                s.del_var(l)
        del s.stack_var_lstr[-1]
    
    def scope(s):
        return ContextManager(s, lambda:0)
    
    def gen_var_num(s): # these vars don't really seem slower than the regular `A`, `B`, `C`, ...
        stack = s.stack_var_num[-1]

        if not stack.in_use:
            stack.in_use = True
            num = s.encode_to_1char(s.stack_num) # if you get an error here you can either: (1: stop abusibng `s.stack_num`) (2: extend the 1char encoder) (3: use a 2char encoder)
            stack.name = f'[list]S{num}'
            stack.allocated_lists.append(stack.name)
        stack.var_count += 1 # tibasic starts count at 1
        num = s.encode_to_1char(stack.var_count)
        ret = f'{stack.name}({num})'

        return ret
    
    def gen_var_lstr(s): # TODO copy-pasta
        stack = s.stack_var_lstr[-1]

        if not stack.in_use:
            stack.in_use = True
            num = s.encode_to_1char(s.stack_num) # if you get an error here you can either: (1: stop abusibng `s.stack_num`) (2: extend the 1char encoder) (3: use a 2char encoder)
            stack.name = f'[list]T{num}'
        stack.var_count += 1 # tibasic starts count at 1
        num = s.encode_to_1char(stack.var_count)
        ret = f'{stack.name}{num}'
        stack.allocated_lists.append(ret)

        return ret
    
    def del_var(s, var):
        s.raw(f'DelVar {var}')
    
    def setupeditor(s, var):
        # creates variable if it doesn't exist
        # also unarchives it if it is archived
        s.raw(f'SetUpEditor {var}')
    
    def setupeditor_lstr(s, var):
        # length will be set to 1

        s.setupeditor(var)

        s.raw(f'If dim({var})=0')
        s.raw(f'1->{var}(1)')
    
    def encode_to_1char(s, num):
        # returns an encoded version of the input that can be used in variable names
        assert type(num) == int
        assert num >= 0
        assert num < len(s.ENCODE_TABLE), f'cannot encode `{num}` into a single character; use 2char encoding instead'
        return s.ENCODE_TABLE[num]
    
    def encode_to_2char(tb, num):
        assert type(num) == int
        assert num >= 0

        num_high = int(num / len(tb.ENCODE_TABLE))
        num_low = num - (num_high * len(tb.ENCODE_TABLE))

        num_high = tb.encode_to_1char(num_high)
        num_low = tb.encode_to_1char(num_low)

        return num_high + num_low

    ##########
    ########## lists
    ##########

    # NOTE don't use this for appending a single element since this is way too slow, in that case use http://tibasicdev.wikidot.com/augment
    def lst_cat(s, store_in, list1, list2):
        assert s.is_var_list(list1) or s.is_list(list1)
        assert s.is_var_list(list2) or s.is_list(list2)
        s.raw(f'augment({list1},{list2})->{store_in}')

    ##########
    ########## pystr
    ##########

    def pychar_to_lchar(tb, pychar):
        assert type(pychar) == str
        assert len(pychar) == 1
        idx = CHARACTER_MAP_1B_CHARS.find(pychar)
        if idx == -1:
            assert False, f'could not convert pychar `{pychar}` to lchar; character is missing from character table'
        idx += 1 # tibasic is 1-indexed
        return str(idx)

    def pystr_to_lstr(tb, pystr):
        assert type(pystr) == str
        res = '{'
        for char in pystr:
            lchar = tb.pychar_to_lchar(char)
            res += lchar
            res += ','
        if res.endswith(','):
            res = res[:-1]
        res += '}'
        return res
    
    def pystr_to_str(tb, pystr):
        assert type(pystr) == str
        assert '"' not in pystr
        return f'"{pystr}"'

    ##########
    ########## memory related
    ##########

    def archive_var(s, var):
        s.raw(f'Archive {var}')
    
    def garbage_collect(s):
        s.raw('GarbageCollect')

    ##########
    ########## other
    ##########

    def raw(s, code, end='\n'):
        s.f.write(code)
        s.f.write(end)
    
    def asm_prgm(s, code):
        s.raw('AsmPrgm', end='')
        code = code.replace('\n', '')
        code = code.replace('\t', '')
        code = code.replace(' ', '')
        s.raw(code, end='')
    
    def digit_to_lchar(s, output_var, input_var):
        if s.is_var_num(input_var):
            pass
        else:
            assert False, f'unsupported type `{input_var}`' # TODO add support for regular digits
        
        assert s.is_var_num(output_var)

        s.raw(f'{input_var}+{s.DIGIT_TO_LCHAR}->{output_var}')

    def num0to99_to_lstr(tb, out, inp):
        assert tb.is_var_num(inp)
        assert tb.is_var_lstr(out)

        vn_high = tb.gen_var_num()
        vn_low = tb.gen_var_num()

        tb.raw(f'int({inp}/10)->{vn_high}')
        tb.digit_to_lchar(f'{out}(1)', vn_high)

        tb.raw(f'{inp}-10*{vn_high}->{vn_low}')
        tb.digit_to_lchar(f'{out}(2)', vn_low)
