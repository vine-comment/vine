xxx=`cat xxx`

for i in $xxx; do
    echo $i
    echo 'site\/'$i
    sedr $i 'site\/'$i
done
