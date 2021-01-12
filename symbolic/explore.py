# Copyright: see copyright.txt

from collections import deque
import logging, coverage, func_timeout
import os

from .z3_wrap import Z3Wrapper
from .path_to_constraint import PathToConstraint
from .invocation import FunctionInvocation
from .symbolic_types import symbolic_type, SymbolicType

log = logging.getLogger("se.conc")

class ExplorationEngine:
	def __init__(self, funcinv, solver="z3", statsdir=None, root=None):
		self.statsdir = statsdir; self.root = root
		if self.statsdir: os.system(f"rm -rf '{statsdir}'"); os.system(f"mkdir -p '{statsdir}'")

		self.invocation = funcinv
		# the input to the function
		self.symbolic_inputs = {}  # string -> SymbolicType
		# initialize
		for n in funcinv.getNames():
			self.symbolic_inputs[n] = funcinv.createArgumentValue(n)

		self.constraints_to_solve = deque([])
		self.num_processed_constraints = 0

		self.path = PathToConstraint(lambda c : self.addConstraint(c))
		# link up SymbolicObject to PathToConstraint in order to intercept control-flow
		symbolic_type.SymbolicObject.SI = self.path

		if solver == "z3":
			self.solver = Z3Wrapper()
		elif solver == "cvc":
			from .cvc_wrap import CVCWrapper
			self.solver = CVCWrapper(self.statsdir)
		else:
			raise Exception("Unknown solver %s" % solver)

		# outputs
		self.generated_inputs = []
		self.execution_return_values = []

	def addConstraint(self, constraint):
		self.constraints_to_solve.append(constraint)
		# make sure to remember the input that led to this constraint
		constraint.inputs = self._getInputs()

	def _explore_loop(self, max_iterations):
		self.tried_input_args = []
		self._oneExecution(); iterations = 1
		if max_iterations != 0 and iterations >= max_iterations:
			log.debug("Maximum number of iterations reached, terminating")
			return self.execution_return_values

		while not self._isExplorationComplete():
			selected = self.constraints_to_solve.popleft()
			if selected.processed:
				continue
			self._setInputs(selected.inputs)

			log.info("Selected constraint %s" % selected)
			asserts, query = selected.getAssertsAndQuery()
			model = self.solver.findCounterexample(asserts, query)

			if model == None:
				continue
			else:
				for name in model.keys():
					self._updateSymbolicParameter(name,model[name])

			if self.symbolic_inputs in self.tried_input_args: continue # don't run repeated inputs
			self._oneExecution(selected)

			iterations += 1
			self.num_processed_constraints += 1

			if max_iterations != 0 and iterations >= max_iterations:
				log.info("Maximum number of iterations reached, terminating")
				break

	def explore(self, max_iterations=0, total_timeout=900):
		if self.root: self.coverage = coverage.Coverage(data_file=None, include=[self.root + '/**'])
		if self.root: self.coverage.start()

		try: func_timeout.func_timeout(total_timeout, self._explore_loop, args=(max_iterations,))
		except: pass

		if self.root:
			self.coverage.stop()
			total_lines = 0
			executed_lines = 0
			for file in self.coverage.get_data().measured_files():
				_, executable_lines, m_lines, _ = self.coverage.analysis(file)
				total_lines += len(set(executable_lines))
				executed_lines += len(set(executable_lines)) - len(m_lines) # Do not use "len(set(self.coverage_data.lines(file)))" here!!!
			if self.statsdir:
				with open(self.statsdir + '/coverage.txt', 'w') as f:
					f.write("{}/{} ({:.2%})\n".format(executed_lines, total_lines, (executed_lines/total_lines) if total_lines > 0 else 0))
		return self.generated_inputs, self.execution_return_values, self.path

	# private

	def _updateSymbolicParameter(self, name, val):
		self.symbolic_inputs[name] = self.invocation.createArgumentValue(name,val)

	def _getInputs(self):
		return self.symbolic_inputs.copy()

	def _setInputs(self,d):
		self.symbolic_inputs = d

	def _isExplorationComplete(self):
		num_constr = len(self.constraints_to_solve)
		if num_constr == 0:
			log.info("Exploration complete")
			return True
		else:
			log.info("%d constraints yet to solve (total: %d, already solved: %d)" % (num_constr, self.num_processed_constraints + num_constr, self.num_processed_constraints))
			return False

	def _getConcrValue(self,v):
		if isinstance(v,SymbolicType):
			return v.getConcrValue()
		else:
			return v

	def _recordInputs(self):
		args = self.symbolic_inputs; inputs = {}
		# inputs = [ (k,self._getConcrValue(args[k])) for k in args ]
		for (k, v) in args.items(): inputs[k] = self._getConcrValue(v)
		self.generated_inputs.append(inputs)
		print(inputs)
		
	def _oneExecution(self,expected_path=None):
		self._recordInputs()
		self.path.reset(expected_path)
		ret = self.invocation.callFunction(self.symbolic_inputs)
		print(ret); self.tried_input_args.append(self.symbolic_inputs.copy())
		self.execution_return_values.append(ret)

