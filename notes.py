
import lib_tibasic

NUMBER_OF_NOTES = 5
LINES_PER_NOTE = 5

with lib_tibasic.TiBasicLib() as tb:

    vars_title    = [f'[list]NTTT{tb.encode_to_1char(i)}' for i in range(NUMBER_OF_NOTES)]
    vars_content = [[f'[list]NTC{tb.encode_to_1char(i)}{tb.encode_to_1char(k)}' for k in range(LINES_PER_NOTE)]  for i in range(NUMBER_OF_NOTES)]

    lbl_exit = tb.gen_label()

    for i in range(NUMBER_OF_NOTES):
        tb.setupeditor_lstr(vars_title[i])

    lbl_main_menu = tb.gen_label()
    tb.label(lbl_main_menu)

    note_selection_labels = [tb.gen_label() for _ in range(NUMBER_OF_NOTES)]

    tb.menu(
        '"SELECT NOTE"',
        vars_title,
        note_selection_labels,
    )
    tb.goto(lbl_exit)

    for note_idx, label in enumerate(note_selection_labels):
        tb.label(label)
        with tb.scope():

            # lbl_menu = tb.gen_label()
            lbl_edit = tb.gen_label()
            lbl_rename = tb.gen_label()

            tb.menu(
                '"NOTE ACTION"',
                [
                    '"EDIT"',
                    '"RENAME"',
                ],
                [
                    lbl_edit,
                    lbl_rename,
                ]
            )
            tb.goto(lbl_main_menu)

            tb.label(lbl_rename)
            with tb.scope():
                tb.input(vars_title[note_idx], '"ENTER NEW NAME: "', ut14c=True)
            tb.goto(lbl_main_menu)

            tb.label(lbl_edit)
            with tb.scope():

                for content_var in vars_content[note_idx]:
                    tb.setupeditor_lstr(content_var)

                line_labels = [tb.gen_label() for _ in range(LINES_PER_NOTE)]

                lbl_exit_this_notes_content_exitor = tb.gen_label()

                lbl_note_main_menu = tb.gen_label()
                tb.label(lbl_note_main_menu)

                tb.menu(
                    '"EDIT CONTENT"',
                    vars_content[note_idx],
                    line_labels,
                )
                tb.goto(lbl_exit_this_notes_content_exitor)

                for line_idx, line_label in enumerate(line_labels):
                    tb.label(line_label)
                    with tb.scope():
                        tb.input(vars_content[note_idx][line_idx], '"ENTR NEW CNTENT:"', ut14c=True)
                    tb.goto(lbl_note_main_menu)

                tb.label(lbl_exit_this_notes_content_exitor)
                with tb.scope():
                    for content_var_idx, content_var in enumerate(vars_content[note_idx]):
                        tb.print_str(f'"ARCH CONTENT {content_var_idx+1}/{LINES_PER_NOTE}"')
                        tb.archive_var(content_var)
                tb.print_str('"ARCH CNTNTS DONE"')
                tb.goto(lbl_main_menu)

            tb.goto(lbl_main_menu)

    tb.label(lbl_exit)
    with tb.scope():
        for i in range(NUMBER_OF_NOTES):
            tb.print_str(f'"ARCH TITLE {i+1}/{NUMBER_OF_NOTES}"')
            tb.archive_var(vars_title[i])
        tb.print_str('"ARCH TITLES DONE"')
