#!/bin/sh
adin=`ps aux|grep 'manage.py runserver 0.0.0.0:8000'|grep -v grep`

export AUTOTEST_HOME=/home/Auto_Test
export AUTOTEST_LOG_LOC=/home/Auto_Test/log

if [ ! -d $AUTOTEST_LOG_LOC ] 
then
   mkdir -p $AUTOTEST_LOG_LOC
fi

case "$1" in
start)
    if [ -z "$adin" ]
    then
    echo "start autotest server...."
    cd $AUTOTEST_HOME
    python manage.py runserver 0.0.0.0:8000 >>$AUTOTEST_LOG_LOC/server.log 2>&1 &
    else
      echo "auto_test already running, no need to start!"
    fi
    ;;
stop)
       pkill -f python
        echo "autotest stopped"
       ;;

restart)
       pkill -f python
       cd $AUTOTEST_HOME
       python manage.py runserver 0.0.0.0:8000>>$AUTOTEST_LOG_LOC/server.log 2>&1 &
       echo "autotest restarted"
                     ;;
version)
       $PREHANDLE_HOME/run-data-prehandle.sh version
                     ;;

debug)
      $PREHANDLE_HOME/run-data-prehandle.sh debug >>$PREHANDLE_LOG_LOC/log.prehandle 2>&1 & 
      ;;
*)
      echo "Usage: collector start|stop|restart|debug|version"
      echo "Your input options:" $*
      exit 1

esac
exit 0

