vim:
    pkg.installed: []

# Copy over custom vimrc
/home/vagrant/.vimrc:
    file.managed:
        - source: salt://resources/vimrc
        - mode: 644
        - user: vagrant
        - require:
            - pkg: vim



# Setup directory structure
/home/vagrant/.vim/:
    file.directory:
        - user: vagrant
        - require:
            - pkg: vim

/home/vagrant/.vim/autoload/:
    file.directory:
        - user: vagrant
        - require:
            - pkg: vim

/home/vagrant/.vim/bundle/:
    file.directory:
        - user: vagrant
        - require:
            - pkg: vim

/home/vagrant/.vim/colors/:
    file.directory:
        - user: vagrant
        - require:
            - pkg: vim

# Install pathogen and packages
/home/vagrant/.vim/autoload/pathogen.vim:
    file.managed:
        - source: salt://resources/pathogen.vim
        - user: vagrant
        - require:
            - file: /home/vagrant/.vim/
            - file: /home/vagrant/.vim/autoload/

/home/vagrant/.vim/colors/molokai.vim:
    file.managed:
        - source: salt://resources/molokai.vim
        - user: vagrant
        - require:
            - file: /home/vagrant/.vim/
            - file: /home/vagrant/.vim/autoload/

https://github.com/scrooloose/syntastic:
    git.latest:
        - target: /home/vagrant/.vim/bundle/syntastic/
        - rev: master
        - require:
            - file: /home/vagrant/.vim/
            - file: /home/vagrant/.vim/bundle/


https://github.com/bling/vim-airline:
    git.latest:
        - target: /home/vagrant/.vim/bundle/vim-airline/
        - rev: master
        - require:
            - file: /home/vagrant/.vim/
            - file: /home/vagrant/.vim/bundle/

# YouCompleteMe Settings
cmake:
    pkg:
        - installed

https://github.com/Valloric/YouCompleteMe:
    git.latest:
        - target: /home/vagrant/.vim/bundle/YouCompleteMe/
        - rev: master
        - require:
            - file: /home/vagrant/.vim/
            - file: /home/vagrant/.vim/bundle/

nano:
    pkg:
        - removed
