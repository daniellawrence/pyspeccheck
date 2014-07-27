pyspeccheck
===========

Lets you write easy specs for what your local machine should be, then checks that is the case.


You write
---------

	$ cat ./example_ssh_check.py
    #!/usr/bin/env python
	from speccheck.util import status
	from speccheck.port import Port
	from speccheck.file import File
	from speccheck.package import Package

    # Monitoring to make sure the port 22 is ready
    ssh_port = Port(22)
    ssh_port.should_be('listening')
    ssh_port.should_not_be('udp')
    ssh_port.should_be('bound_to', '0.0.0.0')
    ssh_port.should_not_be('bound_to', '127.0.0.1')

    for IMPORTANT_DIRS in ["/etc/ssh/"]:
        f = File(IMPORTANT_DIRS)
        f.should_be("directory")
        f.should_be("owned_by", "root:root")
        f.should_be("owned_by", "root")

    for IMPORTANT_FILES in ["/etc/ssh/ssh_config", "/etc/ssh/sshd_config"]:
        f = File(IMPORTANT_FILES)
        f.should_be("file")
        f.should_be("owned_by", "root:root")
        f.should_be("owned_by", "root")
        f.should_be("smaller_than", "5K")
        f.should_be("larger_than", "1k")

    sshd = Package("openssh-server")
    sshd.should_be("installed")
    sshd.should_be("latest")

    telnetd = Package("telnetd")
    telnetd.should_not_be("installed")

    print status.nagios()
    status.report()
    if status.fail:
        print status.fail

It generates
--------------

	$ ./example_check_ssh.py
	OK: 20/20 checks passed
	Port 22 is listening
	Port 22 is not udp
	Port 22 is bound to 0.0.0.0
	The port currently bound to 0.0.0.0 not 127.0.0.1
	File /etc/ssh/ is directory
	File /etc/ssh/ is owned by root:root
	File /etc/ssh/ is owned by root
	File /etc/ssh/ssh_config is file
	File /etc/ssh/ssh_config is owned by root:root
	File /etc/ssh/ssh_config is owned by root
	File /etc/ssh/ssh_config is smaller than 5K
	File /etc/ssh/ssh_config is larger than 1k
	File /etc/ssh/sshd_config is file
	File /etc/ssh/sshd_config is owned by root:root
	File /etc/ssh/sshd_config is owned by root
	File /etc/ssh/sshd_config is smaller than 5K
	File /etc/ssh/sshd_config is larger than 1k
	Package openssh-server is installed
	Package openssh-server is latest
	Package telnetd is not installed
