from flask import Blueprint

from libs import json_response, JsonParser, Argument
from .model import Blog

blueprint = Blueprint(__name__, __name__)


@blueprint.route('/', methods=['GET'])
def get():
    return json_response(Blog.query.all())


@blueprint.route('/', methods=['POST'])
def post():
    form, error = JsonParser(
        Argument('title', help='Please enter the title'),
        Argument('count', type=int, filter=lambda x: x >= 0, help='Please enter the count')
    ).parse()
    if error is None:
        Blog(**form).save()
    return json_response(message=error)
