from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion'

# Inicializamos la lista de registros y el contador de ID en la sesión
@app.before_request
def iniciar_registros():
    if 'registros' not in session:
        session['registros'] = []
    if 'contador_id' not in session:
        session['contador_id'] = 1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nuevo_registro = {
            'id': session['contador_id'],
            'fecha': request.form['fecha'],
            'nombre': request.form['nombre'],
            'apellidos': request.form['apellidos'],
            'turno': request.form['turno'],
            'seminario': request.form['seminario']
        }

        session['registros'].append(nuevo_registro)
        session['contador_id'] += 1  # Incrementar el contador de ID
        session.modified = True
        return redirect(url_for('gestion'))

    return render_template('index.html')

@app.route('/gestion', methods=['GET', 'POST'])
def gestion():
    registros = session.get('registros', [])

    if request.method == 'POST':
        accion = request.form.get('accion')
        indice = int(request.form['indice'])

        if accion == 'eliminar':
            registros.pop(indice)
        elif accion == 'editar':
            return render_template('editar.html', registro=registros[indice], indice=indice)

        session['registros'] = registros
        session.modified = True

    return render_template('gestion.html', registros=registros)

@app.route('/actualizar/<int:indice>', methods=['POST'])
def actualizar(indice):
    registros = session['registros']
    registros[indice] = {
        'id': registros[indice]['id'],  # Mantener el ID original
        'fecha': request.form['fecha'],
        'nombre': request.form['nombre'],
        'apellidos': request.form['apellidos'],
        'turno': request.form['turno'],
        'seminario': request.form['seminario']
    }

    session['registros'] = registros
    session.modified = True
    return redirect(url_for('gestion'))

if __name__ == '__main__':
    app.run(debug=True)
