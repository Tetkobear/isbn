#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Read and write shelve cache.

Implements The Basic Sequence and Mapping Protocol

NOTES:
1. cannot use context manager for shelve because py2
2. metacache has different incompatible formats in py2 and py3
"""


import os
import shelve
import datetime
from time import time as timestamp

DEFAULT_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '.metacache')


class Cache(object):

    """Read and write shelve cache."""

    def __init__(self, cache=DEFAULT_CACHE):
        """Initialize attributes."""
        self._sh = shelve
        self._cache = cache
        try:
            s = self._sh.open(self._cache)
        except:
            s = self._sh.open(self._cache, 'n')
        s.close()

    def __getitem__(self, key):
        """Read cache."""
        try:
            s = self._sh.open(self._cache)
            return s[key]['value'] if s[key] else None
        except KeyError:
            return None
        except ValueError:
            self.new()
            return None
        finally:
            s.close()

    def __setitem__(self, key, value):
        """Write to cache."""
        try:
            s = self._sh.open(self._cache)
            s[key] = {'value': value, 'timestamp': timestamp()}
            status = True
        except:
            status = False
        finally:
            s.close()
        return status

    def __delitem__(self, key):
        """Delete record with key."""
        try:
            s = self._sh.open(self._cache)
            del s[key]
        except KeyError:
            return
        except ValueError:
            self.new()
            return
        finally:
            s.close()

    def __iter__(self):
        """Iterator for values in Cache."""
        s = self._sh.open(self._cache)
        for k in self.keys():
            yield s[k]['value']
        s.close()

    def __len__(self):
        """Return the number of keys in cache."""
        return len(self.keys()) if self.keys() else 0

    def keys(self):
        """Return a list of keys."""
        try:
            s = self._sh.open(self._cache)
            return list(s.keys())
        finally:
            s.close()

    def items(self):
        """Iterator for items in Cache."""
        s = self._sh.open(self._cache)
        for k in self.keys():
            yield k, s[k]['value']
        s.close()

    def ts(self, key):
        """Return the timestamp of the record with key."""
        try:
            s = self._sh.open(self._cache)
            ts = s[key]['timestamp'] if s[key] else None
            if not ts:
                return
            fmt = '%Y-%m-%d %H:%M:%S'
            return datetime.datetime.fromtimestamp(ts).strftime(fmt)
        except KeyError:
            return
        except ValueError:
            self.new()
            return
        finally:
            s.close()

    def new(self):
        """Make new cache."""
        s = self._sh.open(self._cache, 'n')
        s.close()
