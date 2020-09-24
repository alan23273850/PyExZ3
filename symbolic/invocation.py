# Copyright: see copyright.txt

import inspect

class FunctionInvocation:
	def __init__(self, execute, reset, func):
		self.execute = execute # will be Loader._execute
		self.reset = reset
		self.arg_constructor = {}
		self.initial_value = {}
		self.func = func

	def callFunction(self, all_args):
		self.reset()
		args, kwargs = self._complete_primitive_arguments(self.func, all_args)
		return self.execute(args, kwargs)

	def addArgumentConstructor(self, name, init, constructor):
		self.initial_value[name] = init
		self.arg_constructor[name] = constructor

	def getNames(self):
		return self.arg_constructor.keys()

	def createArgumentValue(self,name,val=None):
		if val == None:
			val = self.initial_value[name]
		return self.arg_constructor[name](name,val)

	@staticmethod
	def _complete_primitive_arguments(f, all_args):
		args = []; kwargs = {}
		for v in inspect.signature(f).parameters.values():
			if v.kind in [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]: continue # ignore *args, **kwargs at last
			value = all_args[v.name]
			if v.kind is inspect.Parameter.KEYWORD_ONLY:
				kwargs[v.name] = value
			else: # v.kind in [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]:
				args.append(value)
		return args, kwargs
