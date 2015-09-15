vim:
    pkg.installed

git:
    pkg.installed

ack-grep:
    pkg.installed

nose:
    cmd.run:
        - name: |
            pip install --upgrade nose
        - require:
            - pkg: python-pip
