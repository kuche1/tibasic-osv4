
import tibasiclib

NUMBER_OF_NOTES = 8

with tibasiclib.TiBasicLib() as tb:

    assert len(str(NUMBER_OF_NOTES)) <= 2 # now we have 3 chars left for the list name
    
    vars_title = [f'[list]NTT{i}' for i in range(NUMBER_OF_NOTES)] # TODO implement a function for a more eficient encoder (we could be saving 1 char here)
    vars_content = [f'[list]NTC{i}' for i in range(NUMBER_OF_NOTES)]

    lbl_exit = tb.get_label()

    for i in range(NUMBER_OF_NOTES):
        tb.setupeditor_lstr(vars_title[i])

    lbl_main_menu = tb.get_label()
    tb.label(lbl_main_menu)

    note_selection_labels = [tb.get_label() for _ in range(NUMBER_OF_NOTES)]

    tb.menu(
        '"SELECT NOTE"',
        ['"* EXIT"'] + vars_title,
        [lbl_exit]   + note_selection_labels,
    )

    for note_idx, label in enumerate(note_selection_labels):
        tb.label(label)
        with tb.scope():

            # lbl_menu = tb.get_label()
            lbl_edit = tb.get_label()
            lbl_rename = tb.get_label()

            tb.menu(
                '"NOTE ACTION"',
                [
                    '"EXIT"',
                    '"EDIT"',
                    '"RENAME"',
                ],
                [
                    lbl_main_menu,
                    lbl_edit,
                    lbl_rename,
                ]
            )

            tb.label(lbl_rename)
            with tb.scope():
                tb.input(tb.var_arg_str_0, 'ENTER NEW NAME: ')

                tb.call('st2lst')
                # input : tb.var_arg_str_0
                # output: tb.var_ret_list_0
                # trash : tb.var_trash_num_0

                tb.raw(f'{tb.var_ret_list_0}->{vars_title[note_idx]}')
            tb.goto(lbl_main_menu)

            tb.label(lbl_edit)

            # tb.setupeditor_lstr(vars_content[i])
            # ...


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
