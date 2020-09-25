# Copyright: copyright.txt

import coverage, func_timeout, traceback
import inspect
import re
import os
import sys
import importlib
from .invocation import FunctionInvocation
from .symbolic_types import SymbolicInteger, SymbolicStr, getSymbolic

# The built-in definition of len wraps the return value in an int() constructor, destroying any symbolic types.
# By redefining len here we can preserve symbolic integer types.
import builtins
builtins.len = (lambda x : x.__len__())

class Loader:
	class EXCEPTION: pass # used to indicate occurrence of Exception during execution

	def __init__(self, modpath, entry, root, statsdir):
		# root + modpath = filename, plus entry ==> 4 basic elements!
		root = os.path.abspath(root); self.modpath = modpath
		self._fileName = root + '/' + self.modpath.replace('.', '/') + '.py'
		self._entryPoint = self.modpath.split('.')[-1] if entry is None else entry
		self._resetCallback(True)
		self.statsdir = statsdir

	def getFile(self):
		return self._fileName

	def getEntry(self):
		return self._entryPoint
	
	def createInvocation(self, inputs):
		inv = FunctionInvocation(self._execute, self._resetCallback, self.func)
		# func = self.app.__dict__[self._entryPoint]
		# argspec = inspect.getargspec(self.func)
		# check to see if user specified initial values of arguments
		# if "concrete_args" in func.__dict__:
		# 	for (f,v) in func.concrete_args.items():
		# 		if not f in argspec.args:
		# 			print("Error in @concrete: " +  self._entryPoint + " has no argument named " + f)
		# 			raise ImportError()
		# 		else:
		# 			Loader._initializeArgumentConcrete(inv,f,v)
		# if "symbolic_args" in func.__dict__:
		# 	for (f,v) in func.symbolic_args.items():
		# 		if not f in argspec.args:
		# 			print("Error (@symbolic): " +  self._entryPoint + " has no argument named " + f)
		# 			raise ImportError()
		# 		elif f in inv.getNames():
		# 			print("Argument " + f + " defined in both @concrete and @symbolic")
		# 			raise ImportError()
		# 		else:
		# 			s = getSymbolic(v)
		# 			if (s == None):
		# 				print("Error at argument " + f + " of entry point " + self._entryPoint + " : no corresponding symbolic type found for type " + str(type(v)))
		# 				raise ImportError()
		# 			Loader._initializeArgumentSymbolic(inv, f, v, s)
		para = inspect.signature(self.func).parameters.values()
		if inputs is None: # original version, we do not use this now...
			for a in para:
				if not a.name in inv.getNames():
					Loader._initializeArgumentSymbolic(inv, a.name, 0, SymbolicInteger)
		else:
			for v in para:
				if v.kind in [inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD]: continue # do not support *args, **kwargs currently
				if v.name in inputs:
					value = inputs[v.name]
				else:
					has_value = False
					if (t:=v.annotation) is not inspect._empty:
						try: value = t(); has_value = True # may raise TypeError: Cannot instantiate ...
						except: pass
					if not has_value:
						if (t:=v.default) is not inspect._empty: value = t
						else: value = ''
				if type(value) is int: Loader._initializeArgumentSymbolic(inv, v.name, value, SymbolicInteger)
				elif type(value) is str: Loader._initializeArgumentSymbolic(inv, v.name, value, SymbolicStr)
				else: Loader._initializeArgumentConcrete(inv, v.name, value)
		return inv

	# need these here (rather than inline above) to correctly capture values in lambda
	def _initializeArgumentConcrete(inv,f,val):
		inv.addArgumentConstructor(f, val, lambda n,v: val)

	def _initializeArgumentSymbolic(inv,f,val,st):
		inv.addArgumentConstructor(f, val, lambda n,v: st(n,v))

	# def executionComplete(self, return_vals):
	# 	if "expected_result" in self.app.__dict__:
	# 		return self._check(return_vals, self.app.__dict__["expected_result"]())
	# 	if "expected_result_set" in self.app.__dict__:
	# 		return self._check(return_vals, self.app.__dict__["expected_result_set"](),False)
	# 	else:
	# 		print(self._fileName + " contains no expected_result function")
	# 		return None

	@staticmethod
	def get_funcobj_from_modpath_and_funcname(modname, funcname):
		execute = importlib.import_module(modname)
		while '.' in funcname:
			print(execute.__dict__)
			execute = getattr(execute, funcname.split('.')[0])
			funcname = funcname.split('.')[1]
		return getattr(execute, funcname)

	# -- private

	def _resetCallback(self,firstpass=False):
		self.func = None
		if firstpass and self.modpath in sys.modules:
			print("There already is a module loaded named " + self.modpath)
			raise ImportError()
		try:
			if (not firstpass and self.modpath in sys.modules):
				del(sys.modules[self.modpath])
			self.func = self.get_funcobj_from_modpath_and_funcname(self.modpath, self._entryPoint)
			# if not self._entryPoint in self.app.__dict__ or not callable(self.app.__dict__[self._entryPoint]):
			# 	print("File " +  self._fileName + ".py doesn't contain a function named " + self._entryPoint)
			# 	raise ImportError()
		except Exception as arg:
			print("Couldn't import " + self.modpath)
			print(arg)
			raise ImportError()

	def _execute(self, args, kwargs):
		result = self.EXCEPTION()
		try:
			# result = self.app.__dict__[self._entryPoint](**args)
			result = func_timeout.func_timeout(15, self.func, args=args, kwargs=kwargs)
		except func_timeout.FunctionTimedOut as e:
			print('Timeout Input Vector:', args, kwargs); print(e) #; traceback.print_exc(); sys.exit(1)
			if self.statsdir:
				with open(self.statsdir + '/exception.txt', 'a') as f:
					print('Timeout Input Vector:', args, kwargs, file=f); print(e, file=f)
		except Exception as e:
			print('Exception Input Vector:', args, kwargs); print(e); traceback.print_exc()
			if self.statsdir:
				with open(self.statsdir + '/exception.txt', 'a') as f:
					print('Exception Input Vector:', args, kwargs, file=f); print(e, file=f)
		return result

	def _toBag(self,l):
		bag = {}
		for i in l:
			if i in bag:
				bag[i] += 1
			else:
				bag[i] = 1
		return bag

	def _check(self, computed, expected, as_bag=True):
		b_c = self._toBag(computed)
		b_e = self._toBag(expected)
		if as_bag and b_c != b_e or not as_bag and set(computed) != set(expected):
			print("-------------------> %s test failed <---------------------" % self._fileName)
			print("Expected: %s, found: %s" % (b_e, b_c))
			return False
		else:
			print("%s test passed <---" % self._fileName)
			return True