
import tibasiclib

NUMBER_OF_NOTES = 8

with tibasiclib.TiBasicLib() as tb:

    assert len(str(NUMBER_OF_NOTES)) <= 2 # now we have 3 chars left for the list name
    
    vars_title = [f'[list]NTT{i}' for i in range(NUMBER_OF_NOTES)] # TODO implement a function for a more eficient encoder (we could be saving 1 char here)
    note_selection_labels = [tb.get_label() for _ in range(NUMBER_OF_NOTES)]
    # TODO also make list with var names instead of generating it every time

    lbl_exit = tb.get_label()

    for i in range(NUMBER_OF_NOTES):
        tb.setupeditor_lstr(vars_title[i])

    tb.menu(
        '"SELECT NOTE"',
        ['"* EXIT"'] + vars_title,
        [lbl_exit]   + note_selection_labels,
    )


    for i, label in enumerate(note_selection_labels):
        tb.label(label)
        with tb.scope():
            ... # tb.setupeditor_lstr()


    tb.label(lbl_exit)
    with tb.scope():
        for i in range(NUMBER_OF_NOTES):
            tb.printstr(f'archiving {i+1}/{NUMBER_OF_NOTES}')
            tb.archive_var(vars_title[i])
        tb.printstr('archiving done')



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
