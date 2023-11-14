
import tibasiclib

NUMBER_OF_NOTES = 5
LINES_PER_NOTE = 5

with tibasiclib.TiBasicLib() as tb:

    vars_title    = [f'[list]NTTT{tb.encode_to_1char(i)}' for i in range(NUMBER_OF_NOTES)]
    vars_content = [[f'[list]NTC{tb.encode_to_1char(i)}{tb.encode_to_1char(k)}' for k in range(LINES_PER_NOTE)]  for i in range(NUMBER_OF_NOTES)]

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
                # tb.input(tb.var_arg_str_0, 'ENTER NEW NAME: ')

                # tb.call('st2lst')
                # # input : tb.var_arg_str_0
                # # output: tb.var_ret_list_0
                # # trash : tb.var_trash_num_0

                # tb.raw(f'{tb.var_ret_list_0}->{vars_title[note_idx]}')
                tb.input_lstr(vars_title[note_idx], '"ENTER NEW NAME: "')
            tb.goto(lbl_main_menu)

            tb.label(lbl_edit)
            with tb.scope():

                for content_var in vars_content[note_idx]:
                    tb.setupeditor_lstr(content_var)

                line_labels = [tb.get_label() for _ in range(LINES_PER_NOTE)]

                lbl_exit_this_notes_content_exitor = tb.get_label()

                lbl_note_main_menu = tb.get_label()
                tb.label(lbl_note_main_menu)

                tb.menu(
                    '"EDIT"',
                    ['"* EXIT"']                         + vars_content[note_idx],
                    [lbl_exit_this_notes_content_exitor] + line_labels,
                )

                for line_idx, line_label in enumerate(line_labels):
                    tb.label(line_label)
                    with tb.scope():
                        # tb.input(tb.var_arg_str_0, 'ENTR NEW CNTENT:')

                        # tb.call('st2lst')
                        # # input : tb.var_arg_str_0
                        # # output: tb.var_ret_list_0
                        # # trash : tb.var_trash_num_0

                        # tb.raw(f'{tb.var_ret_list_0}->{vars_content[note_idx][line_idx]}')
                        tb.input_lstr(vars_content[note_idx][line_idx], '"ENTR NEW CNTENT:"')
                    tb.goto(lbl_note_main_menu)

                tb.label(lbl_exit_this_notes_content_exitor)
                with tb.scope():
                    for content_var_idx, content_var in enumerate(vars_content[note_idx]):
                        tb.printstr(f'ARCH CONTENT {content_var_idx+1}/{LINES_PER_NOTE}')
                        tb.archive_var(content_var)
                tb.printstr('ARCH CNTNTS DONE')
                tb.goto(lbl_main_menu)

                # tb.printstr('NOT IMPLEMENTED YET')
                # tb.press_any_key()
                # # tb.setupeditor_lstr(vars_content[i])
                # # ...
            tb.goto(lbl_main_menu)

    tb.label(lbl_exit)
    with tb.scope():
        for i in range(NUMBER_OF_NOTES):
            tb.printstr(f'ARCH TITLE {i+1}/{NUMBER_OF_NOTES}')
            tb.archive_var(vars_title[i])
        tb.printstr('ARCH TITLES DONE')


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
