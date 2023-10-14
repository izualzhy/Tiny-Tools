package cn.izualzhy;

public class Util {
    public static void traverseList(ListNode head) {
        ListNode currentNode = head;
        while (currentNode != null) {
            System.out.print(currentNode.val + " -> ");
            currentNode = currentNode.next;
        }
        System.out.println("\n");
    }
}
