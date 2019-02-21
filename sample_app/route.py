from bottle import get, static_file, route, run


# Static Routes
@get("/assets/css/<file_path:re:.*\.css>")
def css(file_path):
    return static_file(file_path, root="./static/assets/css")


@get("/assets/image/<file_path:re:.*\.(jpg|png|gif|ico|svg)>")
def img(file_path):
    return static_file(file_path, root="./static/assets/image")


@get("/assets/js/<file_path:re:.*\.js>")
def js(file_path):
    return static_file(file_path, root="./static/assets/js")


@route('/download')
def download(file_name='Factom_Whitepaper_v1.2.pdf'):
    return static_file(file_name, root='./static/', download=file_name)


@route('/')
def server_static(file_path='index.html'):
    return static_file(file_path, root='./static/')


run(host='localhost', port=8080, debug=True)
