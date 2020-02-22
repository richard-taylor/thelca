import http.server
from http import HTTPStatus

from thelca.api import API
api = API('1.0.0')

from thelca.error import NotAuthorisedError, NotFoundError, NotSavedError

from thelca.translator import JSON, TranslationError
translate = JSON()

class Handler(http.server.BaseHTTPRequestHandler):

    server_version = 'TheElectricCat/0.1'
    sys_version = ''

    def token(self):
        if 'Authorization' in self.headers:
            auth = self.headers['Authorization']
            if auth.startswith('Bearer'):
                return auth[6:].strip()
        raise NotAuthorisedError()

    def send_json(self, json):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.encode('utf-8'))

    def receive_json(self):
        content_length = self.headers['Content-Length']
        length = int(content_length) if content_length else 0
        posted_bytes = self.rfile.read(length)
        if len(posted_bytes) == length:
            return posted_bytes.decode('utf-8')
        else:
            return "{}"

    def do_GET(self):
        if self.path.startswith('/v1/items/'):
            id = self.path[10:]
            try:
                item = api.read_item(id, self.token())
                self.send_json(translate.from_item(item))

            except NotFoundError:
                self.send_error(HTTPStatus.NOT_FOUND)
            except NotAuthorisedError:
                self.send_error(HTTPStatus.UNAUTHORIZED)
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self):
        if self.path == '/v1/items':
            json = self.receive_json()
            try:
                dict = translate.to_dictionary(json)
                item = api.create_item(dict, self.token())
                self.send_json(translate.from_item(item))

            except TranslationError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
            except NotSavedError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
            except NotAuthorisedError:
                self.send_error(HTTPStatus.UNAUTHORIZED)
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_PUT(self):
        if self.path.startswith('/v1/items/'):
            id = self.path[10:]
            json = self.receive_json()
            try:
                item = translate.to_item(json)
                api.update_item(id, item, self.token())
                self.send_json(translate.from_item(item))

            except TranslationError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
            except NotFoundError:
                self.send_error(HTTPStatus.NOT_FOUND)
            except NotSavedError as error:
                self.send_error(HTTPStatus.BAD_REQUEST, str(error))
            except NotAuthorisedError:
                self.send_error(HTTPStatus.UNAUTHORIZED)
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
