
import tibasiclib

NUMBER_OF_NOTES = 20

with tibasiclib.TiBasicLib() as tb:

    assert len(str(NUMBER_OF_NOTES)) <= 2 # now we have 3 chars left for the list name
    pref_note_title = '[list]NTT'
    
    note_selection_labels = [tb.get_label() for _ in range(NUMBER_OF_NOTES)]

    lbl_exit = tb.get_label()

    for i in range(NUMBER_OF_NOTES):
        var_title = f'{pref_note_title}{i}' # TODO implement a function for a more eficient encoder (we could be saving 1 char here)
        
        tb.setupeditor(var_title)
        
        with tb.iff(f'dim({var_title})=0'):
            tb.raw(f'1->{var_title}(1)')

    tb.menu(
        '"SELECT NOTE"',
        ['"* EXIT"'] + [f'{pref_note_title}{i}' for i in range(NUMBER_OF_NOTES)],
        [lbl_exit]   + note_selection_labels,
    )

    # create note titles if hey don't exist
    # this will unarchive them if they do
    # tb.setupeditor('[list]')


    # tb.input(tb.var_arg_str_0, 'idkman:')

    # tb.call('st2lst')
    # # input : tb.var_arg_str_0
    # # output: tb.var_ret_list_0
    # # trash : tb.var_trash_num_0

    # tb.raw(f'{tb.var_ret_list_0}->{tb.var_arg_list_0}')

    # tb.call('lst2st')
    # # input : tb.var_arg_list_0
    # # output: tb.var_ret_str_0
    # # trash : tb.var_trash_num_0

    # tb.printvar(tb.var_ret_str_0)

    # tb.press_any_key()

    tb.label(lbl_exit)
    with tb.scope():
        for i in range(NUMBER_OF_NOTES):
            var_title = f'{pref_note_title}{i}'

            tb.printstr(f'archiving {i+1}/{NUMBER_OF_NOTES}')
            tb.archive_var(var_title)
        tb.printstr('archiving done')
