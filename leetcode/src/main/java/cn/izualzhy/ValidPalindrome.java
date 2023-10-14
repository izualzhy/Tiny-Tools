package cn.izualzhy;

public class ValidPalindrome {
    public static boolean validPalindrome(String s) {
        int begin = 0;
        int end = s.length() - 1;

        char[] arr = s.toCharArray();

        while (begin < end) {
            if (arr[begin] == arr[end]) {
                begin++;
                end--;
            } else {
                return isPalindrome(arr, begin + 1, end) || isPalindrome(arr, begin, end - 1);
            }
        }

        return true;
    }

    public static boolean isPalindrome(char[] arr, int begin, int end) {
        while (begin < end) {
            if (arr[begin] != arr[end]) {
                return false;
            } else {
                begin++;
                end--;
            }
        }

        return true;
    }

    public static void main(String[] args) {
        System.out.println(validPalindrome("aba"));
        System.out.println(validPalindrome("abca"));
        System.out.println(validPalindrome("abc"));
        System.out.println(validPalindrome("bcacab"));
        System.out.println(validPalindrome("bcaacab"));
        System.out.println(validPalindrome("acbca"));
    }
}
