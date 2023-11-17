;Q3
;这是使用cond方法 答案和我思路是一样的
(define (over-or-under num1 num2) 
    (cond 
        ((< num1 num2) -1)
        ((> num1 num2) 1)
        (else 0)))

;使用if方法
(define (over-or-under num1 num2)
    (if (< num1 num2)
        -1
        (if (> num1 num2)
            1
            (if (= num1 num2)
            0))))

;Q4
;使用lambda表达式 和答案一样
(define (make-adder num) (lambda (inc) (+ num inc)))

;采用define嵌套表达式
(define (make-adder num) (define (inner inc) (+ num inc)) inner)

;Q5
;使用lambda表达式 和答案一样
(define (composed f g) (lambda (x) (f(g x))))

;采用define嵌套表达式
(define (composed f g) (define (inner x) (f(g x))) inner)

;Q6
;服了 这个ok测试最后一问卡了我半天，原来是按照给的图写出列表，英文就不能说的直白一点吗 T.T
;使用cons
(define lst (cons 
                (cons 1 nil) 
                    (cons 2 
                        (cons (cons 3 (cons 4 nil)) 
                            (cons 5 nil)))))

;使用list
(define lst (list (list 1) 2 (list 3 4) 5))

;Q7 答案是当列表为空时返回lst,和我的一样
(define (duplicate lst) ;我觉得也要用到递归
    (if (null? lst)
        nil
        (cons (car lst) (cons (car lst) (duplicate (cdr lst))))))

(define (vir-fib n)
    (cond
        ((= n 1) 1)
        ((= n 2) 1)
        (else (+ (vir-fib (- n 1)) (vir-fib (- n 2))))))
