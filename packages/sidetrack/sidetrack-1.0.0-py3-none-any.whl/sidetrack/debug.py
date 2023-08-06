'''
debug.py: lightweight debug logging facility

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------

Copyright (c) 2019-2020 by the California Institute of Technology.  This code
is open-source software released under a 3-clause BSD license.  Please see the
file "LICENSE" for more information.
'''

# Everything is carefully conditionalized on __debug__.  This is meant to
# minimize the performance impact of this module by eliding everything when
# Python is running with the optimization flag -O.


# Logger configuration.
# .............................................................................

if __debug__:
    from   inspect import currentframe
    import logging
    from   os import path
    import sys

    # This next global variable makes a huge speed difference. It lets us avoid
    # calling logging.getLogger('packagename').isEnabledFor(logging.DEBUG)
    # at runtime in log() to test whether debugging is turned on.
    setattr(sys.modules[__package__], '_debugging', False)


# Exported functions.
# .............................................................................

def set_debug(enabled, dest = '-', show_thread = False):
    '''Turns on debug logging if 'enabled' is True; turns it off otherwise.

    Optional argument 'dest' changes the debug output to the given destination.
    The value can be a file path, or a single dash ('-') to indicate the
    console (standard output).  The default destination is the console.  For
    simplicity, only one destination is allowed at given a time; calling this
    function multiple times with different destinations simply switches the
    destination to the latest one.

    Optional argument 'show_thread' determines whether the name of the current
    thread prefixes every output line.  Setting the value to True is useful if
    the calling programming uses multiple threads; otherwise, it's probably
    best to leave it False to reduce clutter in the output.
    '''
    if __debug__:
        from logging import DEBUG, WARNING, FileHandler, StreamHandler
        setattr(sys.modules[__package__], '_debugging', enabled)

        # Set the appropriate output destination if we haven't already.
        if enabled:
            logger    = logging.getLogger(__package__)
            if show_thread:
                formatter = logging.Formatter('%(threadName)s %(message)s')
            else:
                formatter = logging.Formatter('%(message)s')
            # We only allow one active destination.
            for h in logger.handlers:
                logger.removeHandler(h)
            # We treat empty dest values as meaning "the default output".
            if dest in ['-', '', None]:
                handler = StreamHandler()
            else:
                handler = FileHandler(dest)
            handler.setFormatter(formatter)
            handler.setLevel(DEBUG)
            logger.addHandler(handler)
            logger.setLevel(DEBUG)
            setattr(sys.modules[__package__], '_logger', logger)
        elif getattr(sys.modules[__package__], '_logger'):
            logger = logging.getLogger(__package__)
            logger.setLevel(WARNING)


# You might think that the way to get the current caller info when the log
# function is called would be to use logger.findCaller(). I tried that, and it
# produced very different information, even when using various values of
# stacklevel as the argument. The code below instead uses the Python inspect
# module to get the correct stack frame at run time.

def log(s, *other_args):
    '''Logs a debug message. 's' can contain format directive, and the
    remaining arguments are the arguments to the format string.
    '''
    if __debug__:
        # This test for the level may seem redundant, but it's not: it prevents
        # the string format from always being performed if logging is not
        # turned on and the user isn't running Python with -O.
        if getattr(sys.modules[__package__], '_debugging'):
            __write_log(s.format(*other_args), currentframe().f_back)


def logr(s):
    '''Logs a debug message. 's' is taken as-is; unlike log(...), logr(...)
    does not apply format to the string.
    '''
    if __debug__:
        # This test for the level may seem redundant, but it's not: it prevents
        # the string format from always being performed if logging is not
        # turned on and the user isn't running Python with -O.
        if getattr(sys.modules[__package__], '_debugging'):
            __write_log(s, currentframe().f_back)


# Internal helper functions.
# .............................................................................

def __write_log(s, frame):
    func   = frame.f_code.co_name
    lineno = frame.f_lineno
    file   = path.basename(frame.f_code.co_filename)
    logger = logging.getLogger(__package__)
    logger.debug(f'{file}:{lineno} {func}() -- ' + s)
