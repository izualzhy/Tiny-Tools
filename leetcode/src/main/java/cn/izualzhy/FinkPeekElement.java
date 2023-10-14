package cn.izualzhy;

public class FinkPeekElement {
    public static int findPeakElement(int[] nums) {
        int i = 0, j = nums.length - 1;
        while (i <= j) {
            int middle = i + (j - i) / 2;

            boolean gtLeft = (middle == 0) || (nums[middle] > nums[middle - 1]);
            boolean gtRight = (middle == nums.length - 1) || (nums[middle] > nums[middle + 1]);

            if (gtLeft && gtRight) {
                return middle;
            } else if (gtLeft) {
                i = middle + 1;
            } else if (gtRight) {
                j = middle - 1;
            } else {
                i = middle + 1;
            }
        }

        return -1;
    }

    public static void main(String[] args) {
        System.out.println(findPeakElement(new int[]{1, 2, 3, 4, 5}));
        System.out.println(findPeakElement(new int[]{1, 2, 3, 4, 5, 4, 3, 2, 1}));
        System.out.println(findPeakElement(new int[]{}));
        System.out.println(findPeakElement(new int[]{5, 4, 3, 2, 1}));
        System.out.println(findPeakElement(new int[]{5, 4, 3, 2, 1, 2, 3, 4, 5}));
    }
}
