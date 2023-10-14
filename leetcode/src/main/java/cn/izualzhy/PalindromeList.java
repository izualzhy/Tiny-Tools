package cn.izualzhy;

public class PalindromeList {
    public static boolean isPalindromeList(ListNode head) {
        ListNode current = head;
        int listLength = 0;

        // 计算链表长度
        while (current != null) {
            listLength++;
            current = current.next;
        }
//        System.out.println("listLength = " + listLength);

        // 指向链表后半段
        current = head;
        for (int i = 0; i < (listLength + 1) / 2; i++) {
            current = current.next;
        }
//        System.out.println("current = " + current.val);

        ListNode prev = null;

        // 反转后半段
        while (current != null) {
            ListNode next = current.next;

            current.next = prev;
            prev = current;
            current = next;
        }

        // 比较前后半段是否相同
        current = prev;
//        System.out.println("current = " + current.val);
        while (current != null) {
            if (current.val == head.val) {
                current = current.next;
                head = head.next;
            } else {
                return false;
            }
        }

        return true;
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(123);
        ListNode prev = head;
        ListNode node = null;
        for (int i = 0; i <= 6; i++) {
            node = new ListNode(i);
            prev.next = node;
            prev = node;
        }

        node = new ListNode(321);
        prev.next = node;
        prev = node;

        for (int i = 6; i >= 0; i--) {
            node = new ListNode(i);
            prev.next = node;

            prev = node;
        }
        node = new ListNode(123);
        prev.next = node;

//        node.next = new ListNode(321);

//        Util.traverseList(head);
        System.out.println(isPalindromeList(head));
    }
}
