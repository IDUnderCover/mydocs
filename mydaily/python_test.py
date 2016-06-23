#!/usr/bin/env python
import time
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        length = len(s)
        if length < 2:
            return length
        l = 0
        r = 1
        max_len = 1
        cur_len = 1
        list_zero = [0]
        hash_table = list_zero * 200 

        
        while l < length and r < length:
            hash_table[ord(s[l])] = 1
            num = ord(s[r])
            res = hash_table[num]
            print('res',res, 'l',l,'r',r)
            if res == 0:
                hash_table[num] = r
                cur_len += 1
                if max_len < cur_len:
                    max_len = cur_len
                r += 1
            else:
                l = res 
                hash_table = list_zero * 200 
                cur_len = 1
                r = l + 1
                
            
        return max_len
            



if __name__ == '__main__':
    s = Solution()
    string = "aaa"

    t1 = time.time()
    res = s.lengthOfLongestSubstring(string)
    t2 = time.time()
    print(t2 - t1, res)
