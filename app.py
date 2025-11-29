from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.linalg import eigvals
from sklearn.manifold import TSNE
import random
import itertools
import json
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_constraints(matrix, constraints):
    """Check if a matrix satisfies all constraints"""
    logger.info(f"Checking constraints for matrix of size {matrix.shape}")
    for i, constraint in enumerate(constraints):
        cells = constraint['cells']
        constraint_type = constraint['type']
        value = constraint['value']
        
        # Calculate sum of specified cells
        cell_sum = sum(matrix[int(cell.split(',')[0])][int(cell.split(',')[1])] for cell in cells)
        
        logger.debug(f"Constraint {i}: type={constraint_type}, cells={cells}, value={value}, sum={cell_sum}")
        
        # Check constraint based on type
        if constraint_type == 'sum_greater' and cell_sum < value:
            logger.debug(f"Constraint {i} failed: sum {cell_sum} < {value}")
            return False
        elif constraint_type == 'sum_less' and cell_sum > value:
            logger.debug(f"Constraint {i} failed: sum {cell_sum} > {value}")
            return False
        elif constraint_type == 'sum_equal' and abs(cell_sum - value) > 1e-6:
            logger.debug(f"Constraint {i} failed: sum {cell_sum} != {value}")
            return False
    
    logger.info("All constraints satisfied")
    return True

@app.route('/')
def index():
    return render_template('index.html')

def calculate_max_matrices(size, cell_ranges):
    """Calculate the maximum possible number of matrices based on cell ranges"""
    total_combinations = 1
    
    for i in range(size):
        for j in range(size):
            cell_range = cell_ranges[f"{i},{j}"]
            min_val = cell_range['min']
            max_val = cell_range['max']
            step = cell_range['step']
            
            # Calculate possible values for this cell
            if step <= 0:
                step = 1  # Default to 1 if step is invalid
            values = len([x for x in np.arange(min_val, max_val + step/2, step)])
            if values == 0:
                # If no values in range, just use 1 possibility
                values = 1
            total_combinations *= values
            
            # Limit to prevent extremely large numbers
            if total_combinations > 10**10:  # 10 billion max
                return 10**6  # Return 1 million as a reasonable max
    
    # If total combinations is too large, return a reasonable maximum
    if total_combinations > 10**6:
        return 10**6
    return total_combinations

@app.route('/calculate_max_matrices', methods=['POST'])
def calculate_max_matrices_endpoint():
    try:
        data = request.json
        size = data['size']
        cell_ranges = data['cell_ranges']
        constraints = data.get('constraints', [])
        
        max_possible = calculate_max_matrices(size, cell_ranges)
        
        # Apply additional constraints to reduce the maximum
        # This is a simplified calculation - in a real implementation, 
        # we would need to account for constraint restrictions
        # For now, we'll just return the raw maximum from cell ranges
        # since calculating the exact maximum with constraints is complex
        
        return jsonify({
            'max_possible': max_possible
        })
    except Exception as e:
        logger.error(f"Error in calculate_max_matrices: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_matrices():
    try:
        data = request.json
        size = data['size']
        num_matrices = data['num_matrices']
        dimensionality = data['dimensionality']
        cell_ranges = data['cell_ranges']
        constraints = data['constraints']
        eigenvector_selection = data.get('eigenvector_selection', 'all')  # Default to 'all'
        
        # Validate that num_matrices doesn't exceed maximum possible
        max_possible = calculate_max_matrices(size, cell_ranges)
        if num_matrices > max_possible:
            error_msg = f'Requested {num_matrices} matrices but maximum possible with current ranges is {max_possible}. Please reduce the number of matrices or expand cell ranges.'
            logger.warning(error_msg)
            return jsonify({'error': error_msg}), 400
        
        logger.info(f"Generating {num_matrices} matrices of size {size}x{size} with {len(constraints)} constraints, eigenvector selection: {eigenvector_selection}")
        
        # Generate matrices based on cell ranges and constraints
        valid_matrices = []
        eigenvalues_list = []
        eigenvectors_list = []
        
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
                valid_matrices.append(matrix.copy())  # Store a copy of the matrix
                
                # Calculate eigenvalues and eigenvectors
                eigenvalues = eigvals(matrix)
                # Extract real parts of eigenvalues and handle complex numbers
                processed_eigenvalues = []
                for ev in eigenvalues:
                    if isinstance(ev, complex):
                        if ev.imag == 0:
                            processed_eigenvalues.append(float(ev.real))
                        else:
                            processed_eigenvalues.append({'real': float(ev.real), 'imag': float(ev.imag)})
                    else:
                        processed_eigenvalues.append(float(ev))
                eigenvalues_list.append(processed_eigenvalues)
                
                # Calculate eigenvectors
                eigenvals, eigenvecs = np.linalg.eig(matrix)
                # Convert eigenvectors to lists for JSON serialization and handle complex numbers
                processed_eigenvectors = []
                for col in eigenvecs.T:  # Transpose to get column vectors
                    processed_col = []
                    for component in col:
                        if isinstance(component, complex):
                            if component.imag == 0:
                                processed_col.append(float(component.real))
                            else:
                                processed_col.append({'real': float(component.real), 'imag': float(component.imag)})
                        else:
                            processed_col.append(float(component))
                    processed_eigenvectors.append(processed_col)
                eigenvectors_list.append(processed_eigenvectors)
            
            attempts += 1
        
        logger.info(f"Generated {len(valid_matrices)} valid matrices out of {attempts} attempts")
        
        if len(valid_matrices) < num_matrices:
            error_msg = f'Could only generate {len(valid_matrices)} out of {num_matrices} requested matrices. Try adjusting constraints or ranges.'
            logger.warning(error_msg)
            return jsonify({'error': error_msg}), 400
        
        # Prepare data for dimensionality reduction
        # Flatten eigenvalues to create feature vectors
        eigenvalue_vectors = []
        for ev_list in eigenvalues_list:
            # Pad or truncate eigenvalue lists to fixed size for consistent features
            vector = np.zeros(size * 2)  # Real and imaginary parts for max possible eigenvalues
            for idx, ev in enumerate(ev_list):
                if idx < size * 2:
                    if isinstance(ev, dict):  # Complex number represented as dict
                        vector[idx] = ev['real']  # Use real part for t-SNE
                    else:
                        vector[idx] = ev
            eigenvalue_vectors.append(vector)
        
        eigenvalue_vectors = np.array(eigenvalue_vectors)
        
        # Apply t-SNE for dimensionality reduction
        if len(valid_matrices) == 1:
            # If there's only one matrix, create coordinates manually
            coords = np.array([[0] * dimensionality])  # Single point at origin
        else:
            perplexity_val = min(30, max(1, len(valid_matrices)-1))  # Ensure perplexity is at least 1 and less than n_samples
            tsne = TSNE(n_components=dimensionality, random_state=42, perplexity=perplexity_val)
            coords = tsne.fit_transform(eigenvalue_vectors)
        
        # Convert to list for JSON serialization
        coords_list = coords.tolist()
        
        # Convert matrices to lists for JSON serialization
        matrices_list = [matrix.tolist() for matrix in valid_matrices]
        
        logger.info("Successfully completed matrix generation and visualization processing")
        
        return jsonify({
            'coordinates': coords_list,
            'eigenvalues': eigenvalues_list,
            'matrices': matrices_list,  # Include the original matrices
            'eigenvectors': eigenvectors_list  # Include the eigenvectors
        })
    except Exception as e:
        logger.error(f"Error in generate_matrices: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)