git:
    pkg.installed

python-dev:
    pkg.installed

python-pip:
    pkg.installed:
        - require:
            - pkg: python-dev

mysql_setup:
    debconf.set:
        - name: mysql-server
        - data:
            'mysql-server/root_password': {'type': 'string', 'value': 'default'}
            'mysql-server/root_password_again': {'type': 'string', 'value': 'default'}

libmysqlclient-dev:
    pkg:
        - installed

mysql-server:
    pkg:
        - installed
        - require:
            - debconf: mysql_setup
            - pkg: python-dev
            - pkg: libmysqlclient-dev

MySQL-Python:
    pip.installed:
        - require:
            - pkg: python-pip
            - pkg: mysql-server

sqlalchemy:
    pip.installed:
        - require:
            - pkg:  python-pip
