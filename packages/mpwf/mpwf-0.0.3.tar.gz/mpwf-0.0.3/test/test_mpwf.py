import pytest

from mpwf.api import API
from mpwf.middleware import Middleware


# ROUTES
def test_basic_route_adding(api):
    @api.route("/home")
    def home(request, response):
        response.text = 'Homepage'


def test_route_overlap_throws_exception(api):
    @api.route("/home")
    def home(request, response):
        pass

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(request, response):
            pass


def test_test_client_can_send_requests(api, client):
    response_text = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = response_text

    assert client.get("http://testserver/hey").text == response_text


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
    assert client.get("http://testserver/ashley").text == "hey ashley"


def test_404(client):
    response = client.get("http://testserver/none")
    assert response.status_code == 404
    assert response.text == "Not Found"


# CLASS BASED HANDLERS
def test_class_based_handler_get(api, client):
    response_text = "this is a request"

    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get("http://testserver/book").text == response_text


def test_class_based_handler_post(api, client):
    response_text = "this is a request"

    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post("http://testserver/book").text == response_text


def test_class_based_handler_not_allowed(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            pass

    with pytest.raises(AttributeError):
        client.get("http://testserver/book")


# TEMPLATES
def test_template(api, client):
    title = "THE TITLE"
    name = "THE NAME"

    @api.route("/html")
    def html_handler(request, resp):
        resp.body = api.template("index.html", context={"title": title, "name": name}).encode()

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert title in response.text
    assert name in response.text


# EXCEPTIONS
def test_custom_exception_handler(api, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    api.add_exception_handler(on_exception)

    @api.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get("http://testserver/")

    assert response.text == "AttributeErrorHappened"


# STATIC FILES
def test_not_found_is_returned_for_nonexistent_static_file(client):
    assert client.get(f"http://testserver/static/unexistent.css)").status_code == 404


FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


def _create_static(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset


def test_assets_are_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_static(static_dir)
    api = API(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get(f"http://testserver/static/{FILE_DIR}/{FILE_NAME}")
    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


# MIDDLEWARE
def test_middleware_methods_are_called(api, client):
    process_request_called = False
    process_response_called = False

    class CallMiddlewareMethods(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True

    api.add_middleware(CallMiddlewareMethods)

    @api.route("/")
    def index(req, res):
        res.text = "TEST"

    client.get("http://testserver/")

    assert process_request_called is True
    assert process_response_called is True


# ALLOWED METHODS FOR FUNCTION BASED HANDLERS
def test_allowed_methods_for_func_based_handlers(api, client):
    @api.route("/home", allowed_methods=['post', 'delete'])
    def home(req, resp):
        resp.text = 'TEST'

    with pytest.raises(AttributeError):
        client.get("http://testserver/home")

    assert client.post('http://testserver/home').text == 'TEST'
    assert client.delete('http://testserver/home').text == 'TEST'


def test_no_methods_allowed_allow_all_methods(api, client):
    @api.route("/home")
    def home(req, resp):
        resp.text = 'TEST'

    assert client.post('http://testserver/home').text == 'TEST'
    assert client.delete('http://testserver/home').text == 'TEST'

# CUSTOM RESPONSES CLASSES
def test_json_response_helper(api, client):
    @api.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "TEST"}

    response = client.get("http://testserver/json")
    json_body = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "TEST"


def test_html_response_helper(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.html = api.template("index.html", context={"title": "Best Title", "name": "Best Name"})

    response = client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "Best Title" in response.text
    assert "Best Name" in response.text


def test_text_response_helper(api, client):
    response_text = "Just Plain Text"

    @api.route("/text")
    def text_handler(req, resp):
        resp.text = response_text

    response = client.get("http://testserver/text")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response_text


def test_manually_setting_body(api, client):
    @api.route("/body")
    def text_handler(req, resp):
        resp.body = b"Byte Body"
        resp.content_type = "text/plain"

    response = client.get("http://testserver/body")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"
