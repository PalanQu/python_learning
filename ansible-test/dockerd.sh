#!/bin/sh

function d_start()
{
        echo  "dockerd: starting service" 
        dockerd --pidfile=/tmp/dockerd.pid
         sleep  5
        echo  "PID is $(cat /tmp/dockerd.pid) " 
}

function d_stop()
{
        echo  "dockerd: stopping Service (PID = $(cat /tmp/dockerd.pid))" 
        kill $(cat /tmp/dockerd.pid)
        rm  /tmp/dockerd.pid
 }

function d_status ()
{
        ps -ef | grep dockerd | grep -v grep
        echo  "PID indicate indication file $(cat /tmp/dockerd.pid /dev/null)" 
}

# Some Things That run always 
touch /var/lock/dockerd

# Management instructions of the service 
case  "$1"  in
        start)
                d_start
                ;;
        stop)
                d_stop
                ;;
        restart)
                d_stop
                sleep  1
                d_start
                ;;
        status)
                d_status
                ;;
        *)
        echo  "Usage: $0 {start | stop | reload | status}" 
        exit 1
        ;;
esac

exit 0
