# 59. Spiral Matrix II
# Path: Tasks\59_SpiralMatrixII.py
# Given a positive integer n, generate an n x n matrix filled with elements from 1 to n2 in spiral order.
class Solution:
    def generate_matrix(self, n: int) -> list[list[int]]:
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        num = 1
        for layer in range((n + 1) // 2):
            for i in range(layer, n - layer):
                matrix[layer][i] = num
                num += 1
            for i in range(layer + 1, n - layer):
                matrix[i][n - layer - 1] = num
                num += 1
            for i in range(n - layer - 2, layer - 1, -1):
                matrix[n - layer - 1][i] = num
                num += 1
            for i in range(n - layer - 2, layer, -1):
                matrix[i][layer] = num
                num += 1
        return matrix


test = Solution.generate_matrix(Solution, 6)
print(test)
