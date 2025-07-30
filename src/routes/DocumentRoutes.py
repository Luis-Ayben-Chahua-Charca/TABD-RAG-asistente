from flask import Blueprint, request, jsonify, render_template, current_app, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from services.VectorService import vectorizar_documento, obtener_documentos_vectorizados, eliminar_documento, reindexar_documento
from utils.file_utils import allowed_file

document_bp = Blueprint("documentos", __name__)

@document_bp.route("/documentos", methods=["GET"])
def vista_documentos():
    if "usuario" not in session:
       return redirect(url_for("auth.login"))
    return render_template("documentos.html")


@document_bp.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        carpeta_destino = current_app.config["UPLOAD_FOLDER"]
        path = os.path.join(carpeta_destino, filename)

        try:
            # 🔒 Asegurar que el directorio existe
            os.makedirs(carpeta_destino, exist_ok=True)

            # 💾 Guardar archivo
            file.save(path)

            # ⚙️ Vectorizar
            resultado = vectorizar_documento(path)
            return jsonify({"message": f"Archivo '{filename}' subido. {resultado}"})
        except Exception as e:
            return jsonify({"error": f"Error al guardar o procesar el archivo: {str(e)}"}), 500

    return jsonify({"error": "Formato de archivo no permitido"}), 400



@document_bp.route("/documentos/lista", methods=["GET"])
def lista_documentos():
    docs = obtener_documentos_vectorizados()
    return jsonify({"documentos": docs})


@document_bp.route("/delete", methods=["POST"])
def delete_document():
    nombre = request.json.get("nombre")
    if not nombre:
        return jsonify({"error": "Nombre de archivo requerido"}), 400

    resultado = eliminar_documento(nombre)
    return jsonify({"message": resultado})


@document_bp.route("/reindex", methods=["POST"])
def reindex_document():
    nombre = request.json.get("nombre")
    if not nombre:
        return jsonify({"error": "Nombre de archivo requerido"}), 400

    resultado = reindexar_documento(nombre)
    return jsonify({"message": resultado})
