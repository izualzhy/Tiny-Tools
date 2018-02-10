#include <string>
#include <iostream>

#include "boost/multi_index_container.hpp"
#include "boost/multi_index/hashed_index.hpp"
#include "boost/multi_index/sequenced_index.hpp"
#include "boost/multi_index/member.hpp"
#include "gtest/gtest.h"

template <class T, class V>
class LRUCache {
public:
    explicit LRUCache(int capacity) :
        _capacity(capacity) {
        }

    void put(T key, V value) {
        //try put new items at the begining of the cache
        auto iter = _lru_container.push_front(LRUNode(key, value));
        if (!iter.second) {
            //exists already, modify and inset iter before begin()
            _lru_container.modify(iter.first, [value](LRUNode &node){node.value = value;});
            _lru_container.relocate(_lru_container.begin(), iter.first);
        } else if (_lru_container.size() > _capacity) {
            //oversize, pop the item at the end of the cache
            _lru_container.pop_back();
        }
    }

    bool get(T key, V* value) {
        auto iter = _lru_container.template get<1>().find(key);
        //exists
        if (iter != _lru_container.template get<1>().end()) {
            *value = iter->value;
            //move to the begin
            _lru_container.relocate(
                    _lru_container.begin(),
                    _lru_container.template project<0>(iter));
            return true;
        }

        return false;
    }

    std::string dump() const {
        std::string s;
        for (const auto& item : _lru_container) {
            s.append(item.key).append("\t").append(item.value).append("\n");
        }
        return s;
    }
private:
    struct LRUNode {
        LRUNode(T key_, V value_) :
            key(key_),
            value(value_) {
            }
        T key;
        V value;
    };

    typedef boost::multi_index::multi_index_container<
        LRUNode,
        boost::multi_index::indexed_by<
            boost::multi_index::sequenced<>,
            boost::multi_index::hashed_unique<
                boost::multi_index::member<LRUNode, T, &LRUNode::key> >
        >
    > LRUContainer;

private:
    LRUContainer _lru_container;
    int _capacity;
};//LRUCache

TEST(lru, en_wiki) {
    LRUCache<std::string, std::string> lru_cache(4);
    lru_cache.put("A", "Amanda");
    lru_cache.put("B", "Bruce");
    lru_cache.put("C", "Chris");
    lru_cache.put("D", "Demon");

    std::string expected_str("D\tDemon\nC\tChris\nB\tBruce\nA\tAmanda\n");
    EXPECT_EQ(lru_cache.dump(), expected_str);

    lru_cache.put("E", "Elina");
    expected_str.assign("E\tElina\nD\tDemon\nC\tChris\nB\tBruce\n");
    EXPECT_EQ(lru_cache.dump(), expected_str);

    lru_cache.put("D", "Darel");
    expected_str.assign("D\tDarel\nE\tElina\nC\tChris\nB\tBruce\n");
    EXPECT_EQ(lru_cache.dump(), expected_str);

    lru_cache.put("F", "Frank");
    expected_str.assign("F\tFrank\nD\tDarel\nE\tElina\nC\tChris\n");
    EXPECT_EQ(lru_cache.dump(), expected_str);

    std::string s;
    auto get_ok = lru_cache.get("D", &s);
    EXPECT_TRUE(get_ok);
    EXPECT_EQ(s, "Darel");
    expected_str.assign("D\tDarel\nF\tFrank\nE\tElina\nC\tChris\n");
    EXPECT_EQ(lru_cache.dump(), expected_str);

    get_ok = lru_cache.get("G", &s);
    EXPECT_TRUE(!get_ok);
}

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();

    return 0;
}

/* vim: set ts=4 sw=4 sts=4 tw=100 */
