from flask import Blueprint, jsonify, session
from webargs import fields
from webargs.flaskparser import use_args, parser

from . import db
from .models import User, user_schema

main = Blueprint('main', __name__)

# Error parsing for bad request
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    response = {
        'error': 'Validation Error',
        'msg': err.messages
    }
    return jsonify(response), 400

