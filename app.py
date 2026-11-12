from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, session
from flask_smorest import Api
from flask_babel import Babel, get_locale
from flask_babel_js import BabelJS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
app.config["BABEL_DEFAULT_LOCALE"] = "pt_BR"
app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"
app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"

SUPPORTED_LOCALES = ("pt_BR", "en")
app.config["SUPPORTED_LOCALES"] = SUPPORTED_LOCALES


def select_locale():
	selected_locale = session.get("language")
	if selected_locale in SUPPORTED_LOCALES:
		return selected_locale

	return request.accept_languages.best_match(SUPPORTED_LOCALES) or "pt_BR"


babel = Babel()
babel.init_app(app, locale_selector=select_locale)
babel_js = BabelJS(app)


@app.context_processor
def inject_locale():
	return {"get_locale": get_locale}

# Configurações do OpenAPI / Swagger UI para o Flask-smorest
app.config["API_TITLE"] = "API de Itens"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"



db = SQLAlchemy(app)

api = Api(app)
# Registro do Blueprint de API
from .api_routes import blp as items_blueprint
api.register_blueprint(items_blueprint)


from . import route
