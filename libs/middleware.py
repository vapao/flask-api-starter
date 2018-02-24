from libs import json_response
from public import app as raw_app


def init_app(app):
    app.register_error_handler(Exception, exception_handler)
    app.register_error_handler(404, page_not_found)


def page_not_found(_):
    return json_response(message='Resource not found')


def exception_handler(ex):
    raw_app.logger.exception(ex)
    message = '%s' % ex
    if len(message) > 60:
        message = message[:60] + '...'
    return json_response(message=message)
