if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

export domains_home={{ domains_home }}
export applications_home={{ applications_home }}
