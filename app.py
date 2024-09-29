from flask import Flask, request, jsonify
from KMeans import KMeans  # Import your KMeans class from the previous section
import numpy as np
import pandas as pd
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for interaction with front-end

@app.route('/cluster', methods=['POST'])
def cluster():
    # Get the JSON request data
    request_data = request.get_json()

    # Extract the dataset and other options from the request
    data = np.array(request_data['data'])
    n_clusters = int(request_data['n_clusters'])
    init_method = request_data['init_method']
    max_iters = int(request_data.get('max_iters', 300))

    # Initialize the KMeans object with the provided initialization method
    kmeans = KMeans(n_clusters=n_clusters, init_method=init_method, max_iters=max_iters)
    
    # Run KMeans algorithm
    labels = kmeans.fit(data)
    
    # Prepare the response with centroids and labels
    response = {
        'centroids': kmeans.centroids.tolist(),
        'labels': labels.tolist()
    }

    # Send back the clustered data
    return jsonify(response)

# Route to generate a random dataset
@app.route('/generate_data', methods=['POST'])
def generate_data():
    # Generate random data points between -10 and 10 (2D data for visualization)
    num_points = int(request.json['num_points'])
    data = np.random.uniform(-10, 10, (num_points, 2))
    
    # Return the data as a list of lists (JSON format)
    return jsonify(data.tolist())



# Route to step through the KMeans algorithm
@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    request_data = request.get_json()

    # Extract dataset and KMeans params from the request
    data = np.array(request_data['data'])
    n_clusters = int(request_data['n_clusters'])
    init_method = request_data['init_method']

    # Initialize the KMeans object (or reuse if already created)
    if 'kmeans' not in globals():
        global kmeans
        kmeans = KMeans(n_clusters=n_clusters, init_method=init_method)
    
    # Perform one step of KMeans
    labels, is_converged = kmeans.step(data)

    # Prepare the response with current centroids and labels
    response = {
        'centroids': kmeans.centroids.tolist(),
        'labels': labels.tolist(),
        'converged': is_converged
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
