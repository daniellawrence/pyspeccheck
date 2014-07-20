#!/usr/bin/env python


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


class Spec(object):

    STATES = []
    WIN = "Spec is %s correctly"

    def __init__(self):
        self.get_state()

    def get_state(self):
        raise NotImplemented("")

    def __exit__(self, type, value, traceback):
        pass

    def __enter__(self):
        return self

    def _should_be(self, *args):
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
        if all_ok is True:
            print colors.win(self.WIN % (desired_state))
        else:
            print colors.fail(all_ok)

    def should_not_be(self, *args):
        desired_state = args[0]
        all_ok = self._should_be(*args)
        if all_ok is True:
            print colors.fail(self.WIN % (desired_state))
        else:
            print colors.win(all_ok)

    def _make_sure(self, x, y=True):
        if x == y:
            return True
        else:
            return False
