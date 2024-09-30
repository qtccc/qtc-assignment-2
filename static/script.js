let data = [];
let centroids = [];
let labels = [];
let selectedCentroids = [];
let isManualMode = false;

// Generate random dataset
function generateData() {
    const numPoints = 300;
    fetch('/generate_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num_points: numPoints })
    })
        .then(response => response.json())
        .then(responseData => {
            data = responseData;
            visualizeData();
        })
        .catch(error => console.error('Error:', error));
}

// Run KMeans to convergence
function runKMeans() {
    const numClusters = document.getElementById('num_clusters').value;
    const initMethod = document.getElementById('init_method').value;

    if (initMethod === 'manual') {
        isManualMode = true;
        selectedCentroids = [];
        alert(`Please select ${numClusters} centroids by clicking on the plot.`);
        return;
    }

    fetch('/cluster', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            data: data,
            n_clusters: numClusters,
            init_method: initMethod,
            centroids: selectedCentroids
        })
    })
        .then(response => response.json())
        .then(result => {
            centroids = result.centroids;
            labels = result.labels;
            visualizeClusters();
        })
        .catch(error => console.error('Error:', error));
}

// Step through KMeans one iteration at a time
function stepThroughKMeans() {
    const numClusters = parseInt(document.getElementById('num_clusters').value);  // Ensure input is converted to an integer
    const initMethod = document.getElementById('init_method').value;

    fetch('/step_kmeans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            data: data,
            n_clusters: numClusters,  // Pass the user's cluster input correctly
            init_method: initMethod
        })
    })
    .then(response => response.json())
    .then(result => {
        centroids = result.centroids;
        labels = result.labels;
        visualizeClusters();  // Update the plot after every step

        if (result.converged) {
            alert('KMeans has converged.');
        }
    })
    .catch(error => console.error('Error:', error));
}



// Reset the algorithm without changing the dataset
function resetAlgorithm() {
    // Clear centroids, labels, and selected centroids but keep the dataset
    centroids = [];
    labels = [];
    selectedCentroids = [];
    isManualMode = false;  // Reset manual mode

    // Re-visualize the dataset without centroids and labels
    visualizeData();  // Call the function that only displays the dataset without clusters

    // Optionally: Reset the form inputs (like number of clusters and init method) if needed
    document.getElementById('num_clusters').value = 3;  // Reset to default number of clusters
    document.getElementById('init_method').selectedIndex = 0;  // Reset to 'Random' method (or keep current)

}


// Visualize the raw data points
function visualizeData() {
    const trace = {
        x: data.map(point => point[0]),
        y: data.map(point => point[1]),
        mode: 'markers',
        marker: { size: 5, color: 'gray' }
    };

    const layout = {
        title: 'Dataset',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };

    Plotly.newPlot('plot', [trace], layout);
}

// Visualize clusters and centroids
function visualizeClusters() {
    const colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow'];

    const traceData = data.map((point, i) => ({
        x: [point[0]],
        y: [point[1]],
        mode: 'markers',
        marker: { color: colors[labels[i] % colors.length], size: 5 }
    }));

    const traceCentroids = centroids.map((centroid, i) => ({
        x: [centroid[0]],
        y: [centroid[1]],
        mode: 'markers',
        marker: { color: colors[i % colors.length], size: 15, symbol: 'x' },
        name: 'Centroid'
    }));

    const layout = {
        title: 'KMeans Clustering Visualization',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };

    Plotly.newPlot('plot', [...traceData, ...traceCentroids], layout);
}
