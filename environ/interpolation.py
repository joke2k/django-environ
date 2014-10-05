
import os
import sys
from itertools import chain
from string import Template as StringTemplate
import logging

from compat import ExitStack, basestring

logger = logging.getLogger(__file__)

def iter_properties(iterable):
    """Split lines on '=' and ':=' ignoring blank lines and comments.
    """
    for line in iterable:
        if not line.isspace() and not line.startswith('#'):
            key, sep, val = line.partition(':=')
            if not sep:
                key, sep, val = line.partition('=')
            if not key.isspace() and sep:
                yield key.strip(), val.strip()

def interpolated(d, context=None):
    """Recursively interpolate dictionary values.

    The expected interpolation format is that defined within the stdlib
    `string.Template` class::

        $foo or ${foo}

    Will raise KeyError for missing keys and ValueError for invalid keys.
    """
    if context is None:
        context = dict(d)
    unresolved = {}
    for k,v in d.items():
        newval = StringTemplate(v).substitute(context)
        if StringTemplate.pattern.search(newval):
            unresolved[k] = newval
        else:
            context[k] = newval
    if unresolved:
        context.update(interpolated(unresolved, context))
    return context

def resolve(iterables, defaults=None, overrides=None, iterator=None):
    """
    Create a dictionary from an 'iterable of iterables' and interpolate the
    values within the result. Each iterable instance is expected to yield a
    key/value pair (ie. a 2-tuple of strings). Duplicate keys are allowed,
    with later keys will overriding earlier.
    """
    if not defaults:
        initial = {}
    else:
        # deepcopy?
        initial = dict(defaults)
    if overrides is None:
        overrides = {}
    iterator = iterator or iter_properties
    initial.update(dict(chain(*[iterator(item) for item in iterables])))
    result = interpolated(initial)
    result.update(overrides)
    return result

def resolve_files(files, defaults=None, overrides=None, iterator=None):
    """Create a a dictionary from one or more 'property' or 'env' files and
    interpolate the resulting values.
    """
    with ExitStack() as stack:
        iterables = []
        for f in files:
            if isinstance(f, basestring):
                iterables.append(stack.enter_context(open(f)))
            else:
                iterables.append(stack.enter_context(f))
        return resolve(iterables, defaults, overrides, iterator)

