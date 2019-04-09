
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

P1=$!
/home/aditya/.venvs/tf/bin/psrecord $spid --log "/home/aditya/Documents/project/SubGen/tmp/recognizer_$1.txt" --interval 0.2 --plot "/home/aditya/Documents/project/SubGen/tmp/recog_$1.png" --include-children &
cd /home/aditya/Documents/project/SubGen/src  && /home/aditya/.venvs/vlc/bin/python run.py -d &
sleep 2

ppid=`cat /home/aditya/Documents/project/SubGen/tmp/player.pid`
P2=$!
wait $P1 $P2
/home/aditya/.venvs/tf/bin/psrecord $ppid --log "/home/aditya/Documents/project/SubGen/tmp/player_$1.txt" --interval 0.2 --plot "/home/aditya/Documents/project/SubGen/tmp/player_$1.png" --include-children &


echo "Press Ctrl + C to exit"
read -r -d '' _ </dev/tty
pkill -f python*
kill $ppid
kill $spid
