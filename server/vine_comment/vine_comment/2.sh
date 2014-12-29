
alias gf='find . -type f | xargs grep -nE --color'

i="\'comments\/"
replace="\'plugin\/comments\/"
gf -l $i | grep -vE "(xxx|Binary|json|pyc$)" | xargs sed -i '' "s/$i/$replace/g"

i="\"comments\/"
replace="\"plugin\/comments\/"
gf -l $i | grep -vE "(xxx|Binary|json|pyc$)" | xargs sed -i '' "s/$i/$replace/g"
