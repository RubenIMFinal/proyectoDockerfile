from flask import Flask, jsonify, request
from flask_cors import CORS


#Flask → sirve para crear la aplicación web.
#jsonify → convierte datos de Python en JSON para enviarlos al cliente.
#request → permite leer datos enviados por el cliente (por ejemplo en POST o PUT).
#app = Flask(__name__) → crea la aplicación Flask.

app = Flask(__name__)
CORS(app)

# "Base de datos" en memoria
tareas = [
    {"id": 1, "titulo": "Comprar pan", "completada": False},
    {"id": 2, "titulo": "Estudiar Docker", "completada": True},
]

# GET - Obtener todas las tareas
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify(tareas)

# GET - Obtener una tarea por ID
@app.route("/tareas/<int:id>", methods=["GET"])
def obtener_tarea(id):
    tarea = next((t for t in tareas if t["id"] == id), None)
    if tarea:
        return jsonify(tarea)
    return jsonify({"error": "Tarea no encontrada"}), 404

# POST - Crear una nueva tarea
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.json
    nueva_tarea = {
        "id": tareas[-1]["id"] + 1 if tareas else 1,
        "titulo": datos.get("titulo"),
        "completada": False
    }
    tareas.append(nueva_tarea)
    return jsonify(nueva_tarea), 201

# PUT - Actualizar una tarea existente
@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    tarea = next((t for t in tareas if t["id"] == id), None)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    datos = request.json
    tarea["titulo"] = datos.get("titulo", tarea["titulo"])
    tarea["completada"] = datos.get("completada", tarea["completada"])
    return jsonify(tarea)

# DELETE - Eliminar una tarea
@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    global tareas
    tareas = [t for t in tareas if t["id"] != id]
    return jsonify({"mensaje": "Tarea eliminada"})

# Endpoint simple de saludo
@app.route("/saludo")
def saludo():
    return jsonify({"mensaje": "Hola desde Docker!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
