import argparse, coverage, func_timeout, functools, importlib.util, inspect, multiprocessing, os, pickle, signal, subprocess, sys, time
os.system('/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -config /etc/X11/xorg.conf :1 &')

def SIGINT_handler(signum, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, SIGINT_handler)

parser = argparse.ArgumentParser(); parser.add_argument("mode"); parser.add_argument("project"); parser.add_argument("-i", "--iteration"); args = parser.parse_args()

if args.mode != '2':
    from conbyte.utils import get_module_from_rootdir_and_modpath
    from conbyte.utils import get_function_from_module_and_funcname
    import conbyte.explore; complete_primitive_arguments = conbyte.explore.ExplorationEngine._complete_primitive_arguments
else:
    import symbolic.loader; get_module_from_rootdir_and_modpath = symbolic.loader.Loader.get_module_from_rootdir_and_modpath
    import symbolic.loader; get_function_from_module_and_funcname = symbolic.loader.Loader.get_function_from_module_and_funcname
    import symbolic.invocation; complete_primitive_arguments = symbolic.invocation.FunctionInvocation._complete_primitive_arguments

rootdir = os.path.abspath(args.project); lib = rootdir + '/.venv/lib/python3.8/site-packages'
sys.path.insert(0, lib); sys.path.insert(0, rootdir); project_name = rootdir.split('/')[-1]

TOTAL_TIMEOUT = 15 * 60
