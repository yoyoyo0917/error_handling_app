from sympy import sympify, latex
import sympy as sym
sym.init_printing()

def setting_symbols(formula, *pram):
    try:
        # すべての変数が指定されているか確認
        syms_in_formula = sym.sympify(formula).free_symbols
        syms_provided = set(sym.symbols(' '.join(pram)))
        missing_syms = syms_in_formula - syms_provided

        if missing_syms:
            raise ValueError(f"Missing symbols in parameters: {missing_syms}")

        a = sym.sympify(formula)
        syms = sym.symbols(' '.join(pram))
        err_names = [f'd{p}' for p in pram]
        errsyms = sym.symbols(' '.join(err_names))
        if not isinstance(syms, (tuple, list)):
            syms = (syms,)
            errsyms = (errsyms,)

        b = (sum((sym.diff(a, s) * e) ** 2 for s, e in zip(syms, errsyms))) ** 0.5

        return b
    except Exception as e:
        raise ValueError(f"Error in setting_symbols: {e}")

def substitute_and_eval(expr, values: dict, evalf: bool = True):
    """
    expr    : SymPy 式  (setting_symbols の戻り値など)
    values  : {'x': 1.2, 'dx': 0.05, ...} のような置換辞書
    evalf   : True なら数値化して float 相当を返す
              False なら置換だけ行い SymPy 式を返す
    """
    # 1) 名前を SymPy シンボルに変換しつつ辞書を再構築
    subs_dict = {sympify(k): v for k, v in values.items()}

    # 2) 置換
    substituted = expr.subs(subs_dict)

    # 3) 必要なら数値化して返す
    return substituted.evalf() if evalf else substituted

def latex_original_formula(formula):
    """
    LaTeX 形式の数式を返す
    """
    try:
        # 1) 数式を SymPy 式に変換
        a = sym.sympify(formula)

        # 2) LaTeX 形式に変換
        b = latex(a)

        return b
    except Exception as e:
        raise ValueError(f"Error in latex_original_formula: {e}")


def latex_formula(formula, *pram):
    try:
        # すべての変数が指定されているか確認
        syms_in_formula = sym.sympify(formula).free_symbols
        syms_provided = set(sym.symbols(' '.join(pram)))
        missing_syms = syms_in_formula - syms_provided

        if missing_syms:
            raise ValueError(f"Missing symbols in parameters: {missing_syms}")

        a = sym.sympify(formula)
        syms = sym.symbols(' '.join(pram))
        err_names = [f'd{p}' for p in pram]
        errsyms = sym.symbols(' '.join(err_names))
        if not isinstance(syms, (tuple, list)):
            syms = (syms,)
            errsyms = (errsyms,)
        terms = [f"\\left({latex(sym.diff(a, s))}{latex(e)}\\right)^2" for s, e in zip(syms, errsyms)]
        b = " + ".join(terms)
        b = f"\\sqrt{{{b}}}"

        return b
    except Exception as e:
        raise ValueError(f"Error in setting_symbols: {e}")




a = setting_symbols("3 * x ** 2 + 4 * y ** 3 + 1 / z", "x", "y", "z")

vals = {
    'x': 1.2,
    'dx': 0.05,
    'y': 2.3,
    'dy': 0.01,
    'z': 0.5,
    'dz': 0.001
}

result = substitute_and_eval(a, vals)

print(result)
