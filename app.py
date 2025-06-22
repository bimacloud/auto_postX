# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Contoh data video
VIDEO_DATA = {
    "nature": [
        {"id": "nature1", "title": "Sunset in Bali", "poster_url": "https://res.cloudinary.com/dk2lzbpm5/image/upload/v1750511635/cld-sample-4.jpg"},
        {"id": "nature2", "title": "Forest Walk", "poster_url": "https://res.cloudinary.com/demo/image/upload/sample.jpg"}
    ],
    "technology": [
        {"id": "tech1", "title": "AI Robot Demo", "poster_url": "https://res.cloudinary.com/demo/image/upload/v1618302171/robot.jpg"}
    ]
}

@app.route('/')
def index():
    categories = VIDEO_DATA.keys()
    return render_template("index.html", categories=categories)

@app.route('/videos/<category>')
def videos(category):
    vids = VIDEO_DATA.get(category, [])
    return render_template("videos.html", category=category, videos=vids)

@app.route('/download/<category>/<video_id>')
def download(category, video_id):
    video = next((v for v in VIDEO_DATA.get(category, []) if v['id'] == video_id), None)
    if not video:
        return "Video not found", 404

    # Download image
    image_url = video['poster_url']
    img_data = requests.get(image_url).content
    filename = f"{video_id}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(img_data)

    return redirect(url_for('preview', video_id=video_id))

@app.route('/preview/<video_id>')
def preview(video_id):
    # Cari video dari semua kategori
    video = None
    for vids in VIDEO_DATA.values():
        for v in vids:
            if v['id'] == video_id:
                video = v
                break
    if not video:
        return "Preview not found", 404

    data = {
        "title": video['title'],
        "description": f"Preview of {video['title']}",
        "image_url": url_for('static', filename=f"uploads/{video_id}.jpg", _external=True)
    }
    return render_template("preview.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
