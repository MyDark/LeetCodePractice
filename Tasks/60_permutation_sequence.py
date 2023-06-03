import math


# 60. Permutation Sequence
# Path: Tasks\60_PermutationSequence.py
# The set [1, 2, 3, ..., n] contains a total of n! unique permutations.
# By listing and labeling all the permutations in order, we get the following sequence for n = 3:
# Given n and k, return the kth permutation sequence.
# Note: Given n will be between 1 and 9 inclusive. Given k will be between 1 and n! inclusive.

class Solution:
    def get_permutation(self, n: int, k: int) -> str:
        nums = [i for i in range(1, n + 1)]
        k -= 1
        res = []
        while n > 0:
            n -= 1
            index, k = divmod(k, math.factorial(n))
            res.append(str(nums[index]))
            nums.remove(nums[index])
        return ''.join(res)


test = Solution.get_permutation(Solution, 3, 3)
print(test)
