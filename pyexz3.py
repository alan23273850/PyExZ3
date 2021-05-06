#!/usr/bin/env python3
# Copyright: see copyright.txt

import os, pickle
import sys
import logging
import traceback
from optparse import OptionParser

from symbolic.loader import *
from symbolic.explore import ExplorationEngine

print("PyExZ3 (Python Exploration with Z3)")

sys.path = [os.path.abspath(os.path.join(os.path.dirname(__file__)))] + sys.path

usage = "usage: %prog [options] path.to.module input_dict"
parser = OptionParser(usage=usage)

parser.add_option("-r", "--root", dest="root", default=os.path.dirname(__file__))
parser.add_option("--lib", dest="lib", default=None)
parser.add_option("-l", "--log", dest="logfile", action="store", help="Save log output to a file", default="")
parser.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default=None)
parser.add_option("-g", "--graph", dest="dot_graph", action="store_true", help="Generate a DOT graph of execution tree")
parser.add_option("-m", "--max-iters", dest="max_iters", type=int, help="Run specified number of iterations", default=0)
parser.add_option("--cvc", dest="cvc", action="store_true", help="Use the CVC SMT solver instead of Z3", default=False)
parser.add_option("--z3", dest="cvc", action="store_false", help="Use the Z3 SMT solver")
parser.add_option("--dump_projstats", dest="dump_projstats", action='store_true')
parser.add_option("--file_as_total", dest="file_as_total", action='store_true')
parser.add_option("--total_timeout", dest="total_timeout", type=int, default=900)

(options, args) = parser.parse_args()

if not (options.logfile == ""):
	logging.basicConfig(filename=options.logfile,level=logging.DEBUG)

# if len(args) == 0 or not os.path.exists(options.root + args[0]):
# 	parser.error("Missing app to execute")
# 	sys.exit(1)

################################################################
if options.lib: sys.path.insert(0, os.path.abspath(options.lib))
sys.path.insert(0, os.path.abspath(options.root))
################################################################

solver = "cvc" #if options.cvc else "z3"

# filename = os.path.abspath(args[0])
funcname = t if (t:=options.entry) else args[0].split('.')[-1]
statsdir = os.path.abspath(os.path.dirname(__file__)) + '/project_statistics/' + os.path.abspath(options.root).split('/')[-1] + '/' + args[0] + '/' + funcname if options.dump_projstats else None

# Get the object describing the application
app = Loader(args[0], options.entry, options.root, statsdir)
if app == None:
	sys.exit(1)

# print ("Exploring " + app.getFile() + "." + app.getEntry())

result = None
try:
	engine = ExplorationEngine(app, args[1], solver=solver, statsdir=statsdir, root=options.root)
	generatedInputs, returnVals, path = engine.explore(options.max_iters, options.total_timeout, options.file_as_total)
	print(str(engine.coverage_statistics()[1]) + '/' + str(engine.coverage_statistics()[0]), engine.coverage_statistics()[2])
	if statsdir:
		with open(statsdir + '/inputs.pkl', 'wb') as f:
			pickle.dump(generatedInputs, f)
		with open(statsdir + '/smt.csv', 'w') as f:
			f.write(',number,time\n')
			f.write(f'sat,{engine.solver.stats["sat_number"]},{engine.solver.stats["sat_time"]}\n')
			f.write(f'unsat,{engine.solver.stats["unsat_number"]},{engine.solver.stats["unsat_time"]}\n')
			f.write(f'otherwise,{engine.solver.stats["otherwise_number"]},{engine.solver.stats["otherwise_time"]}\n')
	# check the result
	# result = app.executionComplete(returnVals)

	# output DOT graph
	if (options.dot_graph):
		file = open(filename+".dot","w")
		file.write(path.toDot())	
		file.close()

except ImportError as e:
	# createInvocation can raise this
	logging.error(e)
	sys.exit(1)

# if result == None or result == True:
# 	sys.exit(0);
# else:
# 	sys.exit(1);	
