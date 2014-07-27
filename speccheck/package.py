#!/usr/bin/env python

from .util import Spec


class Package(Spec):

    STATES = [
        "installed", "removed", "latest"
    ]

    def __init__(self, name):
        self.name = name
        self.state = {}
        self.get_state()
        self.WIN = "Package %s is %%s" % self.name

    def get_state(self):
        import os
        state = {'installed': False,
                 'removed': True,
                 'version': None,
                 'latest': False
        }
        lines = os.popen("apt-cache policy %s" % self.name).readlines()
        for line in lines:
            line = line.strip()
            if line.startswith('Installed:'):
                _state = line.split()[-1]
                if _state == '(none)':
                    state['installed'] = False
                    state['removed'] = True
                else:
                    state['installed'] = True
                    state['removed'] = False
                    state['version'] = _state

            if line.startswith('Candidate:'):
                latest_version = line.split()[-1]
                if state['version'] == latest_version:
                    state['latest'] = True
                else:
                    state['latest'] = False
        self.state = state

    def sb_installed(self):
        if self.state['installed']:
            return True
        return "%s is not installed" % self.name

    def sb_latest(self):
        if self.state['latest']:
            return True
        return "%s is not the latest" % self.name
