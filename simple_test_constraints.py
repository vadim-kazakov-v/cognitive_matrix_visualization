#!/usr/bin/env python3
"""
Простой тест для проверки корректности работы ограничений
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

def test_constraints():
    print("Тестируем работу ограничений...")
    
    # Тест 1: Проверим ограничение на сумму
    matrix = [[1, 2], [3, 4]]
    constraints = [
        {
            'cells': ['0,0', '0,1'],  # ячейки [0,0] и [0,1] - первая строка
            'type': 'sum_greater',
            'value': 2  # сумма должна быть >= 2
        }
    ]
    
    result = check_constraints(matrix, constraints)
    expected_sum = matrix[0][0] + matrix[0][1]  # 1 + 2 = 3
    print(f"Тест 1 - Матрица: {matrix}")
    print(f"Сумма ячеек [0,0] и [0,1]: {expected_sum}")
    print(f"Ограничение: сумма >= 2, результат: {result}")
    print(f"Ожидаемый результат: True (т.к. 3 >= 2)")
    print()
    
    # Тест 2: Проверим ограничение на сумму, которое не выполняется
    constraints2 = [
        {
            'cells': ['0,0', '0,1'],  # ячейки [0,0] и [0,1]
            'type': 'sum_less',
            'value': 2  # сумма должна быть <= 2
        }
    ]
    
    result2 = check_constraints(matrix, constraints2)
    expected_sum2 = matrix[0][0] + matrix[0][1]  # 1 + 2 = 3
    print(f"Тест 2 - Матрица: {matrix}")
    print(f"Сумма ячеек [0,0] и [0,1]: {expected_sum2}")
    print(f"Ограничение: сумма <= 2, результат: {result2}")
    print(f"Ожидаемый результат: False (т.к. 3 > 2)")
    print()
    
    # Тест 3: Проверим ограничение на равенство
    matrix3 = [[1, 1], [2, 3]]
    constraints3 = [
        {
            'cells': ['0,0', '0,1'],  # ячейки [0,0] и [0,1]
            'type': 'sum_equal',
            'value': 2  # сумма должна быть = 2
        }
    ]
    
    result3 = check_constraints(matrix3, constraints3)
    expected_sum3 = matrix3[0][0] + matrix3[0][1]  # 1 + 1 = 2
    print(f"Тест 3 - Матрица: {matrix3}")
    print(f"Сумма ячеек [0,0] и [0,1]: {expected_sum3}")
    print(f"Ограничение: сумма = 2, результат: {result3}")
    print(f"Ожидаемый результат: True (т.к. 2 == 2)")
    print()
    
    # Тест 4: Проверим ограничение на равенство, которое не выполняется
    result4 = check_constraints(matrix, constraints3)  # используем исходную матрицу с ограничением на равенство 2
    expected_sum4 = matrix[0][0] + matrix[0][1]  # 1 + 2 = 3
    print(f"Тест 4 - Матрица: {matrix}")
    print(f"Сумма ячеек [0,0] и [0,1]: {expected_sum4}")
    print(f"Ограничение: сумма = 2, результат: {result4}")
    print(f"Ожидаемый результат: False (т.к. 3 != 2)")
    print()
    
    # Тест 5: Проверим несколько ограничений одновременно
    constraints5 = [
        {
            'cells': ['0,0', '0,1'],  # ячейки [0,0] и [0,1]
            'type': 'sum_greater',
            'value': 2  # сумма должна быть >= 2
        },
        {
            'cells': ['1,0', '1,1'],  # ячейки [1,0] и [1,1]
            'type': 'sum_less',
            'value': 8  # сумма должна быть <= 8
        }
    ]
    
    result5 = check_constraints(matrix, constraints5)
    sum1 = matrix[0][0] + matrix[0][1]  # 1 + 2 = 3, >= 2 -> True
    sum2 = matrix[1][0] + matrix[1][1]  # 3 + 4 = 7, <= 8 -> True
    print(f"Тест 5 - Матрица: {matrix}")
    print(f"Сумма ячеек [0,0] и [0,1]: {sum1}, >= 2: True")
    print(f"Сумма ячеек [1,0] и [1,1]: {sum2}, <= 8: True")
    print(f"Результат: {result5}")
    print(f"Ожидаемый результат: True (оба ограничения выполняются)")
    print()
    
    # Тест 6: Проверим несколько ограничений, одно из которых не выполняется
    constraints6 = [
        {
            'cells': ['0,0', '0,1'],  # ячейки [0,0] и [0,1]
            'type': 'sum_greater',
            'value': 2  # сумма должна быть >= 2
        },
        {
            'cells': ['1,0', '1,1'],  # ячейки [1,0] и [1,1]
            'type': 'sum_less',
            'value': 6  # сумма должна быть <= 6
        }
    ]
    
    result6 = check_constraints(matrix, constraints6)
    sum1_6 = matrix[0][0] + matrix[0][1]  # 1 + 2 = 3, >= 2 -> True
    sum2_6 = matrix[1][0] + matrix[1][1]  # 3 + 4 = 7, <= 6 -> False
    print(f"Тест 6 - Матрица: {matrix}")
    print(f"Сумма ячеек [0,0] и [0,1]: {sum1_6}, >= 2: True")
    print(f"Сумма ячеек [1,0] и [1,1]: {sum2_6}, <= 6: False")
    print(f"Результат: {result6}")
    print(f"Ожидаемый результат: False (второе ограничение не выполняется)")
    print()
    
    print("Все тесты выполнены!")

if __name__ == "__main__":
    test_constraints()