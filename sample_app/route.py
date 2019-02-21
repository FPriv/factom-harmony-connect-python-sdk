# import module located on a parent folder, when you don't have a standard package structure
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bottle import get, static_file, route, run
from sample_app.simulate_notary import simulate_notary


# Static Routes
@get(r"/assets/css/<file_path:re:.*\.css>")
def css(file_path):
    return static_file(file_path, root="./static/assets/css")


@get(r"/assets/image/<file_path:re:.*\.(jpg|png|gif|ico|svg)>")
def img(file_path):
    return static_file(file_path, root="./static/assets/image")


@get(r"/assets/js/<file_path:re:.*\.js>")
def js(file_path):
    return static_file(file_path, root="./static/assets/js")


@route('/document')
def download(file_name='Factom_Whitepaper_v1.2.pdf'):
    return static_file(file_name, root='./static/', download=file_name)


@route('/')
def server_static(file_path='index.html'):
    return static_file(file_path, root='./static/')


@get('/simulate')
def simulate():
    return simulate_notary()


run(host='localhost', port=8080, debug=True)
