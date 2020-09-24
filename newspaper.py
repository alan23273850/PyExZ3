#!/usr/bin/env python3
import coverage, importlib, inspect, os, pickle, subprocess, sys

lib = '/home/alan23273850/.local/share/virtualenvs/newspaper-BPbAuwkq/lib/python3.8/site-packages'; sys.path.insert(0, lib)
rootdir = os.path.abspath('../newspaper') + '/'; sys.path.insert(0, rootdir); project_name = rootdir[:-1].split('/')[-1]
os.system(f"rm -rf ./project_statistics/{project_name}")

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

for dirpath, _, files in os.walk(rootdir[:-1]):
    dirpath += '/'
    for file in files:
        if file.endswith('.py'):
            modpath = os.path.abspath(dirpath + file)[len(rootdir):-3].replace('/', '.')
            # if modpath != 'newspaper.api': continue
            if os.fork() == 0: # child process
                funcs = extract_function_list_from_modpath(modpath)
                for f in funcs:
                    if '<locals>' not in f: # cannot access nested functions
                        # if f != 'build': continue
                        # cmd = ['./py-conbyte.py', '-r', rootdir, modpath, '-s', f, '{}', '-m', '20', '--lib', lib, '--dump_projstats', '--ignore_return']
                        cmd = ['./pyexz3.py', '-r', rootdir, modpath, '-s', f, '{}', '-m', '20', '--lib', lib, '--dump_projstats']
                        print(modpath, '+', f, '>>>'); print(' '.join(cmd))
                        try: completed_process = subprocess.run(cmd, capture_output=True)
                        except subprocess.CalledProcessError as e: print(e.output); sys.exit(1)
                        print(completed_process.stderr.decode())
                        print(completed_process.stdout.decode())
                        try:
                            output = completed_process.stdout.decode().splitlines()[-1]
                        except Exception as e:
                            print(e); sys.exit(0)
                os._exit(os.EX_OK)
            os.wait()

func_inputs = {}; cov = coverage.Coverage(data_file=None, include=[rootdir + '**'])
cov.start()
for dirpath, _, files in os.walk(f"./project_statistics/{project_name}"):
    for file in files:
        if file == 'inputs.pkl':
            with open(os.path.abspath(dirpath + '/' + file), 'rb') as f:
                inputs = pickle.load(f)
            func_inputs[(dirpath.split('/')[-2], dirpath.split('/')[-1])] = inputs
            for i in inputs:
                import symbolic.invocation
                import symbolic.loader
                f = symbolic.loader.Loader.get_funcobj_from_modpath_and_funcname(dirpath.split('/')[-2], dirpath.split('/')[-1])
                iargs, ikwargs = symbolic.invocation.FunctionInvocation._complete_primitive_arguments(f, i)
                try: f(*iargs, **ikwargs)
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
