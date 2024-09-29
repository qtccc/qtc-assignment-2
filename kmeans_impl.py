import numpy as np
import random

class KMeans:
    def __init__(self, n_clusters=3, init_method='random', max_iters=300, tol=1e-4):
        self.n_clusters = n_clusters
        self.init_method = init_method
        self.max_iters = max_iters
        self.tol = tol  # Tolerance for centroid movement
        self.centroids = None
        self.current_iter = 0  # Track the current iteration for step-through

    def fit(self, data):
        # Step 1: Initialize centroids
        self.centroids = self._initialize_centroids(data)
        
        for i in range(self.max_iters):
            # Step 2: Assign clusters
            labels = self._assign_clusters(data)

            # Step 3: Update centroids
            new_centroids = self._compute_centroids(data, labels)

            # Check for convergence (if centroids do not change significantly)
            if np.linalg.norm(new_centroids - self.centroids) < self.tol:
                print(f"Converged in {i} iterations.")
                break
            
            self.centroids = new_centroids
        
        return labels
    def step(self, data):
        if self.current_iter == 0:
            self.centroids = self._initialize_centroids(data)

        # Step through one iteration of assignment and updating centroids
        labels = self._assign_clusters(data)
        new_centroids = self._compute_centroids(data, labels)

        # Check if we've converged
        if np.linalg.norm(new_centroids - self.centroids) < self.tol or self.current_iter >= self.max_iters:
            print(f"Converged after {self.current_iter} iterations.")
            return labels, True  # Indicate convergence

        # Update centroids and increment the iteration counter
        self.centroids = new_centroids
        self.current_iter += 1

        return labels, False  # Indicate that there are more iterations to run
    
    def _initialize_centroids(self, data):
        if self.init_method == 'random':
            return self._random_initialization(data)
        elif self.init_method == 'farthest_first':
            return self._farthest_first_initialization(data)
        elif self.init_method == 'kmeans++':
            return self._kmeans_plus_plus_initialization(data)
        else:
            raise ValueError(f"Unknown initialization method: {self.init_method}")

    def _random_initialization(self, data):
        # Randomly select n_clusters data points as initial centroids
        indices = random.sample(range(data.shape[0]), self.n_clusters)
        return data[indices]

    def _farthest_first_initialization(self, data):
        centroids = []
        # Start by selecting a random point as the first centroid
        first_centroid_idx = random.randint(0, data.shape[0] - 1)
        centroids.append(data[first_centroid_idx])
        
        # Now, select the remaining centroids by choosing the point farthest from existing centroids
        for _ in range(1, self.n_clusters):
            dists = np.array([min([np.linalg.norm(point - c) for c in centroids]) for point in data])
            farthest_idx = np.argmax(dists)
            centroids.append(data[farthest_idx])
        
        return np.array(centroids)

    def _kmeans_plus_plus_initialization(self, data):
        centroids = []
        # Step 1: Choose the first centroid randomly from data points
        first_centroid_idx = random.randint(0, data.shape[0] - 1)
        centroids.append(data[first_centroid_idx])
        
        # Step 2: Choose subsequent centroids with probability proportional to the squared distance
        for _ in range(1, self.n_clusters):
            dists = np.array([min([np.linalg.norm(point - c) ** 2 for c in centroids]) for point in data])
            probabilities = dists / dists.sum()
            next_centroid_idx = np.random.choice(range(data.shape[0]), p=probabilities)
            centroids.append(data[next_centroid_idx])
        
        return np.array(centroids)

    def _assign_clusters(self, data):
        # Assign each point to the nearest centroid
        labels = np.zeros(data.shape[0])
        for i, point in enumerate(data):
            dists = np.linalg.norm(point - self.centroids, axis=1)
            labels[i] = np.argmin(dists)
        return labels

    def _compute_centroids(self, data, labels):
        # Recompute centroids as the mean of all points assigned to the cluster
        new_centroids = np.zeros((self.n_clusters, data.shape[1]))
        for k in range(self.n_clusters):
            points_in_cluster = data[labels == k]
            if len(points_in_cluster) > 0:
                new_centroids[k] = np.mean(points_in_cluster, axis=0)
        return new_centroids

# Example usage:
if __name__ == "__main__":
    # Create some dummy data (2D for visualization)
    data = np.random.rand(100, 2) * 10
    
    # Initialize KMeans object
    kmeans = KMeans(n_clusters=3, init_method='kmeans++')

    # Fit the model
    labels = kmeans.fit(data)

    # Output the centroids and labels
    print("Centroids:\n", kmeans.centroids)
    print("Labels:\n", labels)
