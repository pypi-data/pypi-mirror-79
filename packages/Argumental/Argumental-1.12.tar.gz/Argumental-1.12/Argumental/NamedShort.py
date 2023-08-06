#!/usr/bin/env python3

import re

class NamedShort(object):
	"""
	abstract base class representas an argument that can be a name or a short name
	"""
	def __init__(self, fn, kwargs=None):
		# fn : function
		self.fn = fn
		if not kwargs:
			kwargs = dict()
		# documentation
		doc = self.fn.__doc__
		if doc:
			doc = re.sub('^\s+','',doc,flags=re.MULTILINE)

		_help = kwargs.get('help') or doc or ''
		_help = _help.lstrip('\n').lstrip(' ')
		_help = _help.rstrip(' ').rstrip('\n')
		self.help = _help
		# name : str
		self.name = kwargs.get('name') or (fn.__name__ if fn else '?')
		# short : str
		self.short = kwargs.get('short') or None

