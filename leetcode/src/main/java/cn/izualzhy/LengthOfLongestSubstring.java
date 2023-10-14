package cn.izualzhy;

import java.util.HashMap;
import java.util.Map;

public class LengthOfLongestSubstring {
    public static int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> lastIndex = new HashMap<>();
        int maxLength = 0;
        int currentStartIndex = 0;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (lastIndex.containsKey(c) && lastIndex.get(c) >= currentStartIndex) {
                int currentLength = i - lastIndex.get(c);
//                System.out.println("currentLength = " + currentLength);
                maxLength = Math.max(maxLength, currentLength);

                currentStartIndex = lastIndex.get(c) + 1;

//                System.out.println("currentStartIndex = " + currentStartIndex);
            } else {
                int currentLength = i - currentStartIndex + 1;
//                System.out.println("currentLength = " + currentLength);
                maxLength = Math.max(maxLength, currentLength);
            }

            lastIndex.put(c, i);
        }

        return maxLength;
    }

    public static void main(String[] args) {
        System.out.println(lengthOfLongestSubstring("abcabcbb"));
        System.out.println(lengthOfLongestSubstring("bbbbb"));
        System.out.println(lengthOfLongestSubstring("pwwkew"));
        System.out.println(lengthOfLongestSubstring(""));
        System.out.println(lengthOfLongestSubstring("abba"));
    }
}
