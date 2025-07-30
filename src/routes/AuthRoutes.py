from flask import Blueprint, request, render_template, redirect, url_for, session

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        # Usuario fijo por ahora
        if usuario == "admin" and password == "1234":
            session["usuario"] = usuario
            return redirect(url_for("chat.index"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("auth.login"))
