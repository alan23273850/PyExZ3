#!/usr/bin/env python3
import os, subprocess, unittest, sys, time
import symbolic.explore
import symbolic.loader

class TestCodeSnippets(unittest.TestCase):
    dump = bool(os.environ.get('dump', False))
    def test_01(self): self._execute("test", "build_in", {'a':0, 'b':0}) # OK
    def test_02(self): self._execute("test", "call_obj", {'a':0, 'b':0}, {11, 15, 26}) # TODO: 26/29
    def test_03(self): self._execute("test", "do_abs", {'a':0, 'b':0}, {6}) # TODO: 3/4
    def test_04(self): self._execute("test", "do_array", {'a':0, 'b':0}) # OK
    def test_05(self): self._execute("test", "do_numbers", {'a':0, 'b':0}) # OK
    def test_06(self): self._execute("test", "do_range", {'a':0, 'b':0}) # OK
    def test_07(self): self._execute("test", "list_dict", {'a':0, 'b':0}) # OK
    def test_08(self): self._execute("test", "loop", {'a':0, 'b':0}) # OK
    def test_09(self): self._execute("test", "while_loop", {'a':0, 'b':0}) # OK
    def test_10(self): self._execute("test/strings", "string_find", {'a':'', 'b':''}) # OK
    def test_11(self): self._execute("test/strings", "string_in", {'a':'', 'b':''}) # OK
    def test_12(self): self._execute("test/strings", "string_iter", {'a':'', 'b':''}, {5}) # TODO: 4/5
    def test_13(self): self._execute("test/strings", "string_others", {'a':'', 'b':''}) # OK
    def test_14(self): self._execute("test/strings", "string_replace", {'a':'', 'b':''}) # OK
    def test_15(self): self._execute("test/strings", "string_slice", {'a':'', 'b':''}) # OK
    def test_16(self): self._execute("test/strings", "string_startswith", {'a':'', 'b':''}) # OK
    def test_17(self): self._execute("test/targets", "count_emma", {'statement':''}) # OK
    def test_18(self): self._execute("test/targets", "multiplication_or_sum", {'num1':0, 'num2':0}, {6}) # TODO: CVC4 cannot solve num1 * num2 >= 1000
    def test_19(self): self._execute("test/targets", "regex", {'string':''}, {8}) # TODO: 5/6
    def test_20(self): self._execute("test/targets/lib", "email__header_value_parser", {'value':''}, {15, 17, 18, 20, 22, 23, 25, 26, 27, 28, 30, 31, 33, 35}) # TODO: 10/24 (> 15 minutes)
    def test_21(self): self._execute("test/targets/leetcode", "add_digits", {'num':0}) # OK
    def test_22(self): self._execute("test/targets/leetcode", "fraction_to_decimal", {'numerator':0, 'denominator':0}, {13, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30}) # TODO: 11/23
    def test_23(self): self._execute("test/targets/leetcode", "isLongPressedName", {'name':'', 'typed':''}, {6, 7, 10, 12, 13, 16, 17, 18, 21, 22, 24}) # TODO: 4/15
    def test_24(self): self._execute("test/targets/leetcode", "numDecodings", {'s':''}, {12, 13, 14, 15, 18, 19, 20, 21, 24, 25}) # TODO: 5/15
    def test_25(self): self._execute("test/targets/leetcode", "restoreIpAddresses", {'s':''}, {7, 8, 9, 10, 11}) # TODO: 20/25
    def test_26(self): self._execute("test/targets/leetcode", "reverseCheck", {'number':0}) # OK
    def test_27(self): self._execute("test/targets/leetcode", "substring", {'s':''}, {17}) # TODO: 20/21
    def test_28(self): self._execute("test/targets/leetcode", "substring2", {'s':''}, {13, 14, 15, 16, 17}) # TODO: 18/23
    def test_29(self): self._execute("test/targets/leetcode", "ugly_number", {'num':0}) # OK
    def test_30(self): self._execute("test/target_int/leetcode_int", "add_binary", {'a':'', 'b':''}, {8, 9, 10, 11, 12, 13, 27, 28, 29, 30, 32}) # TODO: 12/23
    def test_31(self): self._execute("test/target_int/leetcode_int", "addStrings", {'num1':'', 'num2':''}, {32, 33, 35, 36, 37, 39, 40, 41, 42, 44, 45, 46, 48, 23, 24, 56, 30, 31}) # TODO: 24/42
    def test_32(self): self._execute("test/target_int/leetcode_int", "numDecodings", {'s':''}, {15, 16, 17, 18, 21, 22, 23, 24, 27, 28}) # TODO: 5/15
    def test_33(self): self._execute("test/target_int/leetcode_int", "restoreIpAddresses", {'s':''}, {8, 9, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 32, 33}) # TODO: 5/25
    def test_34(self): self._execute("test/target_int/leetcode_int", "validIPAddress", {'IP':''}, {26, 35, 37, 38}) # TODO: 16/20 (> 15 minutes)
    def test_35(self): self._execute("test/target_int/leetcode_int", "validWordAbbreviation", {'word':'', 'abbr':''}, {17, 18, 19, 21}) # TODO: 15/19
    def test_36(self): self._execute("test/target_int/lib_int", "datetime__parse_hh_mm_ss_ff", {'tstr':''}, {14, 15, 17, 18, 20, 21, 23, 25, 26, 27, 29, 31, 32, 33, 34, 36, 37, 38, 40, 41, 42, 43, 45, 46, 47, 48, 50, 51, 52, 53, 55}) # TODO: 8/39
    def test_37(self): self._execute("test/target_int/lib_int", "datetime__parse_isoformat_date", {'dtstr':''}, {8, 9, 11, 12, 14, 15, 16, 18, 19, 21, 22, 23, 25}) # TODO: 4/17
    def test_38(self): self._execute("test/target_int/lib_int", "distutils_get_build_version", {'version':''}, {10, 11, 13, 15, 17, 18, 19, 20, 22, 23, 24, 26, 28, 30}) # TODO: 9/23
    def test_39(self): self._execute("test/target_int/lib_int", "email__parsedate_tz", {'data':''}, {32, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82, 84, 87, 88, 89, 90, 91, 92, 93, 100, 102, 103, 106, 108}) # TODO: ?/? (> 15 minutes)
    def test_40(self): self._execute("test/target_int/lib_int", "http_parse_request", {'version':''}, {19, 20, 23, 24, 25, 26, 27}) # TODO: 12/19
    def test_41(self): self._execute("test/target_int/lib_int", "ipaddress__ip_int_from_string", {'ip_str':''}, {98, 99, 70, 71, 102, 103, 111, 16, 112, 113, 114, 115, 116, 117, 118, 119}) # TODO: 78/94 (> 15 minutes)
    def test_42(self): self._execute("test/target_int/lib_int", "nntplib__parse_datetime", {'date_str':''}, {11, 12, 13, 14, 15, 18, 19, 20, 21, 22}) # TODO: 4/14
    def test_43(self): self._execute("test/target_int/lib_int", "smtpd_parseargs", {'arg1':'', 'arg2':''}, {28, 35, 40}) # OK with deadcode [28, 35, 40]
    def test_44(self): self._execute("test/target_int/lib_int", "wsgiref_check_status", {'status':''}, {9, 10, 11, 12, 14}) # TODO: 5/10
    def test_45(self): self._execute("test/feature", "read_str_from_file", {'a':'', 'b':''}, {6}) # TODO: 6/7
    def test_46(self): self._executesrv("test/realworld/rpyc", "client", {'x':0}, {15, 16, 17, 18, 25, 26, 27, 28, 29, 30, 31, 32, 34}) # TODO: 7/20 ({34} is deadcode)
    def test_47(self): self._execute("test/realworld", "docxmlrpcserver", {'title':'', 'name':'', 'documentation':''}, {26}) # TODO: {26}

    def _executesrv(self, root, modpath, inputs, _missing_lines=set()):
        libpath = root + '/.venv/lib/python3.8/site-packages'; os.system('kill -KILL $(lsof -t -i:8080)')
        pid = subprocess.Popen(["python3", "../py-conbyte-official/test/realworld/rpyc/server.py"], env={**os.environ, 'PYTHONPATH': '../py-conbyte-official/' + libpath + ':' + os.environ['PYTHONPATH']}).pid
        time.sleep(1) # this short wait is very important!!! (for the client to connect)
        self._execute(root, modpath, inputs, _missing_lines, lib=libpath)
        os.system(f'kill -KILL {pid}')

    def _execute(self, root, modpath, inputs, _missing_lines=set(), *, lib=None):
        _id = sys._getframe(1).f_code.co_name.split('_')[1]
        if _id == 'executesrv': _id = sys._getframe(2).f_code.co_name.split('_')[1]
        if not self._omit(_id):
            self.iteration_max = 1; root = '../py-conbyte-official/' + root
            if os.path.abspath(root) not in sys.path: sys.path.insert(0, os.path.abspath(root))
            if lib:
                lib = '../py-conbyte-official/' + lib
                if os.path.abspath(lib) not in sys.path: sys.path.insert(0, os.path.abspath(lib))
            modpath = modpath.replace('/', '.')
            engine = symbolic.explore.ExplorationEngine(symbolic.loader.Loader(modpath, None, root, None), str(inputs))
            iteration = 0
            start = time.time()
            while iteration == 0 or self._check_coverage(iteration, _missing_lines, missing_lines):
                engine.explore(max_iterations=0, total_timeout=900, file_as_total=True)
                total_lines, executed_lines, missing_lines = engine.coverage_statistics() # missing_lines: dict
                iteration += 1
                # print(executed_lines, total_lines, missing_lines)
            finish = time.time()
            b, c, d, e, F, g = engine.solver.stats['sat_number'], engine.solver.stats['sat_time'], engine.solver.stats['unsat_number'], engine.solver.stats['unsat_time'], engine.solver.stats['otherwise_number'], engine.solver.stats['otherwise_time']
            # col_3 = str(list(map(lambda x: (list(x[0].values()), x[1]), engine.in_out)))[1:-1]
            # print(modpath + ':', col_3)
            # print(modpath + ':', _missing_lines)
            sys.path.remove(os.path.abspath(root))
        if self.dump: # Logging output section
            if self._omit(_id):
                with open(f'{_id}.csv', 'w') as f:
                    f.write(f'{_id}|-|-|-\n')
            else:
                col_1 = "{}/{} ({:.2%})".format(executed_lines, total_lines, (executed_lines/total_lines) if total_lines > 0 else 0)
                # col_2 = str(sorted(list(missing_lines.values())[0]) if missing_lines else '')
                # if col_2 == str(sorted(_missing_lines)):
                #     col_1 += ' >> (100.00%)' #; col_2 += ' (dead code)'
                with open(f'{_id}.csv', 'w') as f:
                    # echo "ID|Function|Line Coverage|Time (sec.)"
                    # echo "ID|Function|Line Coverage|Time (sec.)|# of SMT files|# of SAT|Time of SAT|# of UNSAT|Time of UNSAT|# of OTHERWISE|Time of OTHERWISE" > output.csv2 && dump=True pytest integration_test_pyconbyte.py --workers 4 && cp /dev/null paper_statistics/pyexz3_run_pyconbyte.csv && cat *.csv >> output.csv2 && rm -f *.csv && mv output.csv2 paper_statistics/pyexz3_run_pyconbyte.csv
                    cdivb = c / b if b else 0
                    edivd = e / d if d else 0
                    gdivF = g / F if F else 0
                    # f.write(f'{_id}|{root[len("../py-conbyte-official/"):].replace("/", ".") + "." + modpath}|{col_1}|{round(finish-start, 2)}\n')
                    f.write(f'{_id}|{root[len("../py-conbyte-official/"):].replace("/", ".") + "." + modpath}|{col_1}|{round(finish-start, 2)}|{b+d+F}|{b}|{round(cdivb, 2)}|{d}|{round(edivd, 2)}|{F}|{round(gdivF, 2)}\n')

    def _omit(self, _id):
        return False #_id in ('19', '21', '23', '36', '41', '43')

    def _check_coverage(self, iteration, _missing_lines, missing_lines: dict):
        if missing_lines: # we only care about the primary file
            missing_lines = list(missing_lines.values())[0]
        else:
            missing_lines = set()
        status = self.assert_equal(iteration, missing_lines, _missing_lines)
        return not (iteration == self.iteration_max or status) # := not (termination condition)

    def assert_equal(self, iteration, a, b):
        print(a)
        print(b)
        if iteration == self.iteration_max: self.assertEqual(a, b)
        return a == b
