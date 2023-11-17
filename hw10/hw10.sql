CREATE TABLE parents AS
  SELECT "abraham" AS parent, "barack" AS child UNION
  SELECT "abraham"          , "clinton"         UNION
  SELECT "delano"           , "herbert"         UNION
  SELECT "fillmore"         , "abraham"         UNION
  SELECT "fillmore"         , "delano"          UNION
  SELECT "fillmore"         , "grover"          UNION
  SELECT "eisenhower"       , "fillmore";

CREATE TABLE dogs AS
  SELECT "abraham" AS name, "long" AS fur, 26 AS height UNION
  SELECT "barack"         , "short"      , 52           UNION
  SELECT "clinton"        , "long"       , 47           UNION
  SELECT "delano"         , "long"       , 46           UNION
  SELECT "eisenhower"     , "short"      , 35           UNION
  SELECT "fillmore"       , "curly"      , 32           UNION
  SELECT "grover"         , "short"      , 28           UNION
  SELECT "herbert"        , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
-- 主要就是a.parent=b.child 将两个表联系到一起
/*多行注释*/
-- 写对了
CREATE TABLE by_parent_height AS
  SELECT child
  from parents as a,dogs as b
  where a.parent=b.name
  ORDER by height DESC;


-- The size of each dog
-- 最重要的是比较条件
CREATE TABLE size_of_dogs AS
  SELECT name,size
  from dogs as a,sizes as b
  where b.min<a.height and a.height<=b.max ;


-- Filling out this helper table is optional
CREATE TABLE siblings AS
  SELECT a.child as first,b.child as second
  from parents as a,parents as b
  -- 下面这个条件很关键,必须要用小于才会显示出正确的兄弟数量,要不然就会卡BUG
  where a.parent=b.parent and a.child<b.child;

-- Sentences about siblings that are the same size
-- cheated
CREATE TABLE sentences AS
  SELECT "The two siblings, "|| first ||" plus "|| second ||" have the same size: "||a.size
  from siblings,size_of_dogs as a,size_of_dogs as b
  where a.name=first and b.name=second and a.size=b.size;

