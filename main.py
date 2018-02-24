from public import app
from libs import middleware

from apps import blog

# Load middleware
middleware.init_app(app)

# Registry blueprint
blog.register_blueprint(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=app.config.get('DEBUG'))
