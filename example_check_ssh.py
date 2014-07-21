#!/usr/bin/env python

from speccheck.util import status
from speccheck.port import Port
from speccheck.file import File
import sys

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

print("\n")
print("--------")

if status.status() == "Fail":
    print("summary: Failed %d/%d specs" % (
        len(status.get_problems()),
        len(status.get_problems()) +
        len(status.get_ok()),
    ))
    print("\n".join(status.get_problems()))
    sys.exit(1)
else:
    print("All %d passed" % len(status.get_ok()))
    sys.exit(0)
