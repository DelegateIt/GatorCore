#!/bin/bash


count=0
while [ ! -e "/var/gator/web/startserver.py" ]
do
        if [ $count == 10 ]
        then
                echo "the file /var/gator/web/startserver.py does not exist"
                exit 1
        fi

        sleep 2
        let "count += 1"
done

cd /var/gator/web/
exec /usr/bin/python3 startserver.py --port 8080

