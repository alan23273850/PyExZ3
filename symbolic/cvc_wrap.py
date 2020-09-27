import logging, os

import utils

import CVC4
from CVC4 import ExprManager, SmtEngine, SExpr

from symbolic.cvc_expr.exprbuilder import ExprBuilder

from symbolic.cvc_expr.integer import CVCInteger
from symbolic.cvc_expr.string import CVCString

log = logging.getLogger("se.cvc")


class CVCWrapper(object):
    options = {'produce-models': 'true',
               # Enable experimental string support
               'strings-exp': 'true',
               # Enable modular arithmetic with constant modulus
               'rewrite-divk': 'true',
               # Per Query timeout of 10 seconds
               'tlimit-per': 10000,
               'output-language': 'smt2',
               'input-language': 'smt2'}
    logic = 'ALL_SUPPORTED'

    def __init__(self, statsdir):
        self.asserts = None
        self.query = None
        self.em = None
        self.solver = None; self.cnt = 0; self.statsdir = statsdir
        self.stats = {'sat_number': 0, 'sat_time': 0, 'unsat_number': 0, 'unsat_time': 0, 'otherwise_number': 0, 'otherwise_time': 0}
        if self.statsdir: os.system(f"mkdir -p '{self.statsdir}/formula'")

    def findCounterexample(self, asserts, query):
        """Tries to find a counterexample to the query while
           asserts remains valid."""
        self.em = ExprManager()
        self.solver = SmtEngine(self.em)
        for name, value in CVCWrapper.options.items():
            self.solver.setOption(name, SExpr(str(value)))
        self.solver.setLogic(CVCWrapper.logic)
        self.query = query
        self.asserts = self._coneOfInfluence(asserts, query)
        result = self._findModel()
        log.debug("Query -- %s" % self.query)
        log.debug("Asserts -- %s" % asserts)
        log.debug("Cone -- %s" % self.asserts)
        log.debug("Result -- %s" % result)
        return result

    def _findModel(self):
        self.solver.push()
        exprbuilder = ExprBuilder(self.asserts, self.query, self.solver)
        var_to_types = {}
        for (k, v) in exprbuilder.cvc_vars.items():
            if isinstance(v, CVCInteger): var_to_types[k] = 'Int'
            elif isinstance(v, CVCString): var_to_types[k] = 'String'
            else: raise NotImplementedError
        self.solver.assertFormula(exprbuilder.query.cvc_expr)
        try:
            result = self.solver.checkSat()
            log.debug("Solver returned %s" % result.toString())
            if not result.isSat():
                status = "unsat"
                self.stats['unsat_number'] += 1; self.stats['unsat_time'] += self.solver.getTimeUsage() / 1000.0
                ret = None
            elif result.isUnknown():
                status = "UNKNOWN"
                self.stats['otherwise_number'] += 1; self.stats['otherwise_time'] += self.solver.getTimeUsage() / 1000.0
                ret = None
            elif result.isSat():
                status = "sat"
                self.stats['sat_number'] += 1; self.stats['sat_time'] += self.solver.getTimeUsage() / 1000.0
                ret = self._getModel(exprbuilder.cvc_vars)
            else:
                self.stats['otherwise_number'] += 1; self.stats['otherwise_time'] += self.solver.getTimeUsage() / 1000.0
                raise Exception("Unexpected SMT result")
            if self.statsdir:
                with open(self.statsdir + f"/formula/{self.cnt}_{status}.smt2", 'w') as f:
                    declare_vars = "\n".join(f"(declare-const {name} {_type})" for (name, _type) in var_to_types.items())
                    get_vars = "\n".join(f"(get-value ({name}))" for name in var_to_types.keys())
                    f.write(f"(set-logic ALL)\n{declare_vars}\n{exprbuilder.queries}\n(check-sat)\n{get_vars}\n")
            self.cnt += 1
        except RuntimeError as r:
            log.debug("CVC exception %s" % r)
            ret = None
        self.solver.pop()
        return ret

    @staticmethod
    def _getModel(variables):
        """Retrieve the model generated for the path expression."""
        return {name: cvc_var.getvalue() for (name, cvc_var) in variables.items()}

    @staticmethod
    def _coneOfInfluence(asserts, query):
        cone = []
        cone_vars = set(query.getVars())
        ws = [a for a in asserts if len(set(a.getVars()) & cone_vars) > 0]
        remaining = [a for a in asserts if a not in ws]
        while len(ws) > 0:
            a = ws.pop()
            a_vars = set(a.getVars())
            cone_vars = cone_vars.union(a_vars)
            cone.append(a)
            new_ws = [a for a in remaining if len(set(a.getVars()) & cone_vars) > 0]
            remaining = [a for a in remaining if a not in new_ws]
            ws = ws + new_ws
        return cone
