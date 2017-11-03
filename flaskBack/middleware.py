"""
Fichier qui gère les routes du middleware pour la connection au front en React.
On paramètre ici les routes, et on lance le serveur Flask avec le script runMiddleware.py
"""
from flask import Flask, request, make_response
from controller import Controller
from functools import wraps

controller = Controller()
app = Flask('middleware')

def add_response_headers(headers={}):
    """Custom decorator qui permet d'ajouter un header à une réponse"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

@app.route('/')
def hello():
    return "C'est le middleware !"

@app.route('/msg', methods=['POST'])
@add_response_headers({'Access-Control-Allow-Origin': '*'})
def response():
    """
        Seule route utile, accessible à partir de route/du/middleware/msg
    """
    if request.method == 'POST':
        message = request.form['message']
        token = request.form['token']
        response = controller.handle_message(message, token)
        return response
