#Given a string s consisting of words and spaces, return the length of the last word in the string.
#A word is a maximal substring consisting of non-space characters only.
class Solution:
    def length_of_last_word(self, s: str) -> int:
        return len(s.strip().split(" ")[-1])


test = Solution.length_of_last_word(Solution, " Maximal substring consisting of characters ")
print(test)