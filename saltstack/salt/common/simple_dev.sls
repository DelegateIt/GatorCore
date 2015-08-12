git:
    pkg.installed

ack-grep:
    pkg.installed

python-dev:
    pkg.installed

python-pip:
    pkg.installed:
        - require:
            - pkg: python-dev

nose:
    pkg.installed:
        - require:
            - pkg: python-pip

enum:
    pkg.installed:
        - require:
            - pkg: python-pip

Flask:
    pip.installed:
        - require:
            - pkg: python-pip

boto:
    pip.installed:
        - require:
            -pkg: python-pip
