from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from app.db import get_db, hash_password

# Definir el Blueprint principal
main = Blueprint("main", __name__)

# ---------------------------
# Página principal
# ---------------------------
@main.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)

# ---------------------------
# Login
# ---------------------------
@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form["correo"]
        password = request.form["password"]
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Usuario WHERE correo=%s", (correo,))
        user = cur.fetchone()
        cur.close()

        if user and user["password_hash"] == hash_password(password):
            session["user"] = user
            if user["tipo"] == "Administrador":
                return redirect(url_for("main.admin_dashboard"))
            else:
                return redirect(url_for("main.usuario_dashboard"))
        else:
            flash("Correo o contraseña incorrectos.", "danger")
    return render_template("login.html")

# ---------------------------
# Registro de usuario
# ---------------------------
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]
        tipo = request.form["tipo"]

        conn = get_db()
        cur = conn.cursor()

        # Verificar si ya existe el correo
        cur.execute("SELECT id_usuario FROM Usuario WHERE correo=%s", (correo,))
        if cur.fetchone():
            flash("⚠️ El correo ya está registrado.", "warning")
            cur.close()
            return redirect(url_for("main.register"))

        # Insertar nuevo usuario
        cur.execute("""
            INSERT INTO Usuario (nombre, correo, tipo, fecha_registro, password_hash)
            VALUES (%s, %s, %s, CURDATE(), %s)
        """, (nombre, correo, tipo, hash_password(password)))
        conn.commit()
        cur.close()

        flash("✅ Usuario registrado correctamente. Inicia sesión.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")

# ---------------------------
# Panel del Usuario
# ---------------------------
@main.route("/usuario")
def usuario_dashboard():
    user = session.get("user")
    if not user or user["tipo"] != "Estudiante":
        return redirect(url_for("main.login"))
    return render_template("usuario.html", user=user)

# ---------------------------
# Panel del Administrador (con estadísticas)
# ---------------------------
@main.route("/admin")
def admin_dashboard():
    user = session.get("user")
    if not user or user["tipo"] != "Administrador":
        return redirect(url_for("main.login"))

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # Obtener conteos desde la base de datos
    cur.execute("SELECT COUNT(*) AS total_usuarios FROM Usuario")
    total_usuarios = cur.fetchone()["total_usuarios"]

    cur.execute("SELECT COUNT(*) AS total_libros FROM Libro")
    total_libros = cur.fetchone()["total_libros"]

    cur.execute("SELECT COUNT(*) AS total_prestamos FROM Prestamo")
    total_prestamos = cur.fetchone()["total_prestamos"]

    # Libros más prestados (TOP 5)
    cur.execute("""
        SELECT L.titulo, COUNT(P.id_prestamo) AS total
        FROM Prestamo P
        JOIN Libro L ON L.id_libro = P.id_libro
        GROUP BY L.titulo
        ORDER BY total DESC
        LIMIT 5
    """)
    top_libros = cur.fetchall()

    cur.close()

    return render_template(
        "admin.html",
        user=user,
        total_usuarios=total_usuarios,
        total_libros=total_libros,
        total_prestamos=total_prestamos,
        top_libros=top_libros
    )

# ---------------------------
# Logout
# ---------------------------
@main.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("main.index"))
