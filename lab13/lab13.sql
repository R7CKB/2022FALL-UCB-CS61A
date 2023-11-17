.read data.sql


CREATE TABLE bluedog AS
  SELECT color as colour,pet as pets 
  from students
  where color="blue" and pet="dog" ;

CREATE TABLE bluedog_songs AS
  SELECT color,pet,song
  from students
  where color='blue' and pet='dog';

  -- 意思是只有猜的独特的数才会被挑选出来，即别人没猜到这个数
CREATE TABLE smallest_int_having AS
  SELECT time,smallest
  from students
  group by smallest
  having count(smallest)=1;


-- 注意的是要确保第一个人有较早的时间
CREATE TABLE matchmaker AS
  SELECT a.pet,a.song,a.color,b.color
  from students as a,students as b
  where a.time<b.time and a.pet=b.pet and a.song=b.song;

-- 难倒是不难,还有一个条件是要求两个表链接,用时间一样来建立连接
CREATE TABLE sevens AS
  SELECT a.seven
  from students as a,numbers as b
  where a.number=7 and b.'7'='True' and a.time=b.time;


CREATE TABLE average_prices AS
  SELECT category,avg(MSRP) as average_price
  from products
  group by category;


CREATE TABLE lowest_prices AS
  SELECT store,item,min(price)
  from inventory
  group by item;

CREATE TABLE worth_shopping AS
  SELECT category,name,min(MSRP/rating)
  from products
  group by category;

CREATE TABLE shopping_list AS
  SELECT item,store
  from lowest_prices,worth_shopping
  where item=worth_shopping.name and store=lowest_prices.store;


CREATE TABLE total_bandwidth AS
  SELECT sum(Mbs)
  from stores,shopping_list
  where stores.store=shopping_list.store;





