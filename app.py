from flask import Flask, render_template, request, jsonify
import calc
import json
from flask_cors import CORS
from simplify_json import parse_simplified_format
from flask import flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "your-secret-key"   # flash メッセージ用
CORS(app)  # CORS 有効化

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    print("Request JSON:", request.json)  # リクエストデータをログに記録
    print("Headers:", request.headers)   # ヘッダー情報をログに記録
    print("Method:", request.method)     # メソッド情報をログに記録

    formula = request.json.get("formula", "")
    if isinstance(formula, str):
        formula = formula.strip()
    params = request.json.get("params", [])
    if not isinstance(params, list):
        return jsonify({"error": "Invalid params format. Expected a list."}), 400
    vals = request.json.get("vals", "")
    if isinstance(vals, str):
        vals = vals.strip()

    param_list = [p.strip() for p in params if isinstance(p, str) and p.strip()]
    
    try:
        vals_dict = json.loads(vals)
    except json.JSONDecodeError:
        vals_dict = parse_simplified_format(vals)
    expr    = calc.setting_symbols(formula, *param_list)
    result  = calc.substitute_and_eval(expr, vals_dict)
    tex_formula = calc.latex_formula(formula, *param_list)
    tex_originformula = calc.latex_original_formula(formula)

    print("Response Data:", {
        "formula": formula,
        "params": param_list,
        "vals": vals_dict,
        "result": str(result.evalf()),
        "tex_formula": tex_formula,
        "tex_originformula": tex_originformula
    })

    return jsonify({
        "formula": formula,
        "params": param_list,
        "vals": vals_dict,
        "result": str(result.evalf()),
        "tex_formula": tex_formula,
        "tex_originformula": tex_originformula
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
