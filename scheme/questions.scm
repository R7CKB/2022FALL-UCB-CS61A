(define (caar x) (car (car x)));取出第一个元素中的第一个元素
(define (cadr x) (car (cdr x)));取出第二个元素
(define (cdar x) (cdr (car x)));取出第一个元素中的除第一个外的其余元素
(define (cddr x) (cdr (cdr x)));取出前两个元素之后的元素

;; Problem 15
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 15
  ; 使用辅助函数
  (define (helper s index)
    (if (null? s) 
      nil
    (cons (list index (car s)) (helper (cdr s) (+ index 1))))
  )
  (helper s 0)
  )
  ; END PROBLEM 15

;; Problem 16

;; Merge two lists LIST1 and LIST2 according to ORDERED? and return
;; the merged lists.
(define (merge ordered? list1 list2)
    (cond 
      ((null? list1) list2)
      ((null? list2) list1)
      ((ordered? (car list1) (car list2)) 
      (cons(car list1) (cons (car list2) (merge ordered? (cdr list1) (cdr list2)))))
      (else 
      (cons(car list2) (cons (car list1) (merge ordered? (cdr list1) (cdr list2))))))
  )
  ; END PROBLEM 16

;; Optional Problem 2

;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; cheated
;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN OPTIONAL PROBLEM 2
         ;如果是原子表达式的话就返回自身
         expr
         ; END OPTIONAL PROBLEM 2
         )
        ((quoted? expr)
         ; BEGIN OPTIONAL PROBLEM 2
         ;如果是quote表达式的话也返回自身
         expr
         ; END OPTIONAL PROBLEM 2
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           ;这个也有点难度
           ;当expr为lambda或define form时，需要考虑body中可能出现的let form
           (cons form (cons (map let-to-lambda params) (map let-to-lambda body)))
           ; END OPTIONAL PROBLEM 2
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN OPTIONAL PROBLEM 2
           (cons (cons 'lambda 
                     (cons (car (zip (let-to-lambda values))) (let-to-lambda body))) 
                (cadr (zip (let-to-lambda values))))
           ; END OPTIONAL PROBLEM 2
           ))
        (else
         ; BEGIN OPTIONAL PROBLEM 2
         (map let-to-lambda expr)
         ; END OPTIONAL PROBLEM 2
         )))

; Some utility functions that you may find useful to implement for let-to-lambda

(define (zip pairs)
  (list (map car pairs) (map cadr pairs)))
