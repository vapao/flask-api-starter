from . import views


def register_blueprint(app):
    app.register_blueprint(views.blueprint, url_prefix='/blogs')
