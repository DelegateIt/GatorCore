
###################
# User management #
###################


gator-group:
    group.present:
        - name: gator
        - gid: 4000

gator-user:
    user.present:
        - name: gator
        - createhome: False
        - uid: 4000
        - gid: 4000
        - groups:
            - www-data


########################
# Package Dependencies #
########################

nginx:
    pkg.installed

python-dev:
    pkg.installed

python-pip:
    pkg.installed:
        - require:
            - pkg: python-dev

Flask:
    cmd.run:
        - name: |
            pip install --upgrade Flask
        - require:
            - pkg: python-pip

boto:
    cmd.run:
        - name: |
            pip install --upgrade boto
        - require:
            - pkg: python-pip
jsonpickle:
    cmd.run:
        - name: |
            pip install --upgrade jsonpickle
        - require:
            - pkg: python-pip

flask-socketio:
    cmd.run:
        - name: |
            pip install --upgrade flask-socketio
        - require:
            - pkg: python-pip

###################
# File management #
###################


/etc/nginx/nginx.conf:
    file.managed:
        - source: salt://resources/etc/nginx/nginx.conf
        - user: root
        - group: root
        - mode: 644

/etc/gator/grest.ini:
    file.managed:
        - source: salt://resources/etc/gator/grest.ini
        - user: root
        - group: root
        - mode: 644

/etc/gator/startuwsgi.sh:
    file.managed:
        - source: salt://resources/etc/gator/startuwsgi.sh
        - user: root
        - group: root
        - mode: 744

/etc/init/grest.conf:
    file.managed:
        - source: salt://resources/etc/init/grest.conf
        - user: root
        - group: root
        - mode: 644

/etc/rc.local:
    file.managed:
        - source: salt://resources/etc/rc.local
        - user: root
        - group: root
        - mode: 751

/etc/nginx/sites-available/grest:
    file.managed:
        - source: salt://resources/etc/nginx/sites-available/grest
        - user: root
        - group: root
        - mode: 644

/etc/nginx/sites-enabled/grest:
    file.symlink:
        - target: /etc/nginx/sites-available/grest

/etc/nginx/sites-enabled/default:
    file.absent: []

/var/gator/socks:
    file.directory:
        - user: gator
        - group: www-data
        - dir_mode: 775
        - file_mode: 664


######################
# Service management #
######################


grest-service:
    service.running:
        - enable: True
        - name: grest

nginx-service:
  service.running:
    - name: nginx
    - enable: True
    - require:
        - pkg: nginx

