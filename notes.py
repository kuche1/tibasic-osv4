
import tibasiclib

# app used for writing down notes

# trash: A-E
# trash: STR0-STR4 STR7-STR9 L1

# TODO NUMBER_OF_NOTES = 6

with tibasiclib.TiBasicLib(
    ) as tb:

    # create note titles if hey don't exist
    # this will unarchive them if they do
    tb.raw('''
SetUpEditor [list]NTTI1
SetUpEditor [list]NTTI2
SetUpEditor [list]NTTI3
SetUpEditor [list]NTTI4
SetUpEditor [list]NTTI5
SetUpEditor [list]NTTI6
''')

    tb.label('MM')
    with tb.scope():
        tb.printstr('dcdng ttls...')

        # reload titles since they might have been trashed

        for i in range(1, 6+1):
            tb.raw(f'[list]NTTI{i}->L1')

            tb.call('lst2st')
            # input : L1
            # output: Str0
            # trash : A L1

            tb.raw(f'Str0->Str{i+1}')
        
        tb.printstr('done')

        tb.menu(
            '"notes"',
            [
                'Str2',
                'Str3',
                'Str4',
                'Str5',
                'Str6',
                'Str7',
                '"* EXIT"',
            ],
            [
                'N2',
                'N3',
                'N4',
                'N5',
                'N6',
                'N7',
                'EX',
            ]
        )

    # save selected note

    for i in range(2, 7+1):
        tb.label(f'N{i}')
        tb.raw(f'{i}->C')
        tb.raw(f'Str{i}->Str0')
        tb.goto('NN')
    
    tb.label('NN')

    # number is saved in `c`
    # name is saved in `STR0`

    tb.raw('Menu(Str0,"<edit>",ED,"",NN,"<rename>",RN,"",NN,"",NN,"<del cntnt>",DL,"<back>",MM)')

    tb.label('ed')
    with tb.scope():
        tb.printstr('unarch cntnt...')

        # set `Ans` based on current note

        # create lists if they don't exist
        # and unarchive if they do

        for i in range(2, 7+1):
            with tb.iff(f'C={i}'):
                tb.raw(f'SetUpEditor [list]ntdt{i}')
                tb.raw(f'[list]ntdt{i}->L1')

        tb.printstr('dcdng cntnt...')

        # `L1` set by ifs

        tb.call('lst2st')
        # input : L1
        # output: Str0
        # trash : A L1

        tb.printstr('done')

    program = '''

    STR0
    prgmTXTEDTR
    //input : Ans - string
    //output: Ans - string ||| a - 0[don't save returned data] 1[save returned data]
    //trash : STR0-STR5 STR7 STR8

    If a=1 // if given signal to save returned data
    Then

        Disp "encdng cntnt..."

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        Disp "arch cntnt..."

        If c=2
        Then
            L1->[list]ntdt2
            Archive [list]ntdt2
        End

        If c=3
        Then
            L1->[list]ntdt3
            Archive [list]ntdt3
        End

        If c=4
        Then
            L1->[list]ntdt4
            Archive [list]ntdt4
        End

        If c=5
        Then
            L1->[list]ntdt5
            Archive [list]ntdt5
        End

        If c=6
        Then
            L1->[list]ntdt6
            Archive [list]ntdt6
        End

        If c=7
        Then
            L1->[list]ntdt7
            Archive [list]ntdt7
        End

        Disp "done"
    
    End
    
    Goto mm // go back to main menu

Lbl rn // rename note

    If length(STR0)=0
        " "->STR0

    Disp "--- old name ---"
    Disp ">>"+STR0
    Disp "--- new name ---"

    ">>"
    prgmGETSTFST
    //input : Ans - string - prompt
    //return: STR0 - user input

    If c=2
    Then
        STR0->STR2
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI1
    End

    If c=3
    Then
        STR0->STR3
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI2
    End

    If c=4
    Then
        STR0->STR4
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI3
    End

    If c=5
    Then
        STR0->STR5
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI4
    End

    If c=6
    Then
        STR0->STR6
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI5
    End

    If c=7
    Then
        STR0->STR7
        // this also sets `Ans`

        prgmST2LST
        //input : Ans - string
        //output: L1
        //trash : STR0

        L1->[list]NTTI6
    End

    Goto mm // go back to main menu, now that the appropriate Str variable has been updated

Lbl dl // delete note

    Menu("confirm deletion","no",mm,"yes",dy)

    Lbl dy

    Disp "deleting..."

    If c=2
    Then
        UnArchive [list]ntdt2
        0->dim([list]ntdt2)
        Archive [list]ntdt2
    End

    If c=3
    Then
        UnArchive [list]ntdt3
        0->dim([list]ntdt3)
        Archive [list]ntdt3
    End

    If c=4
    Then
        UnArchive [list]ntdt4
        0->dim([list]ntdt4)
        Archive [list]ntdt4
    End

    If c=5
    Then
        UnArchive [list]ntdt5
        0->dim([list]ntdt5)
        Archive [list]ntdt5
    End

    If c=6
    Then
        UnArchive [list]ntdt6
        0->dim([list]ntdt6)
        Archive [list]ntdt6
    End

    If c=7
    Then
        UnArchive [list]ntdt7
        0->dim([list]ntdt7)
        Archive [list]ntdt7
    End

    Disp "done"

    Goto mm

Lbl EX

ClrList L1

""->STR0
""->STR1
""->STR2
""->STR3
""->STR4
""->STR5
""->STR6
""->STR7

Disp "arch ttls..."

// archive note titles
// this takes some time
Archive [list]NTTI1
Archive [list]NTTI2
Archive [list]NTTI3
Archive [list]NTTI4
Archive [list]NTTI5
Archive [list]NTTI`6

Disp "done"

'''
