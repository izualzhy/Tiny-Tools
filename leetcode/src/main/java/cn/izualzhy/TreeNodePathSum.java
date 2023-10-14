package cn.izualzhy;

public class TreeNodePathSum {
    public static boolean hasPathSum(TreeNode root, int targetSum) {
        if (root == null) {
            return false;
        }

        return treeNodePathSum(root, targetSum);
    }

    public static boolean treeNodePathSum(TreeNode root, int targetSum) {
        if (root == null) {
            return false;
        } else if (root.left == null && root.right == null) {
            return targetSum == root.val;
        }

        return treeNodePathSum(root.left, targetSum - root.val) || treeNodePathSum(root.right, targetSum - root.val);
    }

    public static void main(String[] args) {
    }
}
