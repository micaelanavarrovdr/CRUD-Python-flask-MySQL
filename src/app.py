from flask import Flask, render_template, request, redirect, url_for, flash
import os 
import database as db
from dotenv import load_dotenv

load_dotenv() 

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'clave_secreta'  

# Rutas de la aplicación 
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    myresult = cursor.fetchall()

    # Convertir los datos a diccionario 
    insertObjet = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjet.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('index.html', data=insertObjet)

# Ruta para guardar usuarios en la BD con validación
@app.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    nombreusuario = request.form['nombreusuario']
    contraseña = request.form['contraseña']

    if nombreusuario and nombre and contraseña:
        cursor = db.database.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s OR nombreusuario = %s", (nombre, nombreusuario))
        existing_user = cursor.fetchone()

        if existing_user:
            if existing_user[1] == nombre:  # Comparar con la columna 'nombre'
                flash("Error: Ya existe una persona registrada con este nombre.", "danger")
            elif existing_user[2] == nombreusuario:  # Comparar con la columna 'nombreusuario'
                flash("Error: El nombre de usuario ya está en uso.", "danger")
            cursor.close()
            return redirect(url_for('home'))  # Redirigir y mostrar mensaje

        # Insertar nuevo usuario
        sql = "INSERT INTO usuarios (nombre, nombreusuario, contraseña) VALUES (%s, %s, %s)"
        data = (nombre, nombreusuario, contraseña)
        cursor.execute(sql, data)
        db.database.commit()
        cursor.close()
        flash("Usuario registrado con éxito.", "success")

    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
        cursor = db.database.cursor()
        sql = "DELETE FROM usuarios WHERE id=%s"
        data = (id,)
        cursor.execute(sql,data)
        db.database.commit()
        return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    nombreusuario = request.form['nombreusuario']
    contraseña = request.form['contraseña']

    if  nombre and nombreusuario and contraseña:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET nombre = %s, nombreusuario = %s, contraseña = %s WHERE id = %s"
        data = (nombre, nombreusuario, contraseña, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)
