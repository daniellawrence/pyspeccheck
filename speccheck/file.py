#!/usr/bin/env python

from .util import SpecError, colors, Spec

class File(Spec):

    STATES = [
        "directory", "file"
    ]

    def __init__(self, path):
        self.path = path
        self.state = {}
        self.get_state()
        self.WIN = "File %s is %%s correctly" % self.path

    def get_state(self):
        import os, stat, pwd, grp
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

    def sb_directory(self, *args):
        if self._make_sure(self.state['directory']):
            return True
        return "%s is not a directory" % (self.path)

    def sb_file(self, *args):
        if self._make_sure(self.state['file']):
            return True
        return "%s is not a file" % (self.path)
