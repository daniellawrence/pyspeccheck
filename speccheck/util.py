#!/usr/bin/env python

global status
from collections import defaultdict


class SpecError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)

        # Now for your custom code...
        self.errors = errors


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @classmethod
    def fail(self, msg):
        return "%s%s%s" % (self.FAIL, msg, self.ENDC)

    @classmethod
    def win(self, msg):
        return "%s%s%s" % (self.OKGREEN, msg, self.ENDC)


class Status(object):

    def __init__(self):
        self.ok = []
        self.fail = []

    def add_fail(self, problem):
        self.fail.append(problem)

    def add_ok(self, problem):
        self.ok.append(problem)

    def get_problems(self):
        return self.fail

    def get_ok(self):
        return self.ok

    def status(self):
        if len(self.fail) != 0:
            return("Fail")
        return("OK")

    def __str__(self):
        return "%s" % " ".join(self.fail + self.ok)

    def nagios(self):
        state = "OK"
        if len(self.fail) > 0:
            state = "ERROR"
        if state == "OK":
            return "OK: %s/%s checks passed" % (
                len(self.ok), len(self.ok))
        else:
            return "ERROR: %s/%s checks failed" % (
                len(self.fail), len(self.ok + self.fail))

    def report(self):
        for ok in self.ok:
            print colors.win(ok)
        for fail in self.fail:
            print colors.fail(fail)


class Spec(object):

    STATES = []
    WIN = "Spec is %s"

    def __init__(self):
        self.get_state()

    def get_state(self):
        raise NotImplemented("")

    def __exit__(self, type, value, traceback):
        pass

    def __enter__(self):
        return self

    def _should_be(self, *args):
        global status
        if not status:
            raise Exception("WTF")
        self.status = status

        desired_state = args[0]
        if desired_state not in self.STATES:
            raise Exception("unknown state '%s' should be one of: %s" %
                            (desired_state, self.STATES))

        try:
            results = getattr(self, 'sb_%s' % desired_state)(*args[1:])
        except AttributeError as error:
            raise error

        return results

    def should_be(self, *args):
        desired_state = ' '.join(args).replace('_', ' ')
        all_ok = self._should_be(*args)
        msg = self.WIN % desired_state

        if isinstance(all_ok, tuple):
            state = all_ok[0]
            msg = all_ok[1]
        else:
            state = all_ok

        if state is True:
            self.status.add_ok(msg)
            return state
        else:
            self.status.add_fail(msg)
            return state

    def should_not_be(self, *args):
        desired_state = args[0]
        all_ok = self._should_be(*args)
        msg = self.WIN % desired_state

        if isinstance(all_ok, tuple):
            state = all_ok[0]
            msg = all_ok[1]
        else:
            state = all_ok

        if all_ok is True:
            self.status.add_fail(msg)
        else:
            msg = msg.replace(' is ',' is not ')
            self.status.add_ok(msg)

    def _make_sure(self, x, y=True):
        if x == y:
            return True
        else:
            return False

status = Status()
