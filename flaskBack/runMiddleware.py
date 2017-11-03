#!flask/bin/python
"""
Script de lancement du middleware, qui permet la connection avec le Front en
React
"""

from middleware import app
app.run(debug=False, port=5001, host='0.0.0.0')
