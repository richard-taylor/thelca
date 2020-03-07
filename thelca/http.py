import http.server
from http import HTTPStatus

from thelca.api import API
api = API('1.0.0')

from thelca.error import NotAuthorisedError, NotFoundError, NotSavedError

from thelca.translator import JSON, TranslationError
translate = JSON()

class Handler(http.server.BaseHTTPRequestHandler):

    server_version = 'TheElectricCat/0'
    sys_version = 'X'

    def token(self):
        if 'Authorization' in self.headers:
            auth = self.headers['Authorization']
            if auth.startswith('Bearer'):
                return auth[6:].strip()
        raise NotAuthorisedError()

    def send_text(self, text):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

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

    def do_DELETE(self):
        try:
            if self.path.startswith('/v1/links/'):
                id = self.path[10:]
                link = api.delete_link(id, self.token())
                self.send_json(translate.from_link(link))

            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        except NotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
        except NotAuthorisedError:
            self.send_error(HTTPStatus.UNAUTHORIZED)

    def do_GET(self):
        try:
            if self.path == '/':
                self.send_text('Meeeow\n')

            elif self.path.startswith('/v1/items/'):
                id = self.path[10:]
                item = api.read_item(id, self.token())
                self.send_json(translate.from_item(item))

            elif self.path.startswith('/v1/items?'):
                query = self.path[10:]
                items = api.search_items(query, self.token())
                self.send_json(translate.from_item_list(items))

            elif self.path.startswith('/v1/links/'):
                id = self.path[10:]
                link = api.read_link(id, self.token())
                self.send_json(translate.from_link(link))

            elif self.path.startswith('/v1/links?'):
                query = self.path[10:]
                links = api.search_links(query, self.token())
                self.send_json(translate.from_link_list(links))

            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        except NotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
        except NotAuthorisedError:
            self.send_error(HTTPStatus.UNAUTHORIZED)

    def do_POST(self):
        try:
            json = self.receive_json()
            dict = translate.to_dictionary(json)

            if self.path == '/v1/items':
                item = api.create_item(dict, self.token())
                self.send_json(translate.from_item(item))

            elif self.path == '/v1/links':
                link = api.create_link(dict, self.token())
                self.send_json(translate.from_link(link))

            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        except TranslationError as error:
            self.send_error(HTTPStatus.BAD_REQUEST, str(error))
        except NotSavedError as error:
            self.send_error(HTTPStatus.BAD_REQUEST, str(error))
        except NotAuthorisedError:
            self.send_error(HTTPStatus.UNAUTHORIZED)

    def do_PUT(self):
        try:
            json = self.receive_json()

            if self.path.startswith('/v1/items/'):
                id = self.path[10:]
                item = translate.to_item(json)
                api.update_item(id, item, self.token())
                self.send_json(translate.from_item(item))

            elif self.path.startswith('/v1/links/'):
                id = self.path[10:]
                link = translate.to_link(json)
                api.update_link(id, link, self.token())
                self.send_json(translate.from_link(link))

            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        except TranslationError as error:
            self.send_error(HTTPStatus.BAD_REQUEST, str(error))
        except NotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
        except NotSavedError as error:
            self.send_error(HTTPStatus.BAD_REQUEST, str(error))
        except NotAuthorisedError:
            self.send_error(HTTPStatus.UNAUTHORIZED)
