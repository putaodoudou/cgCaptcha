from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib import request
from urllib.parse import urlparse
import json
import time
from PIL import Image
from io import BytesIO
import imageProcess

curdir = path.dirname(path.realpath(__file__))
sep = '/'

# MIME-TYPE
mimedic = [
    ('.html', 'text/html'),
    ('.htm', 'text/html'),
    ('.js', 'application/javascript'),
    ('.css', 'text/css'),
    ('.json', 'application/json'),
    ('.png', 'image/png'),
    ('.jpg', 'image/jpeg'),
    ('.gif', 'image/gif'),
    ('.txt', 'text/plain'),
    ('.avi', 'video/x-msvideo'),
]


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    global image_buf

    # GET
    def do_GET(self):
        sendReply = False
        querypath = urlparse(self.path)
        filepath, query = querypath.path, querypath.query

        if(querypath.path.startswith('/captcha')):
            url = 'http://zhengzu.cangoonline.net/cas/imageAuthentication?timeTmp=%d' % time.time()
            response = request.urlopen(url)

            data = response.read()
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            print('@@@@ new image fetched...')
            self.wfile.write(data)
            global image_buf
            image_buf = BytesIO(data)
            return

        if filepath.endswith('/'):
            filepath += 'index.html'
        filename, fileext = path.splitext(filepath)
        for e in mimedic:
            if e[0] == fileext:
                mimetype = e[1]
                sendReply = True

        print(path.realpath(curdir + sep +'public' + sep + filepath))
        if sendReply == True:
            try:
                with open(path.realpath(curdir + sep +'public' + sep + filepath), 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(content)
            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)
    # POST
    def do_POST(self):
        querypath = urlparse(self.path)
        if querypath.path == '/submit':
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length).decode('utf-8')
            if len(post_data) > 0:
                req = json.loads(post_data)
                print(req['lNumber'], req['operator'], req['rNumber'])
                global image_buf
                if(image_buf):
                    img = Image.open(image_buf)
                    imageProcess.process(img, req['lNumber'], req['operator'], req['rNumber'])
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write('{}'.encode('UTF-8'))

def run():
    port = 8000
    print('starting server, port', port)

    # Server settings
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()