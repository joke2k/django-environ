
import os
import sys
from itertools import chain
from string import Template as StringTemplate

from .compat import ExitStack

def iter_properties(iterable):
    for line in iterable:
        if not line.isspace() and not line.startswith('#'):
            key, sep, val = line.partition(':=')
            if not sep:
                key, sep, val = line.partition('=')
            if not key.isspace() and sep:
                yield key.strip(), val.strip()

def interpolated(d, context=None):
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

def resolve_files(filenames, defaults=None, overrides=None, iterator=None):
    with ExitStack() as stack:
        return resolve(
            [stack.enter_context(open(f)) for f in filenames],
            defaults,
            overrides,
            iterator
        )

