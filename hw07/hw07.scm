;我和答案的写法不一样，答案喜欢写在同一行，我比较喜欢分开写，更有层次，看得更明白
(define (cddr s) (cdr (cdr s))) ;返回列表的第三个元素及其之后的元素

(define (cadr s) (car (cdr s))) ;返回列表的第二个元素

(define (caddr s) (car (cddr s))) ;返回列表的第三个元素

;只是为了好玩，如果这是一个 Python 链表问题，那么解决方案可能如下所示
;cadr = lambda l: l.rest.first
;caddr = lambda l: l.rest.rest.first

(define (ascending? asc-lst) 
    (if (or(null? asc-lst)(null? (cdr asc-lst)));我没有考虑列表为空的情况,看完答案后补上的
        #t
        (if (<= (car asc-lst) (cadr asc-lst))
            (ascending? (cdr asc-lst))
            #f)))

;Official Answer (思路是一样的，没什么问题，就是刚开始有点搞不没明白他的语法规则，有点奇怪 (,,•́ . •̀,,) )
(define (ascending? asc-lst)
  (if (or (null? asc-lst) (null? (cdr asc-lst))) ;我没有用到or和and有点可惜，下次争取用到
      #t
      (and (<= (car asc-lst) (car (cdr asc-lst))) (ascending? (cdr asc-lst))));这一行有点东西,不用添加#f，使用and来判断否满足条件
)

(define (square n) (* n n))

(define (pow base exp) ;肯定使用递归啊!!
    (if (= exp 1)
        base
        (if (even? exp)
            (square (pow base (/ exp 2)))
            (* base (pow base (- exp 1))))))

;Official Answer (思路也是一样的,只不过它是exp=0,我是exp=1)
(define (pow base exp)
  (cond ((= exp 0) 1);他在课中好像没有讲到cond吧,╥﹏╥
        ((even? exp) (square (pow base (/ exp 2))))
        (else (* base (pow base (- exp 1)))))
)