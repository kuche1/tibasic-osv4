
import subprocess

# TODO
# check if the file ends with new line and if that is the case delete it

def term(cmds:list):
    subprocess.run(cmds, check=True)

class ContextManager:
    def __init__(s, on_exit):
        # s.on_etner = on_enter
        s.on_exit = on_exit
    def __enter__(s):
        # s.on_enter()
        return s
    def __exit__(s, exc_type, exc_value, exc_traceback):
        if exc_type == None: # if not exceptions
            s.on_exit()

class TiBasicLib:

    # constants

    disp_len_x = 16

    str_regs = ['Str0', 'Str1', 'Str2', 'Str3', 'Str4', 'Str5', 'Str6', 'Str7', 'Str8', 'Str9']
    # can't put `Ans` here

    # python stuff

    def __init__(s, program_name, dependencies):
        if len(program_name) > 8:
            raise Exception(f'invalid program name `{program_name}`; it needs to be less than or equal to 8 characters')

        s.program_name = program_name
        s.tibasic_source_file = f'/tmp/{s.program_name}.tib' # extension has to be `.tib` otherwise the compiler refuses to work
        s.compiled_file = f'/tmp/{s.program_name}.8xp'
        s.f = open(s.tibasic_source_file, 'w')

        s.dependencies = dependencies
        for file in s.dependencies:
            try:
                # note that python will take care of double includes
                __import__(file)
            except ModuleNotFoundError:
                raise Exception(f'could not find program `{file}`; the dependencies need to be reachable by PATH')

        s.labels = []

    def __enter__(s):
        return s

    def __exit__(s, exc_type, exc_value, exc_traceback):
        s.f.close()
        if exc_type == None: # if no exceptions
            # compile
            term(['ti84cc', '-o', s.compiled_file, s.tibasic_source_file])
            # send to calc
            term(['tilp', '--no-gui', s.compiled_file])

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

    def inputstr(s, store_in, prompt=None):
        to_write = ''

        to_write += 'Input '

        if prompt != None:
            assert '"' not in prompt

            while len(prompt) > s.disp_len_x:
                s.printstr(prompt[:s.disp_len_x])
                prompt = prompt[s.disp_len_x:]

            to_write += f'"{prompt}",'

        assert store_in in s.str_regs
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
        return ContextManager(lambda:s.raw('End'))
    
    def whiletrue(s, label):
        s.label(label)
        return ContextManager(lambda:s.goto(label))

    def continuee(s, label):
        s.goto(label)
    
    def call(s, program_name, asm=False):
        if program_name not in s.dependencies:
            raise Exception(f'missing dependency `{program_name}`; all called program calls need to be specified as dependencies')
        program_name = program_name.upper()
        
        if asm:
            s.raw(f'Asm(', end='') # save 1 char by ommiting `)`
        s.raw(f'prgm{program_name}')

    # other

    def raw(s, code, end='\n'):
        s.f.write(code)
        s.f.write(end)
    
    def asm_prgm(s, code):
        s.raw('AsmPrgm')
        code = code.replace('\n', '')
        code = code.replace('\t', '')
        code = code.replace(' ', '')
        s.raw(code, end='')
