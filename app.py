import os
import json
import gpxpy
import gpxpy.gpx
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['UPLOAD_EXTENSIONS'] = ['.gpx', '.kml', '.kmz']

# Mock Data for Past Trips
TRIPS = [
    {
        'id': '1',
        'name': 'Monte Rosa Massif',
        'date': 'Aug 2025',
        'location': 'Italy/Switzerland',
        'elevation': '4,634m',
        'image': 'https://picsum.photos/seed/monterosa/800/600',
        'description': 'A multi-day traverse across the second highest massif in the Alps. Challenging glacier travel and high altitude camps.',
        'stats': {'duration': '3 Days', 'distance': '24km', 'gain': '2100m'}
    },
    {
        'id': '2',
        'name': 'Gran Paradiso',
        'date': 'Jul 2025',
        'location': 'Aosta Valley',
        'elevation': '4,061m',
        'image': 'https://picsum.photos/seed/granparadiso/800/600',
        'description': 'The only 4000m peak entirely within Italy. A classic snow climb with a rocky summit block.',
        'stats': {'duration': '2 Days', 'distance': '16km', 'gain': '1800m'}
    },
    {
        'id': '3',
        'name': 'Weissmies Traverse',
        'date': 'Jun 2025',
        'location': 'Saas-Fee',
        'elevation': '4,017m',
        'image': 'https://picsum.photos/seed/weissmies/800/600',
        'description': 'A beautiful traverse ascending the SE ridge and descending the normal route. Spectacular views of the Mischabel group.',
        'stats': {'duration': '1 Day', 'distance': '12km', 'gain': '1100m'}
    },
    {
        'id': '4',
        'name': 'Dom des Mischabel',
        'date': 'Sep 2024',
        'location': 'Randa',
        'elevation': '4,545m',
        'image': 'https://picsum.photos/seed/dom/800/600',
        'description': 'The highest mountain entirely in Switzerland. A long, demanding ascent requiring excellent fitness.',
        'stats': {'duration': '2 Days', 'distance': '28km', 'gain': '3100m'}
    },
    {
        'id': '5',
        'name': 'Piz Bernina',
        'date': 'Aug 2024',
        'location': 'Engadin',
        'elevation': '4,049m',
        'image': 'https://picsum.photos/seed/bernina/800/600',
        'description': 'The most easterly 4000er in the Alps. Famous for the Biancograt, a stunning white ridge.',
        'stats': {'duration': '3 Days', 'distance': '22km', 'gain': '2400m'}
    },
    {
        'id': '6',
        'name': 'Dent Blanche',
        'date': 'Jul 2024',
        'location': 'Val d\'Hérens',
        'elevation': '4,357m',
        'image': 'https://picsum.photos/seed/dentblanche/800/600',
        'description': 'A perfect pyramid of rock and ice. One of the most difficult 4000m peaks in the Alps.',
        'stats': {'duration': '2 Days', 'distance': '18km', 'gain': '1900m'}
    },
]

@app.route('/')
def index():
    return render_template('index.html', trips=TRIPS)

@app.route('/api/parse-gpx', methods=['POST'])
def parse_gpx():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        try:
            # Parse GPX
            gpx = gpxpy.parse(file)
            
            track_points = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        track_points.append([point.latitude, point.longitude])
            
            # Simple metadata extraction
            return jsonify({
                'track': track_points,
                'name': gpx.tracks[0].name if gpx.tracks else 'Uploaded Track',
                'description': gpx.tracks[0].description if gpx.tracks else ''
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
