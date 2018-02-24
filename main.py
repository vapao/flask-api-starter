from public import app
from libs import middleware

from apps import blog

# Load middleware
middleware.init_app(app)

# Registry blueprint
blog.register_blueprint(app)

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG'))
