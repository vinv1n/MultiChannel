from flask import render_template
from flask_json_schema import JsonValidationError


def json_validation_error(error):
    return render_template("validation_error.html", error=error), JsonValidationError