#!/usr/bin/env python3
import os, subprocess, unittest
import conbyte.explore

class TestCodeSnippets(unittest.TestCase):
    dump = bool(os.environ.get('dump', False))
    def test_01(self): self._execute('01', "test", "build_in", {'a':0, 'b':0}) # OK
    def test_02(self): self._execute('02', "test", "call_obj", {'a':0, 'b':0}) # OK with deadcode [11, 26]
    def test_03(self): self._execute('03', "test", "do_abs", {'a':0, 'b':0}) # OK
    def test_04(self): self._execute('04', "test", "do_array", {'a':0, 'b':0}) # OK
    def test_05(self): self._execute('05', "test", "do_numbers", {'a':0, 'b':0}) # OK
    def test_06(self): self._execute('06', "test", "do_range", {'a':0, 'b':0}) # OK
    def test_07(self): self._execute('07', "test", "list_dict", {'a':0, 'b':0}) # OK
    def test_08(self): self._execute('08', "test", "loop", {'a':0, 'b':0}) # OK
    def test_09(self): self._execute('09', "test", "while_loop", {'a':0, 'b':0}) # OK
    def test_10(self): self._execute('10', "test/strings", "string_find", {'a':'', 'b':''}) # OK
    def test_11(self): self._execute('11', "test/strings", "string_in", {'a':'', 'b':''}) # OK
    def test_12(self): self._execute('12', "test/strings", "string_iter", {'a':'', 'b':''}) # OK
    def test_13(self): self._execute('13', "test/strings", "string_others", {'a':'', 'b':''}) # OK
    def test_14(self): self._execute('14', "test/strings", "string_replace", {'a':'', 'b':''}) # OK
    def test_15(self): self._execute('15', "test/strings", "string_slice", {'a':'', 'b':''}) # OK
    def test_16(self): self._execute('16', "test/strings", "string_startswith", {'a':'', 'b':''}) # OK
    def test_17(self): self._execute('17', "test/targets", "count_emma", {'statement':''}) # OK
    def test_18(self): self._execute('18', "test/targets", "multiplication_or_sum", {'num1':0, 'num2':0}) # OK with restriction by solver ability [6]
    def test_19(self): self._execute('19', "test/targets", "regex", {'string':''}) # TODO
    def test_20(self): self._execute('20', "test/targets/lib", "email__header_value_parser", {'value':''}) # OK
    def test_21(self): self._execute('21', "test/targets/lib", "httplib2___negotiatehttp", [["1", "2", "3"]]) # TODO: We currently do not support concolic lists.
    def test_22(self): self._execute('22', "test/targets/leetcode", "add_digits", {'num':0}) # OK
    def test_23(self): self._execute('23', "test/targets/leetcode", "findUnsortedSubarray", [[0]]) # TODO: We currently do not support concolic lists.
    def test_24(self): self._execute('24', "test/targets/leetcode", "fraction_to_decimal", {'numerator':2, 'denominator':3}) # OK (but [0,0] cannot lead to full coverage...)
    def test_25(self): self._execute('25', "test/targets/leetcode", "isLongPressedName", {'name':'', 'typed':''}) # OK
    def test_26(self): self._execute('26', "test/targets/leetcode", "numDecodings", {'s':''}) # OK
    def test_27(self): self._execute('27', "test/targets/leetcode", "restoreIpAddresses", {'s':''}) # OK
    def test_28(self): self._execute('28', "test/targets/leetcode", "reverseCheck", {'number':0}) # OK
    def test_29(self): self._execute('29', "test/targets/leetcode", "substring", {'s':''}) # OK
    def test_30(self): self._execute('30', "test/targets/leetcode", "substring2", {'s':''}) # OK
    def test_31(self): self._execute('31', "test/targets/leetcode", "ugly_number", {'num':0}) # OK
    def test_32(self): self._execute('32', "test/target_int/leetcode_int", "add_binary", {'a':'', 'b':''}) # OK
    def test_33(self): self._execute('33', "test/target_int/leetcode_int", "addStrings", {'num1':'', 'num2':''}) # OK
    def test_34(self): self._execute('34', "test/target_int/leetcode_int", "numDecodings", {'s':''}) # OK
    def test_35(self): self._execute('35', "test/target_int/leetcode_int", "restoreIpAddresses", {'s':''}) # OK
    def test_36(self): self._execute('36', "test/target_int/leetcode_int", "validIPAddress", {'IP':''}) # TODO 本來就還不行
    def test_37(self): self._execute('37', "test/target_int/leetcode_int", "validWordAbbreviation", {'word':'', 'abbr':''}) # OK
    def test_38(self): self._execute('38', "test/target_int/lib_int", "datetime__parse_hh_mm_ss_ff", {'tstr':''}) # OK
    def test_39(self): self._execute('39', "test/target_int/lib_int", "datetime__parse_isoformat_date", {'dtstr':''}) # OK
    def test_40(self): self._execute('40', "test/target_int/lib_int", "distutils_get_build_version", {'version':'MSC v.1212 abc'}) # OK with deadcode [26, 30], but [""] cannot lead to full coverage...
    def test_41(self): self._execute('41', "test/target_int/lib_int", "email__parsedate_tz", {'data':'Mon, 16 Nov 2009 13:32:02 +0100'}) # TODO 本來就還不行
    def test_42(self): self._execute('42', "test/target_int/lib_int", "http_parse_request", {'version':''}) # OK
    def test_43(self): self._execute('43', "test/target_int/lib_int", "ipaddress__ip_int_from_string", {'ip_str':''}) # TODO 本來就還不行
    def test_44(self): self._execute('44', "test/target_int/lib_int", "nntplib__parse_datetime", {'date_str':'000000000000'}) # OK, at least 11 digits for avoiding errors, and 12 digits for full coverage
    def test_45(self): self._execute('45', "test/target_int/lib_int", "smtpd_parseargs", {'arg1':'', 'arg2':''}) # OK with deadcode [28, 35, 40]
    def test_46(self): self._execute('46', "test/target_int/lib_int", "wsgiref_check_status", {'status':''}) # OK
    def test_47(self): self._execute('47', "test/feature", "read_str_from_file", {'a':'', 'b':''}) # OK
    def test_48(self): self._executesrv('48', "test/realworld/rpyc", "client", {'x':0}) # OK
    def test_49(self): self._execute('49', "test/realworld", "docxmlrpcserver", {'title':'', 'name':'', 'documentation':''}) # OK

    def _executesrv(self, _id, root, modpath, inputs):
        libpath = root + '/.venv/lib/python3.8/site-packages'; os.system('kill -KILL $(lsof -t -i:8080)')
        pid = subprocess.Popen(["python3", "test/realworld/rpyc/server.py"], env={**os.environ, 'PYTHONPATH': libpath + ':' + os.environ['PYTHONPATH']}).pid
        import time; time.sleep(1) # this short wait is very important!!! (for the client to connect)
        self._execute(_id, root, modpath, inputs, lib=libpath)
        os.system(f'kill -KILL {pid}')

    def _execute(self, _id, root, modpath, inputs, *, lib=None):
        if not self._omit(_id):
            self.iteration_max = 1
            engine = conbyte.explore.ExplorationEngine()
            iteration = 0
            while iteration == 0 or self._check_coverage(iteration, _id, missing_lines):
                engine.explore(modpath, inputs, root=root, deadcode=self._missing_lines(_id), lib=lib)
                total_lines, executed_lines, missing_lines = engine.coverage_statistics() # missing_lines: dict
                iteration += 1
            col_3 = str(list(map(lambda x: (list(x[0].values()), x[1]), engine.in_out)))[1:-1]
            print(modpath + ':', col_3)
        if self.dump: # Logging output section
            if self._omit(_id):
                with open(f'{_id}.csv', 'w') as f:
                    f.write(f'{_id}|-|-|-\n')
            else:
                col_1 = "{}/{} ({:.2%})".format(executed_lines, total_lines, (executed_lines/total_lines) if total_lines > 0 else 0)
                col_2 = str(sorted(list(missing_lines.values())[0]) if missing_lines else '')
                if col_2 == str(sorted(self._missing_lines(_id))):
                    col_1 += ' >> (100.00%)' #; col_2 += ' (dead code)'
                with open(f'{_id}.csv', 'w') as f:
                    f.write(f'{_id}|{col_1}|{col_2}|{col_3}\n')

    def _omit(self, _id):
        return _id in ('19', '21', '23', '36', '41', '43')

    @staticmethod
    def _missing_lines(_id):
        if _id == "02":
            return {11, 26}
        if _id == "18":
            return {6}
        if _id == "40":
            return {26, 30}
        if _id == "45":
            return {28, 35, 40}
        if _id == "48":
            return {34}
        return {} # empty dictionary

    def _check_coverage(self, iteration, _id, missing_lines: dict):
        if missing_lines: # we only care about the primary file
            missing_lines = list(missing_lines.values())[0]
        status = self.assert_equal(iteration, missing_lines, self._missing_lines(_id))
        return not (iteration == self.iteration_max or status) # := not (termination condition)

    def assert_equal(self, iteration, a, b):
        if iteration == self.iteration_max: self.assertEqual(a, b)
        return a == b
