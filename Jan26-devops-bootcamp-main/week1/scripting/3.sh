# loops -> run a block of code multiple times

# for i in 1 2 3 4 5; do
#     echo "iteration number $i"
# done

#$1 -> access.log
# for i in `cat block-ip.txt` ; do

#     grep $i $1 > /dev/null
#     if [ $? -ne 0 ] ; then
#         echo "ip $i not found in log"
#         continue
#     fi
#     echo "blocking ip $i"
#     # sudo ufw deny from $i
# done



# for i in `cat block-ip.txt` ; do

#     occurance=$(grep $i $1 | wc -l)

#     if [ $occurance -gt 10 ] ; then
#         echo "Notify to team -> ip $i is attaching the system - total occurance $occurance"
#         continue
#     fi
# done



### while loop

# while read line ; do
#     echo "line content -> $line"
# done 

flag=0

while [ $flag -eq 0 ]; do
    echo "Loop is running... (flag is $flag)"
    sleep 1
    flag=1

done

echo "Loop stopped"