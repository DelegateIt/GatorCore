#!/bin/bash


count=0
while [ ! -e "/var/gator/api/gator/rest_handler.py" ]
do
        echo "Checking $checking"
        if [ $count == 10 ]
        then
                echo "the file /var/gator/api/gator/rest_handler.py does not exist"
                exit 1
        fi

        sleep 2
        let "count += 1"
done

echo "Hurray"
exec /var/gator/api/wsgi.py

