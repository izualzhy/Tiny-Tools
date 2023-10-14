package cn.izualzhy;

import java.util.*;

public class TreeNodePathSumTwo {
    List<List<Integer>> pathSum(TreeNode root, int targetNum) {
        List<LinkedList<Integer>> result = twoNodePathSumTwo(root, targetNum);
        if (result == null) {
            return new ArrayList<>();
        }
        return new ArrayList<>(result);
    }

    List<LinkedList<Integer>> twoNodePathSumTwo(TreeNode root, int targetNum) {
        List<LinkedList<Integer>> result = new ArrayList<>();
        if (root == null) {
            return null;
        } else if (root.left == null && root.right == null) {
            if (root.val == targetNum) {
                result.add(new LinkedList<>(Collections.singletonList(root.val)));
            }
        }

        List<LinkedList<Integer>> leftResult = null, rightResult = null;
        if (root.left != null) {
            leftResult = twoNodePathSumTwo(root.left, targetNum - root.val);
            if (leftResult != null) {
                leftResult.forEach(l -> l.addFirst(root.val));
                result.addAll(leftResult);
            }
        }
        if (root.right != null) {
            rightResult = twoNodePathSumTwo(root.right, targetNum - root.val);
            if (rightResult != null) {
                rightResult.forEach(l -> l.addFirst(root.val));
                result.addAll(rightResult);
            }
        }

        return result;
    }

    public static void main(String[] args) {

    }
}
