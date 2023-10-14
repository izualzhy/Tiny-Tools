package cn.izualzhy;

public class ReverseList {

    public static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode current = head;

        while (current != null) {
            ListNode next = current.next;
            current.next = prev;

            prev = current;
            current = next;
        }

        return prev;
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(100);
        ListNode prev = head;
        for (int i = 0; i < 10; i++) {
            ListNode node = new ListNode(i);
            prev.next = node;

            prev = node;
        }

        Util.traverseList(head);
        head = reverseList(head);
        Util.traverseList(head);
    }
}
