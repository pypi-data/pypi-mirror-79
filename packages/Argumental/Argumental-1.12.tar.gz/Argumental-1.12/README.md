# Argumental

annotation descripters to put closuer on classes and objects to allow argparse to be easy to use

## Argue.py

A tool to decorate a python class to create an argparse ready command line application

Here is an example application

```python
#!/usr/bin/env python3

import os,re,sys,json

from Argumental.Argue import Argue

# the argument decorator
args = Argue()

# create a root level argparse argument.
@args.argument(short='v', flag=True)
def verbose():
	"""
	detailed output mode
	"""
	return False

## simple arg main code
# args.parse()
# print(args.verbose())
## or create a reusable decorated class for the command line

# create a subparser based on the class
@args.command(name="class", single=False) # True to bypass to methods
class MyClass(object):
	"""
	My Class
	"""

	# add an argparse value as a property, override class attributes
	@args.property(
		short='v',
		default='abc123',
		help='with built in setter and deleter'
	)
	def value(self): return

	# declare the method as a sub parser with method parameters
	@args.operation(
		name='method'
	)
	@args.parameter(
		param='myParameter',
		short='p',
		name='parameter',
		required=True,
		help='My Parameter'
	)
	@args.returns(
		type=dict,
		help='test values'
	)
	def myOperation(self, myParameter=None):
		"""
		My Operation
		"""
		return dict(
			myParameter=myParameter,
			value=self.value
		)


if __name__ == '__main__': args.execute()
```


# output

```bash
$ ./MyClass.py -h

usage: Argue.py [-h] [-v] {class,args} ...

positional arguments:
  {class,args}   commands
    class        My Class
    args         print the values for the args

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  detailed output mode
```

# sub paser for class

```bash
$ ./MyClass.py class -h

usage: Argue.py class [-h] [-v VALUE] {method} ...

positional arguments:
  {method}              operations
    method              My Operation

optional arguments:
  -h, --help            show this help message and exit
  -v VALUE, --value VALUE
                        with built in setter and deleter, default=abc123

```

# sub parser for method

```bash
$ ./MyClass.py class method -h

usage: Argue.py class method [-h] -p PARAMETER

optional arguments:
  -h, --help            show this help message and exit
  -p PARAMETER, --parameter PARAMETER
                        My Parameter

```

# and calling the method

```bash
$ ./MyClass.py class -v myv method -p myp

{
    "myParameter": "myp",
    "value": "myv"
}

```

