# Matrix Eigenvalue Visualizer

This web application allows users to define rules for generating square matrices, calculates their eigenvalues, and visualizes the results in 2D or 3D space using t-SNE for dimensionality reduction.

## Features

- Define matrix size (N×N)
- Set individual value ranges for each matrix cell (min, max, step)
- Add custom constraints on groups of cells (sum constraints)
- Generate multiple matrices based on rules
- Calculate eigenvalues for each matrix
- Visualize results using Plotly.js in 2D or 3D
- Supports radiation shielding example use case

## Requirements

- Python 3.7+
- Docker (optional)
- Docker Compose (optional)

## Installation

### Option 1: Direct Python Installation

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

### Option 2: Docker (Recommended)

1. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

2. Open your browser and go to `http://localhost:5000`

### Option 3: Docker without Compose

1. Build the Docker image:
   ```bash
   docker build -t matrix-eigenvalue-visualizer .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 matrix-eigenvalue-visualizer
   ```

3. Open your browser and go to `http://localhost:5000`

## Usage

1. Enter the desired matrix size (N×N)
2. Click "Generate Matrix Form" to create input fields for each cell
3. Set the minimum, maximum, and step values for each matrix cell
4. Add constraints if needed (e.g., sum of certain cells ≤ value)
5. Set the number of matrices to generate and visualization dimensionality
6. Click "Generate and Visualize" to process and view results

## Architecture

- Frontend: HTML/CSS/JavaScript with jQuery and Plotly.js
- Backend: Flask with NumPy, SciPy, and scikit-learn
- Matrix generation with user-defined rules
- Eigenvalue calculation using SciPy
- Dimensionality reduction using t-SNE
- Interactive visualization with Plotly.js

## Example Use Case

For radiation shielding applications:
- Matrix rows represent layers in the shield
- Matrix columns represent different material properties
- Constraints ensure material percentages sum to appropriate values
- Eigenvalues help analyze the properties of the resulting matrices

## Docker Configuration

The application includes:
- Dockerfile for building the application image
- docker-compose.yml for easy orchestration
- Automatic reloading during development
- Volume mapping to reflect code changes immediately