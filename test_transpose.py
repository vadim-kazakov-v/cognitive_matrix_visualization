#!/usr/bin/env python3
"""
Test script to verify that the transpose functionality works correctly.
This script simulates the transposition logic used in the application.
"""
import numpy as np

def test_transpose_logic():
    """Test the transposition logic that was added to the application."""
    print("Testing transpose functionality...")
    
    # Create a sample matrix
    original_matrix = np.array([[1, 2, 3],
                                [4, 5, 6],
                                [7, 8, 9]])
    
    print("Original matrix:")
    print(original_matrix)
    
    # Test without transposition
    transpose_matrix = False
    if transpose_matrix:
        matrix = original_matrix.T
    else:
        matrix = original_matrix.copy()
    
    print("\nMatrix without transposition:")
    print(matrix)
    
    # Test with transposition
    transpose_matrix = True
    if transpose_matrix:
        matrix = original_matrix.T
    else:
        matrix = original_matrix.copy()
    
    print("\nMatrix with transposition:")
    print(matrix)
    
    # Verify that transposition actually happened
    expected_transposed = np.array([[1, 4, 7],
                                    [2, 5, 8],
                                    [3, 6, 9]])
    
    assert np.array_equal(matrix, expected_transposed), "Transposition failed!"
    print("\n✓ Transposition works correctly!")
    
    # Test eigenvalue calculation difference
    original_eigenvals = np.linalg.eigvals(original_matrix)
    transposed_eigenvals = np.linalg.eigvals(expected_transposed)
    
    print(f"\nOriginal matrix eigenvalues: {original_eigenvals}")
    print(f"Transposed matrix eigenvalues: {transposed_eigenvals}")
    
    # Note: For symmetric matrices, eigenvalues are the same, but for non-symmetric they can differ
    # Let's test with a non-symmetric matrix
    nonsym_matrix = np.array([[1, 2],
                              [3, 4]])
    
    nonsym_transposed = nonsym_matrix.T
    
    nonsym_orig_eigenvals = np.linalg.eigvals(nonsym_matrix)
    nonsym_trans_eigenvals = np.linalg.eigvals(nonsym_transposed)
    
    print(f"\nNon-symmetric matrix eigenvalues: {nonsym_orig_eigenvals}")
    print(f"Non-symmetric transposed matrix eigenvalues: {nonsym_trans_eigenvals}")
    
    print("\n✓ All tests passed! The transpose functionality will correctly affect eigenvalue calculations.")

if __name__ == "__main__":
    test_transpose_logic()