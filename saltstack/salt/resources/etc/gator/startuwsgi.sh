#!/bin/bash


count=0
while [ ! -e "/var/gator/api/wsgi.py" ]
do
        if [ $count == 10 ]
        then
                echo "the file /var/gator/api/wsgi.py does not exist"
                exit 1
        fi

        sleep 2
        let "count += 1"
done

exec /usr/local/bin/uwsgi --ini /etc/gator/grest.ini

