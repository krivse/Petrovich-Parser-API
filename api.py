from flask import Flask, request, jsonify, Response

from main import calculate_materials
from validate import validation

app = Flask(__name__)


@app.route("/", methods=['POST'])
def make_the_materials_calculations() -> Response:
    """
    Запрос на расчёт материалов по заданному типу помещения.
        "type_room": "Кухня-гостиная",
        "length": "2",
        "width": "3",
        "height": "2"
    """
    validate_data = validation(request.json)
    response = calculate_materials(*validate_data)

    return jsonify(response)
