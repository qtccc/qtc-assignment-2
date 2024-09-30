from flask import Flask, render_template, request, jsonify
from KMeans import KMeans  # Import your KMeans class from the previous section
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for interaction with front-end

# Declare kmeans globally
kmeans = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cluster', methods=['POST'])
def cluster():
    global kmeans  # Ensure kmeans is accessible
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

    return jsonify(response)

# Route to generate a random dataset
@app.route('/generate_data', methods=['POST'])
def generate_data():
    num_points = int(request.json['num_points'])
    data = np.random.uniform(-10, 10, (num_points, 2))
    
    return jsonify(data.tolist())

# Route to step through the KMeans algorithm
@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    global kmeans  # Declare the global variable
    
    request_data = request.get_json()
    data = np.array(request_data['data'])
    n_clusters = int(request_data['n_clusters'])
    init_method = request_data['init_method']

    # Initialize or reinitialize KMeans if necessary
    if kmeans is None or kmeans.n_clusters != n_clusters:
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
    app.run(debug=True, port=3000)
