from app import create_app, db
from flask import Flask
app = create_app()

# Для flask db
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print(app.template_folder)
    app.run(debug=True)
