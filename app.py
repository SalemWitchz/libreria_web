from app import create_app

# Crea la instancia de Flask a partir de tu paquete principal
app = create_app()

if __name__ == "__main__":
    # Ejecuta localmente en modo desarrollo
    app.run(host="0.0.0.0", port=5000, debug=True)

