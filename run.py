if __package__:
    from .app import app, db
else:
    from restful.app import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

def inicializar_app_web():
    with app.app_context():
        db.create_all()
    app.run(debug=True)