# app/app.py
import os

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .calculadora import sumar, restar, multiplicar, dividir

app = Flask(__name__)
_dev_secret = "dev-secret-change-in-production"
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", _dev_secret)
csrf = CSRFProtect(app)


def _resultado_from_post() -> str | float | None:
    try:
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operacion = request.form["operacion"]

        if operacion == "sumar":
            return sumar(num1, num2)
        if operacion == "restar":
            return restar(num1, num2)
        if operacion == "multiplicar":
            return multiplicar(num1, num2)
        if operacion == "dividir":
            return dividir(num1, num2)
        return "Operación no válida"
    except ValueError:
        return "Error: Introduce números válidos"
    except ZeroDivisionError:
        return "Error: No se puede dividir por cero"


@app.get("/")
def index_get():
    return render_template("index.html", resultado=None)


@app.post("/")
def index_post():
    return render_template("index.html", resultado=_resultado_from_post())


if __name__ == "__main__":  # pragma: no cover
    # Quita debug=True para producción
    app.run(debug=True, port=5000, host="127.0.0.1")
