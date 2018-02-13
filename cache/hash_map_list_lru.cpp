#include "sys/time.h"
#include <vector>
#include <iostream>
#include <unordered_map>
// #include "gtest/gtest.h"

template <class K, class T>
struct Node {
    K key;
    T data;
    Node* prev, *next;

    Node()
        : prev(NULL)
        , next(NULL) {}
};

template <class K, class T>
class LRUCache {
public:
    LRUCache(size_t size) :
        head_(NULL),
        tail_(NULL),
        entries_(NULL),
        capacity_(size) {
        initialize();
    }

    ~LRUCache() {
        delete head_;
        delete tail_;
        delete[] entries_;
    }

    void put(K key, T data) {
        Node<K, T>* node = hashmap_[key];

        if (node) { // node exists
            detach(node);
            node->data = data;
            attach(node);
        } else {
            if (free_entries_.empty()) {
                node = tail_->prev;
                detach(node);
                hashmap_.erase(node->key);
            } else {
                node = free_entries_.back();
                free_entries_.pop_back();
            }

            node->key = key;
            node->data = data;
            hashmap_[key] = node;
            attach(node);
        }
    }

    bool get(K key, T* value) {
        auto iter = hashmap_.find(key);

        if (iter != hashmap_.end()) {
            Node<K, T>* node = iter->second;
            detach(node);
            attach(node);
            *value = node->data;
            return true;
        }
        return false;
    }

    std::string dump() const {
        std::string s;
        Node<K, T>* iter = head_->next;
        while (iter != tail_) {
            s.append(iter->key).append("\t").append(iter->data).append("\n");
            iter = iter->next;
        }

        return s;
    }

private:
    void initialize() {
        hashmap_.clear();
        free_entries_.clear();
        if (entries_ != NULL) {
            delete[] entries_;
        }
        entries_ = new Node<K, T>[capacity_];
        for (size_t i = 0; i < capacity_; ++i) {
            free_entries_.push_back(entries_ + i);
        }
        if (head_ != NULL) {
            delete head_;
        }
        head_ = new Node<K, T>;
        if (tail_ != NULL) {
            delete tail_;
        }
        tail_ = new Node<K, T>;
        head_->prev = NULL;
        head_->next = tail_;
        tail_->prev = head_;
        tail_->next = NULL;
    }

    void detach(Node<K, T>* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    void attach(Node<K, T>* node) {
        node->prev = head_;
        node->next = head_->next;
        head_->next = node;
        node->next->prev = node;
    }
private:
    std::unordered_map<K, Node<K, T>* > hashmap_;
    std::vector<Node<K, T>* > free_entries_;
    Node<K, T>* head_, *tail_;
    Node<K, T>* entries_;
    uint32_t capacity_;
};

// TEST(lru, en_wiki) {
    // LRUCache<std::string, std::string> lru_cache(4);
    // lru_cache.put("A", "Amanda");
    // lru_cache.put("B", "Bruce");
    // lru_cache.put("C", "Chris");
    // lru_cache.put("D", "Demon");

    // std::string expected_str("D\tDemon\nC\tChris\nB\tBruce\nA\tAmanda\n");
    // EXPECT_EQ(lru_cache.dump(), expected_str);

    // lru_cache.put("E", "Elina");
    // expected_str.assign("E\tElina\nD\tDemon\nC\tChris\nB\tBruce\n");
    // EXPECT_EQ(lru_cache.dump(), expected_str);

    // lru_cache.put("D", "Darel");
    // expected_str.assign("D\tDarel\nE\tElina\nC\tChris\nB\tBruce\n");
    // EXPECT_EQ(lru_cache.dump(), expected_str);

    // lru_cache.put("F", "Frank");
    // expected_str.assign("F\tFrank\nD\tDarel\nE\tElina\nC\tChris\n");
    // EXPECT_EQ(lru_cache.dump(), expected_str);

    // std::string s;
    // auto get_ok = lru_cache.get("D", &s);
    // EXPECT_TRUE(get_ok);
    // EXPECT_EQ(s, "Darel");
    // expected_str.assign("D\tDarel\nF\tFrank\nE\tElina\nC\tChris\n");
    // EXPECT_EQ(lru_cache.dump(), expected_str);

    // get_ok = lru_cache.get("G", &s);
    // EXPECT_TRUE(!get_ok);
// }

// int main(int argc, char** argv) {
    // testing::InitGoogleTest(&argc, argv);
    // return RUN_ALL_TESTS();
// }

void test(const int n) {
    struct timeval start_tv, end_tv;
    gettimeofday(&start_tv, NULL);

    LRUCache<int, int> lru_cache(n);
    //put
    for (int i = 0; i < n; ++i) {
        lru_cache.put(i, i);
    }
    int value = -1;
    //get
    for (int i = 0; i < n; ++i) {
        lru_cache.get(i, &value);
    }
    //put
    for (int i = n; i < 2*n; ++i) {
        lru_cache.put(i, i);
    }

    gettimeofday(&end_tv, NULL);

    std::cout << "n:" << n << "\ttime:" << (end_tv.tv_sec - start_tv.tv_sec) * 1000000.0 + (end_tv.tv_usec - start_tv.tv_usec) << std::endl;
}

int main() {
    test(100000);
    test(1000000);
    test(10000000);

    return 0;
}
