from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "data/tareas.db"

# -------------------------
# CONEXIÓN A LA BD
# -------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------
# CREAR BD SI NO EXISTE
# -------------------------
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            completada BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# GET TODAS LAS TAREAS
# -------------------------
@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    conn = get_db()
    tareas = conn.execute("SELECT * FROM tareas").fetchall()
    conn.close()
    return jsonify([dict(t) for t in tareas])

# -------------------------
# GET TAREA POR ID
# -------------------------
@app.route("/tareas/<int:id>", methods=["GET"])
def obtener_tarea(id):
    conn = get_db()
    tarea = conn.execute(
        "SELECT * FROM tareas WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    if tarea:
        return jsonify(dict(tarea))
    return jsonify({"error": "Tarea no encontrada"}), 404

# -------------------------
# POST NUEVA TAREA
# -------------------------
@app.route("/tareas", methods=["POST"])
def crear_tarea():
    datos = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tareas (titulo, completada) VALUES (?, ?)",
        (datos.get("titulo"), False)
    )
    conn.commit()
    nueva_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": nueva_id,
        "titulo": datos.get("titulo"),
        "completada": False
    }), 201

# -------------------------
# PUT ACTUALIZAR TAREA
# -------------------------
@app.route("/tareas/<int:id>", methods=["PUT"])
def actualizar_tarea(id):
    datos = request.json
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tareas
        SET titulo = ?, completada = ?
        WHERE id = ?
    """, (
        datos.get("titulo"),
        datos.get("completada", False),
        id
    ))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    if updated == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify({"mensaje": "Tarea actualizada"})

# -------------------------
# DELETE TAREA
# -------------------------
@app.route("/tareas/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Tarea no encontrada"}), 404

    return jsonify({"mensaje": "Tarea eliminada"})

@app.route("/saludo")
def saludo():
    return jsonify({"mensaje": "Hola desde Docker con SQLite!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
