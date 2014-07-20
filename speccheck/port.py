#!/usr/bin/env python

from .util import SpecError, colors, Spec


class Port(Spec):

    STATES = [
        "listening", "closed", "open",
        "bound_to",
        "tcp", "tcp6"
    ]

    def __init__(self, portnumber):
        self.portnumber = portnumber
        self.get_state()
        self.state = {
            'state': 'closed',
            'bound': False,
            'uid': None,
            'inode': None,
            'proto': None,
        }
        self.get_state()
        #
        self.WIN = "Port %s is %%s correctly" % self.portnumber

    def get_state(self):
        import os
        for line in os.popen("netstat -tnle").readlines():
            line = line.strip().split()
            if len(line) != 8:
                continue
            (proto, _, _, local, foreign, state, uid, inode) = line
            if proto == 'tcp':
                (bound, port) = local.split(':')
            port = int(port)
            if port == self.portnumber:
                self.state = {
                    'state': 'listening',
                    'bound': bound,
                    'uid': uid,
                    'inode': inode,
                    'proto': proto,
                }

    def _make_sure(self, x, y):
        if x == y:
            return True
        else:
            return False

    def sb_listening(self, *args):
        if self._make_sure(self.state['state'], "listening"):
            return True
        return "Port %s is current %s not listening" % (self.portnumber,
                                                        self.state['state']
        )

    def sb_closed(self, *args):
        if self._make_sure(self.state['state'], "closed"):
            return True
        return "Port %s is current %s not closed" % (self.portnumber,
                                                     self.state['state']
        )

    def sb_tcp(self, *args):
        if self._make_sure(self.state['proto'], "tcp"):
            return True
        return "Port %s is using protocol %s not TCP" % (self.portnumber,
                                                         self.state['proto']
        )

    def sb_bound_to(self, bound_ip):
        if self._make_sure(self.state['bound'], bound_ip):
            return True
        return "The port is bound to %s not %s" % (self.state['bound'], bound_ip)
