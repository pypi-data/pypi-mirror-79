from quart import request
import functools


class EasyRequest:
    """
    A helper class that make request handling easier, especially for beginners.
    All attributes are assessable via the same syntax, while with Flask.request
    or quart.request, you will have slightly different syntax when retrieving
    different request attributes.

    ..hint:
        You only need to await attributes that need calculation, for example
        evaluating the request body, like `.json` or `.form`.

    """

    params = ...
    headers = ...
    __quart_request = ...

    def load(self):
        self.__quart_request = request
        self.params = dict(self.__quart_request.args)
        self.headers = dict(self.__quart_request.headers)
        return self

    def __call__(self, f):
        print("decorating")

        @functools.wraps(f)
        async def decorated_function(*args2, **kwargs2):
            f.__globals__[self.__class__.__name__] = self.__class__().load()
            return await f(*args2, **kwargs2)

        return decorated_function

    @property
    async def form(self):
        return dict(await self.__quart_request.form)

    @property
    async def json(self):
        json = await self.__quart_request.get_json()
        return {} if json is None else json


if __name__ == '__main__':
    from Aeros import WebServer, render_template, jsonify
    from time import strftime

    app = WebServer(__name__, host="0.0.0.0", port=80)  # init backend & web server
    app.template_folder = "./frontend/build/"
    app.static_folder = "./frontend/build/static/"


    @app.route("/")
    async def home():
        return await render_template("index.html")


    @app.route("/time/")
    @EasyRequest()
    async def current_time():
        print("Headers:", EasyRequest.headers)
        print("Params :", EasyRequest.params)
        print("Form   :", await EasyRequest.form)
        print("JSON   :", await EasyRequest.json)
        return jsonify({"timestamp": strftime("%H:%M:%S")})


    app.run_server()  # run web server in this thread (endless mode)
