xxx=`cat xxx`

alias gf='find . -type f | xargs grep -nE --color'
for i in $xxx; do
    echo $i
    echo 'common\/'$i
    replace='plugin\/'$i
    gf -l $i | grep -vE "(xxx|Binary|json|pyc$|html$)" | xargs sed -i '' "s/$i/$replace/g"
    # sedr $i 'plugin\/'$i
done
