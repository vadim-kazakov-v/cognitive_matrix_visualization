from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.linalg import eigvals
from sklearn.manifold import TSNE
import random
import itertools
import json

app = Flask(__name__)

def check_constraints(matrix, constraints):
    """Check if a matrix satisfies all constraints"""
    for constraint in constraints:
        cells = constraint['cells']
        constraint_type = constraint['type']
        value = constraint['value']
        
        # Calculate sum of specified cells
        cell_sum = sum(matrix[int(cell.split(',')[0])][int(cell.split(',')[1])] for cell in cells)
        
        # Check constraint based on type
        if constraint_type == 'sum_greater' and cell_sum < value:
            return False
        elif constraint_type == 'sum_less' and cell_sum > value:
            return False
        elif constraint_type == 'sum_equal' and abs(cell_sum - value) > 1e-6:
            return False
    
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_matrices():
    try:
        data = request.json
        size = data['size']
        num_matrices = data['num_matrices']
        dimensionality = data['dimensionality']
        cell_ranges = data['cell_ranges']
        constraints = data['constraints']
        
        # Generate matrices based on cell ranges and constraints
        valid_matrices = []
        eigenvalues_list = []
        
        attempts = 0
        max_attempts = num_matrices * 10  # Limit attempts to prevent infinite loop
        
        while len(valid_matrices) < num_matrices and attempts < max_attempts:
            # Create a new matrix
            matrix = np.zeros((size, size))
            
            # Fill each cell with a random value within its range
            for i in range(size):
                for j in range(size):
                    cell_range = cell_ranges[f"{i},{j}"]
                    min_val = cell_range['min']
                    max_val = cell_range['max']
                    step = cell_range['step']
                    
                    # Calculate possible values
                    values = np.arange(min_val, max_val + step/2, step)
                    if len(values) == 0:
                        # If no values in range, use the min value
                        matrix[i][j] = min_val
                    else:
                        matrix[i][j] = random.choice(values)
            
            # Check if matrix satisfies all constraints
            if check_constraints(matrix, constraints):
                valid_matrices.append(matrix)
                
                # Calculate eigenvalues
                eigenvalues = eigvals(matrix)
                # Extract real parts of eigenvalues
                real_eigenvalues = np.real(eigenvalues).tolist()
                eigenvalues_list.append(real_eigenvalues)
            
            attempts += 1
        
        if len(valid_matrices) < num_matrices:
            return jsonify({'error': f'Could only generate {len(valid_matrices)} out of {num_matrices} requested matrices. Try adjusting constraints or ranges.'}), 400
        
        # Prepare data for dimensionality reduction
        # Flatten eigenvalues to create feature vectors
        eigenvalue_vectors = []
        for ev_list in eigenvalues_list:
            # Pad or truncate eigenvalue lists to fixed size for consistent features
            vector = np.zeros(size * 2)  # Real and imaginary parts for max possible eigenvalues
            for idx, ev in enumerate(ev_list):
                if idx < size * 2:
                    vector[idx] = ev
            eigenvalue_vectors.append(vector)
        
        eigenvalue_vectors = np.array(eigenvalue_vectors)
        
        # Apply t-SNE for dimensionality reduction
        tsne = TSNE(n_components=dimensionality, random_state=42, perplexity=min(30, len(valid_matrices)-1))
        coords = tsne.fit_transform(eigenvalue_vectors)
        
        # Convert to list for JSON serialization
        coords_list = coords.tolist()
        
        return jsonify({
            'coordinates': coords_list,
            'eigenvalues': eigenvalues_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)