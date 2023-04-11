from io import BytesIO
from urllib import response
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    # get parameters from request
    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)
    color = request.args.get('color')
    image_format = request.args.get('format')

    # validate parameters
    if not width or not height or not color or not image_format:
        return jsonify({'error': 'Invalid parameters. Please provide width, height, color, and format.'}), 400
    if color not in ['red', 'green', 'blue']:
        return jsonify({'error': 'Invalid color. Please choose one of red, green, or blue.'}), 400
    if image_format not in ['jpeg', 'png', 'gif']:
        return jsonify({'error': 'Invalid format. Please choose one of jpeg, png, or gif.'}), 400

    # generate image array
    color_map = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color_map[color]

    # create PIL image
    pil_image = Image.fromarray(image)

    # convert image to bytes
    with BytesIO() as buffer:
        pil_image.save(buffer, format=image_format)
        image_bytes = buffer.getvalue()

    # return image as response
    return response(image_bytes, mimetype=f'image/{image_format}')

if __name__ =="__main__":
    app.run(debug=True)
