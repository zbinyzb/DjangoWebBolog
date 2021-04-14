# .bashrc

# User specific aliases and functions

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
export LD_LIBRARY_PATH="/usr/local/lib"
export VIRTUALENVWRAPPER_PYTHON=/usr/local/python3/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
source /usr/bin/virtualenvwrapper.sh