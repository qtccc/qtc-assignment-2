let data = [];
let centroids = [];
let labels = [];
let selectedCentroids = [];
let isManualMode = false;


function generateData() {
    // Generate random dataset
    const numPoints = 300;
    fetch('/generate_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ num_points: numPoints })
    })
    .then(response => response.json())
    .then(responseData => {
        data = responseData;
        visualizeData();
    })
    .catch(error => console.error('Error:', error));
}

function runKMeans() {
    const numClusters = document.getElementById('num_clusters').value;
    const initMethod = document.getElementById('init_method').value;

    // Check if the user selected manual initialization
    if (initMethod === 'manual') {
        isManualMode = true;
        selectedCentroids = [];
        alert(`Please select ${numClusters} centroids by clicking on the plot.`);
        return;
    } else {
        isManualMode = false;
    }

    // Send data and clustering options to the server
    fetch('/cluster', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: data,
            n_clusters: numClusters,
            init_method: initMethod
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


// Capture plot clicks for manual initialization
document.getElementById('plot').on('plotly_click', function(eventData) {
    if (isManualMode) {
        const numClusters = document.getElementById('num_clusters').value;

        // Extract the clicked point's x and y coordinates
        const x = eventData.points[0].x;
        const y = eventData.points[0].y;

        // Add the clicked point to the selected centroids list
        selectedCentroids.push([x, y]);

        // Plot the selected centroids so far
        visualizeSelectedCentroids();

        // Check if enough centroids have been selected
        if (selectedCentroids.length == numClusters) {
            isManualMode = false;
            alert('Centroids selected. Running KMeans...');
            runKMeans();  // Proceed to run KMeans with the selected centroids
        }
    }
});

function visualizeSelectedCentroids() {
    // Visualize the selected centroids on the plot
    const traceCentroids = {
        x: selectedCentroids.map(c => c[0]),
        y: selectedCentroids.map(c => c[1]),
        mode: 'markers',
        marker: { color: 'red', size: 15, symbol: 'x' },
        name: 'Selected Centroids'
    };

    Plotly.addTraces('plot', [traceCentroids]);
}

function stepThroughKMeans() {
    const numClusters = document.getElementById('num_clusters').value;
    const initMethod = document.getElementById('init_method').value;

    // Send data and clustering options to the server for one step
    fetch('/step_kmeans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: data,
            n_clusters: numClusters,
            init_method: initMethod
        })
    })
    .then(response => response.json())
    .then(result => {
        centroids = result.centroids;
        labels = result.labels;
        visualizeClusters();

        // If converged, show a message
        if (result.converged) {
            alert('KMeans has converged.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function resetAlgorithm() {
    data = [];
    centroids = [];
    labels = [];
    Plotly.purge('plot');
}

function visualizeData() {
    // Visualize the raw data without clustering
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

function visualizeClusters() {
    // Visualize the clustered data and centroids
    const colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow'];
    
    const traceData = data.map((point, i) => {
        return {
            x: [point[0]],
            y: [point[1]],
            mode: 'markers',
            marker: { color: colors[labels[i] % colors.length], size: 5 }
        };
    });

    const traceCentroids = centroids.map((centroid, i) => {
        return {
            x: [centroid[0]],
            y: [centroid[1]],
            mode: 'markers',
            marker: { color: colors[i % colors.length], size: 15, symbol: 'x' },
            name: 'Centroid'
        };
    });

    const layout = {
        title: 'KMeans Clustering Visualization',
        xaxis: { title: 'X' },
        yaxis: { title: 'Y' }
    };

    Plotly.newPlot('plot', [...traceData, ...traceCentroids], layout);
}
