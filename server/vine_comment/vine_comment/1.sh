xxx=`cat xxx`

for i in $xxx; do
    echo $i
    echo 'common\/'$i
    sedr $i 'common\/'$i
done
