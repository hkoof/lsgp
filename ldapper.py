import time
import logging
import bonsai

import prog

log = logging.getLogger(prog.name)

class AsyncJob:
    def __init__(self, msgid, callback, args, kwargs):
        log.debug("AsyncJob({} {} {} {})".format(msgid, callback, args, kwargs))
        self.msgid = msgid
        self.callback = callback
        self.args = args
        self.kwargs = kwargs


class Connection:
    def __init__(self, config):
        self._config = config
        self._client = bonsai.LDAPClient(self._config['url'])
        self._client.set_credentials("SIMPLE", (self._config['binddn'], self._config['password']))
        self._connection = bonsai.LDAPConnection(self._client, is_async=True)
        self._jobs = list()

    def open(self, callback, *args, **kwargs):
        msgid = self._connection.open()
        if callback is None:
            self._wait(msgid)
            return
        job = AsyncJob(msgid, callback, args, kwargs)
        self._jobs.append(job)

    def close(self):
        if hasattr(self, '_connection'): 
            self._connection.close()

    def __del__(self):
        self.close()

    def fileno(self):
        return self._connection.fileno()

    def poll(self):
        '''Handle async jobs ready to be processed.'''
        i = 0
        for job in self._jobs[:]:  # iterate shallow copy so we can delete items while looping it
            job_result = self._connection.get_result(job.msgid)
            if job_result is not None:
                try:
                    log.debug("Calling back: {} {} {}".format(job.callback, job.args, jobs.kwargs))
                    job.callback(job_result, *job.args, **job.kwargs)
                finally:
                    del self._jobs[i]
                    log.debug("Deleted job for msgid={}".format(job.msgid,))
            i += 1

    def _wait(self, msgid):
        i = 0
        result = None
        while result is None:
            time.sleep(0.1)
            i += 1
            log.debug("_wait({}): {} times".format(msgid, i))
            result = self._connection.get_result(msgid)
        return result 

    def search(self, base, scope, filter_, attrs, callback, *args, **kwargs):
        msgid = self._connection.search(base, scope, filter_, attrs)
        job = AsyncJob(msgid, callback, args, kwargs)
        self._jobs.append(job)

