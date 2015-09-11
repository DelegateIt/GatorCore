
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

python3-dev:
    pkg.installed

python3-pip:
    pkg.installed:
        - require:
            - pkg: python3-dev

Flask:
    cmd.run:
        - name: |
            pip3 install --upgrade Flask
        - require:
            - pkg: python3-pip

boto:
    cmd.run:
        - name: |
            pip3 install --upgrade boto
        - require:
            - pkg: python3-pip
jsonpickle:
    cmd.run:
        - name: |
            pip3 install --upgrade jsonpickle
        - require:
            - pkg: python3-pip

pip-stripe:
    cmd.run:
        - name: |
            pip3 install --upgrade stripe
        - require:
            - pkg: python3-pip

uwsgi:
    cmd.run:
        - name: |
            pip3 install --upgrade uwsgi
        - require:
            - pkg: python3-pip


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
        - reload: True

nginx-service:
  service.running:
    - name: nginx
    - enable: True
    - reload: True
    - require:
        - pkg: nginx

