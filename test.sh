#!/bin/bash

start_time=$(date +%s)

sleep 4

end_time=$(date +%s)

timeout=`expr $end_time - $start_time`

if [ $timeout -lt 2 ]; then
	echo " 2"
fi

if [ $timeout -lt 5 ]; then
        echo " 5"
fi

if [ $timeout -gt 4 ]; then
        echo " 4"
fi

echo $timeout
