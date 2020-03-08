import http.server
from http import HTTPStatus

from thelca.api import API
api = API('1.0.0')

from thelca.error import NotAuthorisedError, NotFoundError, NotSavedError

from thelca.translator import JSON, TranslationError
translate = JSON()

class Handler(http.server.BaseHTTPRequestHandler):
    '''The Electric Cat - REST API

    All endpoints other than "/" require a valid Authorization header.

    You can find a full list of endpoints at /help

    Meeeow!
    '''
    server_version = 'TheElectricCat/0'
    sys_version = 'X'
    counters = {
        HTTPStatus.OK: 0,
        HTTPStatus.NOT_FOUND: 0,
        HTTPStatus.BAD_REQUEST: 0,
        HTTPStatus.UNAUTHORIZED: 0
    }

    def help(self):
        return 'The Electric Cat\n\n' + \
            'All endpoints require a valid Authorization header.\n\n' + \
            self.doc(self.do_GET.__doc__) + '\n' + \
            self.doc(self.do_POST.__doc__) + '\n' + \
            self.doc(self.do_PUT.__doc__) + '\n' + \
            self.doc(self.do_DELETE.__doc__)

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
        self.counters[HTTPStatus.OK] += 1

    def send_error(self, code, message=None):
        super().send_error(code, message)
        self.counters[code] += 1

    def send_json(self, json):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.encode('utf-8'))
        self.counters[HTTPStatus.OK] += 1

    def receive_json(self):
        content_length = self.headers['Content-Length']
        length = int(content_length) if content_length else 0
        posted_bytes = self.rfile.read(length)
        if len(posted_bytes) == length:
            return posted_bytes.decode('utf-8')
        else:
            return "{}"

    def do_DELETE(self):
        '''DELETE

        /v1/links/{link identifier}
        '''
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
        '''GET

        /help
        /health
        /metrics

        /v1/items/{item identifier}
        /v1/items?{query string}

        /v1/links/{link identifier}
        /v1/links?{query string}
        '''
        try:
            if self.path == '/':
                self.send_text(self.doc(Handler.__doc__))

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

            elif self.path == '/help':
                api.read_service('help', self.token())
                self.send_text(self.help())

            elif self.path == '/health':
                api.read_service('health', self.token())
                self.send_text('UP\n')

            elif self.path == '/metrics':
                api.read_service('metrics', self.token())
                self.send_text(self.metrics())

            else:
                self.send_error(HTTPStatus.NOT_FOUND)

        except NotFoundError:
            self.send_error(HTTPStatus.NOT_FOUND)
        except NotAuthorisedError:
            self.send_error(HTTPStatus.UNAUTHORIZED)

    def do_POST(self):
        '''POST

        /v1/items
        /v1/links
        '''
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
        '''PUT

        /v1/items/{item identifier}
        /v1/links/{link identifier}
        '''
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

    def doc(self, docstring):
        lines = docstring.split('\n')
        stripped = [line.strip() for line in lines]
        return '\n'.join(stripped)

    @staticmethod
    def count(code, value):
        return 'http_responses{{code="{0}"}} {1}'.format(str(int(code)), str(value))

    def metrics(self):
        help = '# HELP http_responses The total number of HTTP responses.\n'
        type = '# TYPE http_responses counter\n'

        lines = [self.count(key, value) for key, value in self.counters.items()]
        return help + type + '\n'.join(lines) + '\n'
