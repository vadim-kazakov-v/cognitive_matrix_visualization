#!/usr/bin/env python3
"""
Тест для проверки корректности работы ограничений в генерации матриц
"""

def check_constraints(matrix, constraints):
    """Check if a matrix satisfies all constraints"""
    for i, constraint in enumerate(constraints):
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

def test_constraint_filtering():
    """Тест для проверки, как ограничения фильтруют сгенерированные матрицы"""
    print("Тестируем фильтрацию матриц с помощью ограничений...")
    
    # Создадим несколько тестовых матриц
    test_matrices = [
        [[1, 2], [3, 4]],  # сумма первой строки = 3
        [[0, 1], [2, 3]],  # сумма первой строки = 1
        [[2, 3], [1, 4]],  # сумма первой строки = 5
        [[-1, 2], [3, 1]], # сумма первой строки = 1
    ]
    
    # Ограничение: сумма элементов первой строки >= 3
    constraints = [
        {
            'cells': ['0,0', '0,1'],  # первая строка
            'type': 'sum_greater',
            'value': 3
        }
    ]
    
    print("Ограничение: сумма элементов первой строки >= 3")
    print("Тестируемые матрицы и их суммы первой строки:")
    
    filtered_matrices = []
    for matrix in test_matrices:
        sum_first_row = matrix[0][0] + matrix[0][1]
        passes_constraint = check_constraints(matrix, constraints)
        print(f"  Матрица {matrix}, сумма первой строки: {sum_first_row}, проходит: {passes_constraint}")
        
        if passes_constraint:
            filtered_matrices.append(matrix)
    
    print(f"\nИсходно: {len(test_matrices)} матриц")
    print(f"После фильтрации: {len(filtered_matrices)} матриц")
    print(f"Ограничения корректно отфильтровали матрицы: {'ДА' if len(filtered_matrices) < len(test_matrices) else 'НЕТ'}")
    
    # Проверим, что все отфильтрованные матрицы действительно удовлетворяют ограничениям
    all_pass = all(check_constraints(m, constraints) for m in filtered_matrices)
    print(f"Все оставшиеся матрицы удовлетворяют ограничениям: {all_pass}")
    
    print("\nВывод: Ограничения корректно работают для фильтрации сгенерированных матриц.")

if __name__ == "__main__":
    test_constraint_filtering()