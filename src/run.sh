
pkill -f python*

if [ "$1"  == "" ]
then
    echo  "Enter valid backend type {RNN, DS, SPHINX}"
    echo  "Exiting ...."
    exit -1
fi

cd /home/aditya/Documents/project/SubGen/src  && /home/aditya/.venvs/tf/bin/python server.py -b $1& 

sleep 2
spid=`cat /home/aditya/Documents/project/SubGen/tmp/recognizer.pid`

/home/aditya/.venvs/tf/bin/psrecord $spid --log /home/aditya/Documents/project/SubGen/tmp/recognizer.txt --interval 0.2 --plot /home/aditya/Documents/project/SubGen/tmp/recog.png --include-children &
P1=$!

cd /home/aditya/Documents/project/SubGen/src  && /home/aditya/.venvs/vlc/bin/python run.py -d &
sleep 2
ppid=`cat /home/aditya/Documents/project/SubGen/tmp/player.pid`
/home/aditya/.venvs/tf/bin/psrecord $ppid --log /home/aditya/Documents/project/SubGen/tmp/player.txt --interval 0.2 --plot /home/aditya/Documents/project/SubGen/tmp/player.png --include-children &
P2=$!
wait $P1 $P2
echo "Press Ctrl + C to exit"
read -r -d '' _ </dev/tty
pkill -f python*
kill $ppid
kill $spid