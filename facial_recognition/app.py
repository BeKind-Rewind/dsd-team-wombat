from deepface import DeepFace

from flask import (Flask,
                   request,
                   Response,
                   make_response,
                   jsonify)

from werkzeug.exceptions import BadRequest, UnsupportedMediaType

from facial_verification import (handle_deepface_response,
                                 validate_request_body,
                                 handle_encoded_images)

from helpers import send_error_response
from image_handler import get_image_url_for_base64 as get_image_path

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Team Wombat - Facial Recognition Service :) </p>"


# Required json body (with content type - "application/json")
# {
#   "captured": "base64_encoded string of captured image",
#   "reference": "base64_encoded string image to be compared against"
#   }
@app.route("/verify", methods=['POST'])
def verify_images():
    key = "verified"
    json_response: Response

    # Retrieve json body parameters and validate it
    # Sends 400 Bad Request response if request body is invalid
    try:
        request_body = request.get_json()

        # Validate request body
        error_msg = validate_request_body(request_body)

        # If request body is valid
        if not error_msg:

            # Decode and save the base64 encoded image strings
            decoding_errors = handle_encoded_images(request_body)

            if decoding_errors:
                return send_error_response(decoding_errors, 500)

        else:
            # Denotes Bad Request
            return send_error_response(error_msg, 400)
    except (BadRequest, UnsupportedMediaType) as err:
        print(f"Request Body error: {err}, {type(err)=}")
        return send_error_response(str(err), 400)

    # Invoke Deepface's verify method to compare the
    # images and handle exceptions
    try:

        image1_url = get_image_path(request_body.get("captured"))
        image2_url = get_image_path(request_body.get("reference"))

        result = DeepFace.verify(image1_url, image2_url)
        response = handle_deepface_response(result, key)

        json_response = make_response(jsonify(response))

        if response["data"].keys() == 0:
            json_response.status_code = 500
        else:
            json_response.status_code = 200

        return json_response

    except Exception as err:
        print(f"Unexpected error: {err}, {type(err)=}")

        # Denotes Internal Server Error
        return send_error_response(str(err), 500)
