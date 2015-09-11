vim:
    pkg.installed

git:
    pkg.installed

ack-grep:
    pkg.installed

/etc/gator/startdlgtweb.sh:
    file.managed:
        - source: salt://resources/etc/gator/startdlgtweb.sh
        - user: root
        - group: root
        - mode: 744

delgator-web-service:
    file.managed:
        - name: /etc/init/dlgtweb.conf
        - source: salt://resources/etc/init/dlgtweb.conf
        - user: root
        - group: root
        - mode: 644
        - require:
            - file: /etc/gator/startdlgtweb.sh

    service.running:
        - name: dlgtweb
        - enable: True
        - require:
            - file: /etc/gator/startdlgtweb.sh

