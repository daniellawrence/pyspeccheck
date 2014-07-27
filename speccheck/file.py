#!/usr/bin/env python

from .util import Spec


class File(Spec):

    STATES = [
        "directory", "file",
        "owned_by",
        "smaller_than", "larger_than"
    ]

    def __init__(self, path):
        self.path = path
        self.state = {}
        self.get_state()
        self.WIN = "File %s is %%s" % self.path

    def get_state(self):
        import os
        import stat
        import pwd
        import grp
        s = os.stat(self.path)
        self.state = {
            'st_mode': s.st_mode,
            'st_ino': s.st_ino,
            'st_dev': s.st_dev,
            'st_nlink': s.st_nlink,
            'st_uid': s.st_uid,
            'st_gid': s.st_gid,
            'st_size': s.st_size,
            'user': pwd.getpwuid(s.st_uid)[0],
            'group': grp.getgrgid(s.st_gid)[0],
            'directory': stat.S_ISDIR(s.st_mode),
            'file': stat.S_ISREG(s.st_mode),
            'full_mode': oct(stat.S_IMODE(s.st_mode)),
            'mode': oct(stat.S_IMODE(s.st_mode))[1:],
        }

    def sb_smaller_than(self, size):
        size_map = {
            'k': 1024,
            'm': 1024*1024,
            'g': 1024*1024*1024
        }
        real_size = self.state['st_size']
        size_units = size[-1].lower()
        size_count = int(size[0:-1])
        expected_size = size_count * size_map[size_units]

        if expected_size > real_size:
            return True, "File %s is smaller than %s" % (self.path, size)
        else:
            return False, "File %s is larger than %s" % (self.path, size)

    def sb_larger_than(self, size):
        x, msg = self.sb_smaller_than(size)
        return x is False, msg

    def sb_directory(self, *args):
        if self._make_sure(self.state['directory']):
            return True
        return "%s is not a directory" % (self.path)

    def sb_file(self, *args):
        if self._make_sure(self.state['file']):
            return True
        return "%s is not a file" % (self.path)

    def sb_owned_by(self, desired_owner):
        user = None
        group = None
        problems = []
        if ':' in desired_owner:
            (user, group) = desired_owner.split(':')
        else:
            user = desired_owner

        if user and self.state['user'] != user:
            problems.append("owned %s not %s" % (self.state['user'], user))

        if group and self.state['group'] != group:
            problems.append("group %s not %s" % (self.state['group'], group))

        if problems:
            return ' and '.join(problems)
        return True
