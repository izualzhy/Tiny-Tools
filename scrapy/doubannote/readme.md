
## 1. 代码

豆瓣note的爬虫，使用 scrapy 完成，代码比较简单。

安全问题去掉了mysql_model.py里相关数据库配置

```
DB_CONNECT_STRING = 'mysql+mysqldb://${user}:${passwd}@${hostname}:3306/scrapy'
```

ip代理地址从<http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&p>这里获取.

修改后开箱即用

## 2. 分析

<https://izualzhy.cn/douban-note>用到的分析sql

```
select year(pub_date),count(*) from doubannote group by year(pub_date);
select * from doubannote order by pub_date limit 1\G
select * from doubannote order by pub_date desc limit 1\G
select date_format(pub_date, "%H") t, count(*) from doubannote  group by t;
select count(distinct(author)) from doubannote
select t.c, count(*) from (select count(*) c from doubannote group by author) t group by t.c;
select tags from doubannote where tags != ""
select comment_num, count(*) from doubannote group by comment_num;
```
