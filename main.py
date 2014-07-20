#!/usr/bin/env python

from speccheck.port import Port
from speccheck.file import File

# Monitoring to make sure the port 22 is ready
ssh_port = Port(22)
ssh_port.should_be('listening')
ssh_port.should_be('tcp')
ssh_port.should_be('bound_to', '0.0.0.0')
ssh_port.should_not_be('bound_to', '127.0.0.1')


# This is not a websever make sure 80 is closed.
port_80 = Port(80)
port_80.should_be('closed')

# keep the following ports closed
for PORT_NUMBER in [21, 23, 53, 25]:
    Port(PORT_NUMBER).should_be('closed')


slash_tmp = File("/tmp")
slash_tmp.should_be("directory")
slash_tmp.should_not_be("file")
