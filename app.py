from flask import Flask, request, jsonify
from sympy import integrate, Symbol, sympify
from sympy.core.sympify import SympifyError

app = Flask(__name__)

@app.route('/operacion/<string:integral>', methods=['GET'])
def get_integral(integral):
    x = Symbol('X')
    try:
        expr = sympify(integral)
        resultadoIntegral = integrate(expr, x)
        resultado = {"resultado": str(resultadoIntegral)}
    except SympifyError:
        resultado = {"error": "La expresión proporcionada no es válida"}
        return jsonify(resultado), 400
    except Exception as e:
        resultado = {"error": str(e)}
        return jsonify(resultado), 500
    
    return jsonify(resultado), 200

@app.route('/integrate', methods=['POST'])
def integrate_expression():
    try:
        data = request.get_json()
        expression = data['expression']
        variable = data.get('variable', 'X')
        print(expression)
        # Convert the variable to a SymPy symbol
        symbol = Symbol(variable)
        
        # Convert the expression to a SymPy expression and integrate it
        sympy_expression = sympify(expression)
        result = integrate(sympy_expression, symbol)
        
        print(str(result))
        return jsonify({'result': str(result)}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
