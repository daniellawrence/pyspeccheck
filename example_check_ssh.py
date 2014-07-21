#!/usr/bin/env python

from speccheck.util import status
from speccheck.port import Port
from speccheck.file import File

# Monitoring to make sure the port 22 is ready
ssh_port = Port(21)
ssh_port.should_be('listening')
ssh_port.should_be('tcp')
ssh_port.should_be('bound_to', '0.0.0.0')
ssh_port.should_not_be('bound_to', '127.0.0.1')

for IMPORTANT_DIRS in ["/etc/ssh/"]:
    f = File(IMPORTANT_DIRS)
    f.should_be("directory")
    f.should_be("owned_by", "root:root")
    f.should_be("owned_by", "root")

print status.nagios() + "\n"

print "\n".join(status.fail)
