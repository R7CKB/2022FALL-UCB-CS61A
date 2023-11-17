;和答案一样 Perfect Answer!
(define (my-filter pred s) 
    (cond 
        ((null? s) nil)
        ((pred (car s)) (cons (car s) (my-filter pred (cdr s))))
        (else (my-filter pred (cdr s)))))

;这道题用互递归会不会更好一点？
(define (interleave lst1 lst2) 
    (cond 
        ((null? lst1) lst2)
        ((null? lst2) lst1)
        ((not (null? lst1)) (cons (car lst1) (interleave lst2 (cdr lst1))))))

;使用互递归的话
; (define (interleave lst1 lst2)
;     (if (null? lst1)
;         lst2
;         (cons (car lst1) (interleave1 (cdr lst1) lst2))))

; (define (interleave1 lst1 lst2)
;     (if (null? lst2)
;         lst1
;         (cons (car lst2) (interleave lst1 (cdr lst2)))))


;Official Answer (我感觉我比答案的方法好)
(define (interleave lst1 lst2)
  (if (or (null? lst1) (null? lst2))
      (append lst1 lst2)
      (cons (car lst1)
            (cons (car lst2)
                  (interleave (cdr lst1) (cdr lst2)))))
)


(define (accumulate joiner start n term)
    (if (= n 1)
        (joiner start (term n))
        (joiner (term n) (accumulate joiner start (- n 1) term))))

;Official Answer (思路有一点不同,它是倒着来递归先加start,最后返回start,将start变为结果,我是递归求和)
(define (accumulate joiner start n term)
  (if (= n 0)
    start
    (accumulate joiner (joiner (term n) start) (- n 1) term))
)

;根据题目提示,应该使用my-filter和lambda两个函数制作过滤器
;稍微看了下答案
(define (no-repeats lst) 
    (if (null? lst)
        lst
        (cons (car lst) (no-repeats (my-filter (lambda (x) (not (= (car lst) x))) (cdr lst))))))
