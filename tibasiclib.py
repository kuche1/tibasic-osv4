
import subprocess
import inspect
import os

# TODO
# check if the file ends with new line and if that is the case delete it

def term(cmds:list):
    subprocess.run(cmds, check=True)

class ContextManager:
    def __init__(s, tibasicobj, on_exit):
        s.on_exit = on_exit
        s.tibasicobj = tibasicobj
    def __enter__(s):
        s.tibasicobj._create_new_scope()
        return s
    def __exit__(s, exc_type, exc_value, exc_traceback):
        if exc_type == None: # if not exceptions
            s.on_exit()
            s.tibasicobj._delete_last_scope()

class TiBasicLib:

    # display

    disp_len_x = 16

    # variables

    label_count = 0

    vars_str = ['Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9']
    vars_str_in_use = [False] * len(vars_str)
    vars_str_used_in_this_scope = []

    vars_num = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']
    vars_num_in_use = [False] * len(vars_num)
    vars_num_used_in_this_scope = []

    var_ret = 'Z'

    # functions stuff

    def __init__(s, archive=True):
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

        s.archive = archive

        s.context_manager = ContextManager(s, lambda:0)
        s.labels = []

    def __enter__(s):
        s.context_manager.__enter__()
        return s

    def __exit__(s, exc_type, exc_value, exc_traceback):
        s.context_manager.__exit__(exc_type, exc_value, exc_traceback)

        s.f.close()
        if exc_type == None: # if no exceptions
            # compile
            cmd = ['ti84cc']
            if s.archive:
                cmd += ['-a']
            cmd += ['-o', s.compiled_file, s.tibasic_source_file]
            term(cmd)
            # send to calc
            term(['tilp', '--no-gui', '--silent', s.compiled_file])

    # IO

    def printstr(s, text):
        assert '"' not in text

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
            assert '"' not in prompt_str

            while len(prompt_str) > s.disp_len_x:
                s.printstr(prompt_str[:s.disp_len_x])
                prompt_str = prompt_str[s.disp_len_x:]

            to_write += f'"{prompt_str}",'

        to_write += f'{store_in}'

        s.raw(to_write)

    # control flow

    def label(s, name):
        if name not in s.labels:
            s.labels.append(name)
        name = s.labels.index(name)
        s.raw(f'Lbl {name}')

    def goto(s, label):
        name = s.labels.index(label)
        s.raw(f'Goto {name}')
    
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

        dependencies = ['unarcprg', 'doarcprg'] + [program_name]
        for file in dependencies:
            try:
                # note that python will take care of double includes
                __import__(file)
            except ModuleNotFoundError:
                raise Exception(f'could not find program `{file}`')

        program_name = program_name.upper()

        if not asm:
            s.raw(f'"{program_name}') # set Ans
            s.raw('prgmUNARCPRG')

        if asm:
            s.raw(f'Asm(', end='') # save 1 char by ommiting `)`
        s.raw(f'prgm{program_name}')

        if not asm:
            s.raw(f'"{program_name}') # set Ans
            s.raw('prgmDOARCPRG')

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

    # variable generation

    def get_label(s):
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
        # if False not in s.vars_num_in_use:
        #     raise Exception('all vars used; time to implement a stack :(')
        # idx = s.vars_num_in_use.index(False)
        # s.vars_num_in_use[idx] = True
        # s.vars_num_used_in_this_scope[-1].append(idx)
        # return s.vars_num[idx]
        return s._get_var(s.vars_num, s.vars_num_in_use, s.vars_num_used_in_this_scope)
    
    def get_var_str(s):
        return s._get_var(s.vars_str, s.vars_str_in_use, s.vars_str_used_in_this_scope)

    def _create_new_scope(s):
        s.vars_num_used_in_this_scope.append([])
        s.vars_str_used_in_this_scope.append([])

    def _delete_last_scope(s):
        for var_idx in s.vars_num_used_in_this_scope[-1]:
            assert s.vars_num_in_use[var_idx] == True
            s.vars_num_in_use[var_idx] = False
        del s.vars_num_used_in_this_scope[-1]

        for var_idx in s.vars_str_used_in_this_scope[-1]:
            assert s.vars_str_in_use[var_idx] == True
            s.vars_str_in_use[var_idx] = False
        del s.vars_str_used_in_this_scope[-1]

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

