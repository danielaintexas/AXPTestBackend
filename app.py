# app.py
import subprocess
import uuid
from flask import Flask, request, jsonify, send_file
import requests
from werkzeug.utils import secure_filename
import os
import ffmpeg
from scipy.spatial import distance


def create_app():
    app = Flask(__name__, static_folder='uploads', static_url_path='/uploads')
    app.config['UPLOAD_FOLDER'] = '/app/uploads/'
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    # Other setup code...
    return app


app = create_app()


@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello"

@app.route('/get_similar', methods=['POST'])
def cosine_similarity():
    data = request.json
    query_vector = data['query_vector']
    vector_text_pairs = data['vectors']

    # Extract embeddings and their corresponding texts
    vectors = [pair['embeddings'] for pair in vector_text_pairs]
    texts = [pair['text'] for pair in vector_text_pairs]

    # Calculate cosine similarity for each vector
    # Return the index of the most similar vector
    most_similar_index = max(range(len(vectors)), key=lambda index: 1 - distance.cosine(query_vector, vectors[index]))

    return jsonify({'most_similar_text': texts[most_similar_index]})
from flask import Flask, request, jsonify
import requests
from moviepy.editor import VideoFileClip

app = Flask(__name__)

@app.route('/get_video_length', methods=['GET'])
def get_video_length():
    # Get the URL of the video file from the request
    video_url = request.args.get('url')

    if not video_url:
        return jsonify({'error': 'Video URL is missing'}), 400

    try:
        # Download the video file
        response = requests.get(video_url)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download video file'}), 500

        # Save the video file
        with open('temp_video.mp4', 'wb') as f:
            f.write(response.content)

        # Get the length of the video
        clip = VideoFileClip('temp_video.mp4')
        duration = clip.duration

        # Cleanup: Remove the temporary video file
        clip.close()
        # You may want to remove the temporary file after using it
        # to avoid filling up your storage with temporary files

        # Return the length of the video
        return jsonify({'length': duration}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

