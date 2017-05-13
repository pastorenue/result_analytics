import hotshot
import os
import time

PROFILE_LOG_BASE = os.path.dirname(os.path.abspath(__file__))

def profile(log_file):
    if not os.path.isabs(log_file):
        log_file = os.path.join(PROFILE_LOG_BASE, log_file)

    def _outer(f):
        def _inner(*args, **kwargs):
            (base, ext) = os.path.splitext(log_file)
            #base = base + "-" + time.strftime("%Y%m%dT%H%M%S", time.gmtime())
            final_log_file = base + ext

            prof = hotshot.Profile(final_log_file)
            try:
                ret = prof.runcall(f, *args, **kwargs)
            finally:
                prof.close()
            return ret
        return _inner
    return _outer
