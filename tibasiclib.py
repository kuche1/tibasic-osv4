
import subprocess
import inspect
import os
import hashlib
import shutil
import time

# TODO
# check if the file ends with new line and if that is the case delete it
# try `expr(` for string to num conversion
# add parameters for input and output variables

# INFO
# ti84+ ROM: 404     KB
# ti84+ RAM:  16_354  B

def term(cmds:list, silent=False):
    if silent:
        subprocess.run(cmds, check=True, capture_output=True)
    else:
        subprocess.run(cmds, check=True)

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
    in_use = False
    var_count = 0
    name = None

class TiBasicLib:

    # display

    disp_len_x = 16

    # variables

    label_count = 0

    vars_str = ['Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9']
    vars_str_in_use = [False] * len(vars_str)
    vars_str_used_in_this_scope = []

    # vars_num = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    # vars_num_in_use = [False] * len(vars_num)
    # vars_num_used_in_this_scope = []

    # variables used for args, return, trash

    var_arg_str_0 = 'Str9'

    var_ret_num_0 = 'Z'
    var_ret_list_0 = 'L6'

    var_trash_num_0 = 'Y'

    # stack

    stack = []
    stack_num = 0 # used for youngest stack

    # functions stuff

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
        s.previously_sent_file = f'{s.tibasic_source_file}-previously-sent' # needs tp be >8 characters long
        s.previously_sent_file_max_mtime_diff = 60 * 25 # in seconds

        s.archive = archive
        s.archive_if_that_big = 500 # (bytes)
                                    # if `s.archive` is set to None and if the compiled binary is at least this big it will be archived
                                    # note that this is not an accurate representation of the size the program will take on the calc

        s.context_manager = ContextManager(s, lambda:0)

    def __enter__(s):
        s.context_manager.__enter__()
        return s

    def __exit__(s, exc_type, exc_value, exc_traceback):
        s.context_manager.__exit__(exc_type, exc_value, exc_traceback)

        s.f.close()

        if exc_type == None: # if no exceptions

            # compile
            while True:
                print(f'`{s.program_name}`: compiling')
                cmd = ['ti84cc']
                if s.archive:
                    cmd += ['-a']
                cmd += ['-o', s.compiled_file, s.tibasic_source_file]
                term(cmd)

                if s.archive == None:
                    compiled_binary_size = os.path.getsize(s.compiled_file)
                    print(f'`{s.program_name}`: compiled binary size is `{compiled_binary_size}` bytes')
                    if compiled_binary_size >= s.archive_if_that_big:
                        print(f'`{s.program_name}`: compiled binary size is >= `{s.archive_if_that_big}` bytes; archive flag will be set')
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
                print(f'`{s.program_name}`: skipping sending')
            else:
                # send to calc
                print(f'`{s.program_name}`: sending to calc')
                try:
                    term(['tilp', '--no-gui', '--silent', s.compiled_file], silent=True)
                except subprocess.CalledProcessError:
                    print(f'ERROR: could not send `{s.program_name}`')
                else:
                    shutil.copyfile(s.compiled_file, s.previously_sent_file)

    # asserts

    def _assert_str(s, text):
        assert type(text) == str
        assert '"' not in text

    # IO

    def printstr(s, text):
        s._assert_str(text)

        while text:
            part = text[:s.disp_len_x]
            text = text[len(part):]
            s.raw(f'Disp "{part}') # save 1 char by ommiting `"`
        
    # TODO what is var is bigger than screen len
    def printvar(s, var):
        if len(var) == 1:
            assert var == var.upper()
        s.raw(f'Disp {var}')

    def input(s, store_in, prompt_str=None):
        to_write = ''

        to_write += 'Input '

        if prompt_str != None:
            s._assert_str(prompt_str)

            while len(prompt_str) > s.disp_len_x:
                s.printstr(prompt_str[:s.disp_len_x])
                prompt_str = prompt_str[s.disp_len_x:]

            to_write += f'"{prompt_str}",'

        to_write += f'{store_in}'

        s.raw(to_write)

    # control flow

    def label(s, label):
        # TODO since we're doing this in an idiotic manner we can actually check
        # if a label has been declared twice (or a custom name has been given)
        label = label.upper()
        s.raw(f'Lbl {label}')

    def goto(s, label):
        label = label.upper()
        s.raw(f'Goto {label}')
    
    # TODO would be awesome if we could find a way to check if only 1 line of code is in the if
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
    
    def call(s, program_name, asm=False):

        dependencies = ['unarcprg', 'doarcprg'] + [program_name] # program name has to be the last item
        for file in dependencies:
            try:
                dep_module = __import__(file) # note that python will take care of double includes
            except ModuleNotFoundError:
                raise Exception(f'could not find program `{file}`')

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

    def menu_raw(s, title, options, labels):
        assert len(options) <= 7

        labels = [lbl.upper() for lbl in labels]

        code = f'Menu({title}'
        for opt, lab in zip(options, labels, strict=True):
            code += f',{opt},{lab}'

        s.raw(code)
    
    def menu(s, title, options, labels):
        assert len(options) == len(labels)

        if len(options) <= 7:
            return s.menu_raw(title, options, labels)

        lbl_page_0 = s.get_label()
        lbl_page_1 = s.get_label()

        s.label(lbl_page_0)
        s.menu_raw(
            title, # TODO? add page num
            options[:6] + ['"* NEXT"'],
            labels[:6] + [lbl_page_1],
        )
        options = options[6:]
        labels = labels[6:]

        s.label(lbl_page_1)
        s.menu_raw(
            title,
            options[:6] + ['"* PREV"'],
            labels[:6] + [lbl_page_0],
        )

        options = options[6:]
        labels = labels[6:]

        assert len(options) == 0, f'I am increadibly lazy; this needs to be fixed'

    def press_any_key(s):
        s.printstr('PRESS ANY KEY')
        s.raw('Repeat Ans')
        s.raw('getKey')
        s.raw('End')

    # date and time

    def date_get(s, var_out):
        assert var_out in s.vars_str
        s.raw(f'getDtStr(3->{var_out}')

    def date_set(s, var_year, var_month, var_day):
        s.raw(f'setDate({var_year},{var_month},{var_day}')
    
    def time_get(s, var_out):
        assert var_out in s.vars_str
        s.raw(f'getTmStr(24->{var_out}')
    
    def time_set(s, var_hour, var_minute, var_second):
        s.raw(f'setTime({var_hour},{var_minute},{var_second}')
    
    def utime_sec(s, var_num):
        s.raw(f'startTmr->{var_num}')

    # variable generation and scopes

    def get_label(s):
        assert s.label_count <= 99, 'time to fix this'
        ret = str(s.label_count)
        s.label_count += 1
        return ret

    def _get_var(s, vars, vars_in_use, vars_used_in_scope):
        if False not in vars_in_use:
            raise Exception('all vars used; time to implement a stack :(')
        idx = vars_in_use.index(False)
        vars_in_use[idx] = True
        vars_used_in_scope[-1].append(idx)
        return vars[idx]

    def get_var_num(s):
        # return s._get_var(s.vars_num, s.vars_num_in_use, s.vars_num_used_in_this_scope)
        return s.get_var_num_stack()

    def get_var_str(s):
        # TODO maybe we could use Str9, Str8 to save the prev value of Str0, Str1 when requested this way
        # and we could restore it on scope exit
        return s._get_var(s.vars_str, s.vars_str_in_use, s.vars_str_used_in_this_scope)

    def _create_new_scope(s):
        # s.vars_num_used_in_this_scope.append([])
        s.vars_str_used_in_this_scope.append([])
        s.stack.append(StackInfo())
        s.stack_num += 1

    def _delete_last_scope(s):
        # for var_idx in s.vars_num_used_in_this_scope[-1]:
        #     assert s.vars_num_in_use[var_idx] == True
        #     s.vars_num_in_use[var_idx] = False
        # del s.vars_num_used_in_this_scope[-1]

        for var_idx in s.vars_str_used_in_this_scope[-1]:
            assert s.vars_str_in_use[var_idx] == True
            s.vars_str_in_use[var_idx] = False
        del s.vars_str_used_in_this_scope[-1]

        stack = s.stack[-1]
        if stack.in_use:
            s.del_var(stack.name)
        del s.stack[-1]
    
    def scope(s):
        return ContextManager(s, lambda:0)
    
    def get_var_num_stack(s): # these vars don't really seem slower than the regular `A`, `B`, `C`, ...
        stack = s.stack[-1]

        if not stack.in_use:
            stack.in_use = True
            assert len(str(s.stack_num)) <= 4, 'too many stacks, this can be fixed by not abusing `s.stack_num`'
            stack.name = f'[list]S{s.stack_num}'

            s.raw(f'SetUpEditor {stack.name}') # TODO check if this is needed
            # create list if it doesn't exist
            # this will also unarchive it if it is archived

        stack.var_count += 1 # tibasic starts count at 1
        ret = f'{stack.name}({stack.var_count})'

        return ret
    
    def del_var(s, var):
        s.raw(f'DelVar {var}')

    # other

    def raw(s, code, end='\n'):
        s.f.write(code)
        s.f.write(end)
    
    def asm_prgm(s, code):
        s.raw('AsmPrgm', end='')
        code = code.replace('\n', '')
        code = code.replace('\t', '')
        code = code.replace(' ', '')
        s.raw(code, end='')

