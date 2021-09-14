import os
from collections.abc import MutableMapping


class FileAwareMapping(MutableMapping):
    """
    A mapping that wraps os.environ, first checking for the existance of a key
    appended with ``_FILE`` whenever reading a value. If a matching file key is
    found then the value is instead read from the file system at this location.

    By default, values read from the file system are cached so future lookups
    do not hit the disk again.

    A ``_FILE`` key has higher precidence than a value is set directly in the
    environment, and an exception is raised if the file can not be found.
    """

    def __init__(self, env=None, cache=True):
        """
        Initialize the mapping.

        :param env:
            where to read environment variables from (defaults to
            ``os.environ``)
        :param cache:
            cache environment variables read from the file system (defaults to
            ``True``)
        """
        self.env = env if env is not None else os.environ
        self.cache = cache
        self.files_cache = {}

    def __getitem__(self, key):
        if self.cache and key in self.files_cache:
            return self.files_cache[key]
        key_file = self.env.get(key + "_FILE")
        if key_file:
            with open(key_file) as f:
                value = f.read()
            if self.cache:
                self.files_cache[key] = value
            return value
        return self.env[key]

    def __iter__(self):
        """
        Iterate all keys, also always including the shortened key if ``_FILE``
        keys are found.
        """
        for key in self.env:
            yield key
            if key.endswith("_FILE"):
                no_file_key = key[:-5]
                if no_file_key and no_file_key not in self.env:
                    yield no_file_key

    def __len__(self):
        """
        Return the length of the file, also always counting shortened keys for
        any ``_FILE`` key found.
        """
        return len(tuple(iter(self)))

    def __setitem__(self, key, value):
        self.env[key] = value
        if self.cache and key.endswith("_FILE"):
            no_file_key = key[:-5]
            if no_file_key and no_file_key in self.files_cache:
                del self.files_cache[no_file_key]

    def __delitem__(self, key):
        file_key = key + "_FILE"
        if file_key in self.env:
            del self[file_key]
            if key in self.env:
                del self.env[key]
            return
        if self.cache and key.endswith("_FILE"):
            no_file_key = key[:-5]
            if no_file_key and no_file_key in self.files_cache:
                del self.files_cache[no_file_key]
        del self.env[key]
