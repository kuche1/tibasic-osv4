
import tibasiclib

# converts list to string

# input : L1
# output: Str0
# trash : A L1

with tibasiclib.TiBasicLib(
    ) as tb:

    tb.raw('''
" "
For(A,1,dim(L1))
Ans+sub("0123456789abcdefghijklmnopqrstuvwxyz :?[theta].,()",L1(A),1)
End

If length(Ans)=1
Then
""->Str0
Else
sub(Ans,2,length(Ans)-1)->Str0
End
''')
