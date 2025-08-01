from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from services.RAGService import handle_query

chat_bp = Blueprint("chat", __name__)
_historial = []

@chat_bp.route("/", methods=["GET"])
def index():
    if "usuario" not in session:
        return redirect(url_for("auth.login"))
    return render_template("consultas.html")

@chat_bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No se envió ninguna pregunta"}), 400

    resultado = handle_query(question)
    _historial.append({
        "pregunta": question,
        "pregunta_reescrita": resultado["pregunta_reescrita"],
        "respuesta": resultado["respuesta"],
        "tiempo": resultado["tiempo"]
    })
    return jsonify({
        "response": resultado["respuesta"],
        "tiempo": resultado["tiempo"],
        "pregunta_reescrita": resultado["pregunta_reescrita"]
    })

@chat_bp.route("/historial", methods=["GET"])
def ver_historial():
    return jsonify({"historial": _historial[-10:]})
