pyspeccheck
===========

Lets you write easy specs for what your local machine should be, then checks that is the case.


You write
---------

	$ cat ./example_ssh_check.py
    #!/usr/bin/env python
    from speccheck.port import Port
    from speccheck.file import File

    # Monitoring to make sure the port 22 is ready
    ssh_port = Port(22)
    ssh_port.should_be('listening')
    ssh_port.should_be('tcp')
    ssh_port.should_be('bound_to', '0.0.0.0')
    ssh_port.should_not_be('bound_to', '127.0.0.1')

	for IMPORTANT_DIRS in ["/etc/ssh/"]:
		f = File(IMPORTANT_DIRS)
		f.should_be("directory")
		f.should_be("owned_by", "root:root")
		f.should_be("owned_by", "root")

It generates
--------------

	Port 22 is listening correctly
	Port 22 is tcp correctly
	Port 22 is bound to 0.0.0.0 correctly
	Port 22 is bound to 0.0.0.0 not 127.0.0.1
	File /etc/ssh/ is directory correctly
	File /etc/ssh/ is owned by root:root correctly
	File /etc/ssh/ is owned by root correctly
