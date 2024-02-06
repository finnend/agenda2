from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'agenda'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    events = []

    if request.method == 'POST':
        nombre = request.form['nombre']
        fecha = request.form['fecha']
        hora = request.form['hora']
        datos_adicionales = request.form['datos_adicionales']
        mensaje_confirmacion = request.form['mensaje']
        confirmo_hora = request.form['confirmo']
        boleta = request.form['boleta']
        pago = request.form.get('pago')

        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute('''INSERT INTO paciente (NOMBRE, FECHA, hora, datos_adicionales,
                                 mensaje_confirmacion, confirmo_hora, boleta, pago) 
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                               (nombre, fecha, hora, datos_adicionales, mensaje_confirmacion, confirmo_hora, boleta, pago))
                mysql.connection.commit()

                # Limpiar la lista de eventos después de insertar un paciente
                events.clear()

                # Actualizar la lista de eventos después de insertar un paciente
                events.append({'title': nombre, 'date': f'{fecha} {hora}'})

        except Exception as e:
            return f"Error: {str(e)}"

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT NOMBRE, FECHA, hora FROM paciente")
            data = cursor.fetchall()

            # Limpiar la lista de eventos antes de poblarla nuevamente
            events.clear()

            for paciente in data:
                nombre = paciente[0]
                fecha_hora = f"{paciente[1]} {paciente[2]}"
                events.append({'title': nombre, 'date': fecha_hora})
    except Exception as e:
        return f"Error: {str(e)}"

    return render_template('base.html', events=events, data=data)

@app.route('/see', methods=['GET'])
def see():
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM paciente")
            data = cursor.fetchall()
        return render_template('see.html', data=data)
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    try:
        with mysql.connection.cursor() as cursor:
            if request.method == "POST":
                nombre = request.form['nombre']
                fecha = request.form['fecha']
                hora = request.form['hora']
                datos_adicionales = request.form['datos_adicionales']
                mensaje_confirmacion = request.form['mensaje']
                confirmo_hora = request.form['confirmo']
                boleta = request.form['boleta']
                pago = request.form['pago']

                cursor.execute("UPDATE paciente SET nombre = %s, fecha = %s, hora = %s, datos_adicionales = %s, mensaje_confirmacion = %s, confirmo_hora = %s, boleta = %s, pago = %s WHERE id = %s",
                               (nombre, fecha, hora, datos_adicionales, mensaje_confirmacion, confirmo_hora,boleta,pago, id))
                mysql.connection.commit()

                return redirect('/see')
            else:
                cursor.execute("SELECT * FROM paciente WHERE id = %s", (id,))
                paciente = cursor.fetchone()
                return render_template('update.html', paciente=paciente)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
