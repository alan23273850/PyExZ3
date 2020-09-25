#!/usr/bin/env python3
import argparse, coverage, importlib, inspect, os, pickle, subprocess, sys, func_timeout

parser = argparse.ArgumentParser(); parser.add_argument("mode"); parser.add_argument("project"); args = parser.parse_args()

rootdir = os.path.abspath(args.project) + '/'; lib = rootdir + '.venv/lib/python3.8/site-packages'
sys.path.insert(0, lib); sys.path.insert(0, rootdir); project_name = rootdir[:-1].split('/')[-1]
os.system(f"rm -rf './project_statistics/{project_name}'")

for dirpath, _, _ in os.walk(rootdir):
    dirpath = os.path.abspath(dirpath) + '/'
    if dirpath != rootdir and not dirpath.startswith(rootdir + '.'):
        print(dirpath)
        os.system(f"touch '{dirpath}/__init__.py'")

# Please note this function must be executed in a child process, or
# the import action will affect the coverage measurement later.
def extract_function_list_from_modpath(modpath):
    ans = []#; print(modpath, '==> ', end='')
    try:
        mod = importlib.import_module(modpath)#; print(mod, end='')
        for _, obj in inspect.getmembers(mod):
            if inspect.isclass(obj):
                for _, o in inspect.getmembers(obj):
                    if inspect.isfunction(o):
                        if inspect.getmodule(o) == mod:
                            ans.append(o.__qualname__)#; print(o.__qualname__)
            elif inspect.isfunction(obj):
                if inspect.getmodule(obj) == mod:
                    ans.append(obj.__qualname__)#; print(obj.__qualname__)
    except Exception as e:
        pass
        # print('Exception: ' + str(e), end='')
    # print()
    return ans

for dirpath, _, files in os.walk(rootdir):
    dirpath += '/'
    for file in files:
        if file.endswith('.py'):
            modpath = os.path.abspath(dirpath + file)[len(rootdir):-3].replace('/', '.')
            if os.fork() == 0: # child process
                funcs = extract_function_list_from_modpath(modpath)
                for f in funcs:
                    if '<locals>' not in f: # cannot access nested functions
                        if (modpath, f) in [('arithmetic_analysis.newton_forward_interpolation', 'main')]: continue
                        if len(f.split('.')) == 2:
                            (a, b) = f.split('.')
                            if b.startswith('__') and not b.endswith('__'): b = '_' + a + b
                            f = a + '.' + b
                        if args.mode == '1': cmd = f"./py-conbyte.py -r '{rootdir}' '{modpath}' -s {f} {{}} -m 20 --lib '{lib}' --include_exception --dump_projstats"
                        else: cmd = f"./pyexz3.py -r '{rootdir}' '{modpath}' -s {f} {{}} -m 20 --lib '{lib}' --dump_projstats"
                        print(modpath, '+', f, '>>>'); print(cmd)
                        try: completed_process = subprocess.run(cmd, shell=True, stdout=sys.stdout, stderr=sys.stderr)
                        except subprocess.CalledProcessError as e: print(e.output); sys.exit(1)
                os._exit(os.EX_OK)
            os.wait()

if args.mode == '1':
    from conbyte.utils import get_funcobj_from_modpath_and_funcname
    import conbyte.explore; _complete_primitive_arguments = conbyte.explore.ExplorationEngine._complete_primitive_arguments
else:
    import symbolic.loader; get_funcobj_from_modpath_and_funcname = symbolic.loader.Loader.get_funcobj_from_modpath_and_funcname
    import symbolic.invocation; _complete_primitive_arguments = symbolic.invocation.FunctionInvocation._complete_primitive_arguments
func_inputs = {}; cov = coverage.Coverage(data_file=None, include=[rootdir + '**'])
cov.start()
for dirpath, _, files in os.walk(f"./project_statistics/{project_name}"):
    for file in files:
        if file == 'inputs.pkl':
            with open(os.path.abspath(dirpath + '/' + file), 'rb') as f:
                inputs = pickle.load(f)
            func_inputs[(dirpath.split('/')[-2], dirpath.split('/')[-1])] = inputs
            for i in inputs:
                f = get_funcobj_from_modpath_and_funcname(dirpath.split('/')[-2], dirpath.split('/')[-1])
                iargs, ikwargs = _complete_primitive_arguments(f, i)
                try: func_timeout.func_timeout(15, f, args=iargs, kwargs=ikwargs)
                except: pass
cov.stop()
total_lines = 0
executed_lines = 0
for file in cov.get_data().measured_files():
    _, executable_lines, m_lines, _ = cov.analysis(file)
    total_lines += len(set(executable_lines))
    executed_lines += len(set(executable_lines)) - len(m_lines)
    # print(file, executed_lines, total_lines)

with open(f"./project_statistics/{project_name}/inputs_and_coverage.txt", 'w') as f:
    for (func, inputs) in func_inputs.items():
        print(func, inputs, file=f)
    print("\nTotal line coverage {}/{} ({:.2%})".format(executed_lines, total_lines, (executed_lines/total_lines) if total_lines > 0 else 0), file=f)
print("\nTotal line coverage {}/{} ({:.2%})".format(executed_lines, total_lines, (executed_lines/total_lines) if total_lines > 0 else 0))
