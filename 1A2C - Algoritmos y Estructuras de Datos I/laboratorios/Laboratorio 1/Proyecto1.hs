-- ejercicio 1 a
esCero :: Int -> Bool 
esCero n = n == 0

-- $> esCero 0 
-- True
-- $> esCero 5 
-- False

-- ejercicio 1 b
esPositivo :: Int -> Bool
esPositivo n = n > 0

-- $> esPositivo (-1) 
-- False
-- $> esPositivo 0 
-- False
-- $> esPositivo 5 
-- True

-- ejercicio 1 c
esVocal :: Char -> Bool
esVocal c = c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'

-- $> esVocal 'a' 
-- True
-- $> esVocal 'G' 
-- False

-- ejercicio 1 d
valorAbsoluto :: Int -> Int
valorAbsoluto n = abs n

-- $> valorAbsoluto 26 
-- 26
-- $> valorAbsoluto (-26)
-- 26

-- ejercicio 2 a
paratodo :: [Bool] -> Bool
paratodo [] = True
paratodo (x:xs) = x && paratodo xs

-- $> paratodo [True, False, True]
-- False
-- $> paratodo [True, True]
-- True

-- ejercicio 2 b
sumatoria :: [Int] -> Int
sumatoria [] = 0
sumatoria (x:xs) = x + sumatoria xs

-- $> sumatoria [] 
-- 0
-- $> sumatoria [2,5,1] 
-- 8

-- ejercicio 2 c
productoria :: [Int] -> Int
productoria [] = 1
productoria (x:xs) = x * productoria xs

-- $> productoria [] 
-- 1
-- $> productoria [2,5,6] 
-- 60

-- ejercicio 2 d
factorial :: Int -> Int
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- $> factorial 0 
-- 1
-- $> factorial 4 
-- 24

-- ejercicio 2 e
promedio :: [Int] -> Int
promedio xs = sumatoria xs `div` length xs

-- $> promedio [6,8,10]
-- 8
-- $> promedio [6,8,9]
-- 7

-- ejercicio 3
pertenece :: Int -> [Int] -> Bool
pertenece n [] = False
pertenece n (x:xs) = n == x || pertenece n xs

-- $> pertenece 5 []
-- False
-- $> pertenece 5 [2,5,1]
-- True
-- $> pertenece 5 [2,6,3] 
-- False

-- ejercicio 4 a
paratodo' :: [a] -> (a -> Bool) -> Bool
paratodo' [] t = True
paratodo' (x:xs) t = t x && paratodo' xs t

-- $> paratodo' [0,0,0] esCero
-- True
-- $> paratodo' [0,3,7] esPositivo
-- False

-- ejercicio 4b 
existe' :: [a] -> (a -> Bool) -> Bool
existe' [] t = False
existe' (x:xs) t = t x || existe' xs t

-- $> existe' [2,6,0,1] esCero
-- True
-- $> existe' [2, -1, -5] esPositivo
-- True
-- $> existe' "HOLA" esVocal
-- False

-- ejercicio 4 c
sumatoria' :: [a] -> (a -> Int) -> Int
sumatoria' [] t = 0
sumatoria' (x:xs) t = t x + sumatoria' xs t

-- $> sumatoria' [2,-3,4,-5] valorAbsoluto
-- 14
-- $> sumatoria' [2,4,2] factorial
-- 28

-- ejercicio 4 d
productoria' :: [a] -> (a -> Int) -> Int
productoria' [] t = 1
productoria' (x:xs) t = t x * productoria' xs t

-- $> productoria' [2,-3,4,-5] valorAbsoluto
-- 120
-- $> productoria' [2,4,2] factorial
-- 96

-- ejercicio 5 
paratodo'' :: [a] -> (a -> Bool) -> Bool
paratodo'' xs t' = paratodo' xs t' 

-- $> paratodo'' [0, 0, 0] esCero
-- True
-- $> paratodo'' [0, 0, 1] esCero
-- False
-- $> paratodo'' [3, 0, 1] esPositivo
-- False

-- ejercicio 6 a
todosPares :: [Int] -> Bool 
todosPares xs = paratodo'' xs even

-- $> todosPares [2,5,1,4]
-- False
-- $> todosPares [2,6,2,4]
-- True

-- ejercicio 6 b
esMultiplo :: Int -> Int -> Bool
esMultiplo n x = mod x n == 0

hayMultiplo :: Int -> [Int] -> Bool
hayMultiplo n xs = existe' xs (esMultiplo n)

-- $> hayMultiplo 2 [8,5,6] 
-- True
-- $> hayMultiplo 2 [9,5,7]
-- False
-- $> hayMultiplo 11 [22]
-- True

-- ejercicio 6 c
sumaCuadrados :: Int -> Int
sumaCuadrados n = sumatoria' [0..(n-1)] (^2)

-- $> sumaCuadrados 2
-- 1
-- $> sumaCuadrados 4
-- 14
-- $> sumaCuadrados 5
-- 30

-- ejercicio 6 d
esDivisor :: Int -> Int -> Bool
esDivisor n x = mod n x == 0

existeDivisor :: Int -> [Int] -> Bool
existeDivisor n xs = existe' xs (esDivisor n)

-- $> existeDivisor 7 [8,2]
-- False
-- $> existeDivisor 7 [8,2,7]
-- True
-- $> existeDivisor 7 [8,2,14]  
-- False

-- ejercicio 6 e
esPrimo :: Int -> Bool
esPrimo n = n > 1 && not (existeDivisor n [2..(n-1)])

-- $> esPrimo 6
-- False
-- $> esPrimo 13
-- True

-- ejercicio 6 f
factorial' :: Int -> Int
factorial' n = productoria [1..n]

-- $> factorial' 0 
-- 1
-- $> factorial' 4 
-- 24

-- ejercicio 6 g
esPrimo' :: Int -> Int
esPrimo' n  | esPrimo n = n
            | otherwise = 1

multiplicaPrimos :: [Int] -> Int
multiplicaPrimos xs = productoria' xs esPrimo'

-- $> multiplicaPrimos [2,3,5,4,10]
-- 30
-- $> multiplicaPrimos [21,2,11,2]
-- 44

-- ejercicio 6 h 
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n-1) + fib (n-2)

esFib :: Int -> Bool
esFib n = pertenece n (map fib [1..(n+1)])

-- $> esFib 2
-- True
-- $> esFib 3
-- True
-- $> esFib 9
-- False

-- ejercicio 6 i
todosFib :: [Int] -> Bool
todosFib xs = paratodo' xs esFib

-- $> todosFib [2,3,5,8]
-- True
-- $> todosFib [10]
-- False

-- ejercicio 7 a
{-
-La funcion map aplica funciones a una lista, y la funcion filter toma elementos de una lista que
cumple determinadas condiciones, ambas devuelven una lista.

-La expresion map succ [1, -4, 6, 2, -8], donde succ n = n+1 equivale a aplicar la funcion succ
a la lista [1, -4, 6, 2, -8], creando otra sumando a cada elemento uno, devolviendo [2, -3, 7, 3, -7]

    $> map succ [0,1,2,3]
    [1,2,3,4]
    $> map succ [-1,-2,-3,-4]
    [0,-1,-2,-3]

-La expresion filter esPositivo [1, -4, 6, 2, -8] toma elementos de la lista [1, -4, 6, 2, -8]
que cumple con la condicion esPositivo, devolviendo la lista [1, 6, 2]

    $> filter esPositivo [0,1,2,3]
    [1,2,3]
    $> filter esPositivo [-1,-2,-3,-4]
    []
-} 

-- ejercicio 8 a
duplicar :: [Int] -> [Int]
duplicar [] = []
duplicar (x:xs) = (2 * x) : duplicar xs

-- $> duplicar [2,5,6,1]
-- [4,10,12,2]
-- $> duplicar [3,4,7,0]
-- [6,8,14,0]

-- ejercicio 8 b
duplicar' :: [Int] -> [Int]
duplicar' xs = map (*2) xs

-- $> duplicar' [2,5,6,1]
-- [4,10,12,2]
-- $> duplicar' [3,4,7,0]
-- [6,8,14,0]

-- ejercicio 9 a
primos :: [Int] -> [Int]
primos [] = []
primos (x:xs) 	| esPrimo x = x : primos xs
	      	    | otherwise = primos xs
	      
-- $> primos [1..10]
-- [2,3,5,7]
-- $> primos [16..33]
-- [17,19,23,29,31]

-- ejercicio 9 b
primos' :: [Int] -> [Int]
primos' xs = filter esPrimo xs

-- $> primos' [1..10]
-- [2,3,5,7]
-- $> primos' [16..33]
-- [17,19,23,29,31]

-- ejercicio 9 c
multiplicaPrimos' :: [Int] -> Int
multiplicaPrimos' xs = productoria (filter esPrimo xs)

-- $> multiplicaPrimos' [2,3,5,4,10]
-- 30
-- $> multiplicaPrimos' [21,2,11,2]
-- 44

-- ejercicio 10 a
primIgualesA :: Eq a => a -> [a] -> [a]
primIgualesA _ [] = []
primIgualesA n (x:xs)   | n == x = x : primIgualesA n xs
                        | otherwise = primIgualesA n []

-- $> primIgualesA 3 [3,3,4,1]
-- [3,3]
-- $> primIgualesA True [True,True,True,False,True]
-- [True,True,True]

--- ejercicio 10 b
primIgualesA' :: Eq a => a -> [a] -> [a]
primIgualesA' n xs = takeWhile (==n) xs

-- $> primIgualesA' 3 [3,3,4,1]
-- [3,3]
-- $> primIgualesA' True [True,True,True,False,True]
-- [True,True,True]

-- ejercicio 11 a
primIguales :: Eq a => [a] -> [a]
primIguales [] = []
primIguales [x] = [x]
primIguales (x:xs)	| x == head xs = x : primIguales xs
			        | otherwise = primIguales [x]
  
-- $> primIguales [4,3,3,4,1]
-- [4]
-- $> primIguales [False,False,False,True,False]
-- [False,False,False]

-- ejercicio 11 b
primIguales' :: Eq a => [a] -> [a]
primIguales' xs = primIgualesA' (head xs) xs

-- $> primIguales' [4,3,3,4,1]
-- [4]
-- $> primIguales' [False,False,False,True,False]
-- [False,False,False]

-- ejercicio 12*
cuantGen :: (b -> b -> b) -> b -> [a] -> (a -> b) -> b
cuantGen op z [] t = z
cuantGen op z (x:xs) t = t x `op` cuantGen op z xs t 

paratodo''' :: [a] -> (a -> Bool) -> Bool
paratodo''' xs t = cuantGen (&&) True xs t

-- $> paratodo''' [0, 0, 0] esCero
-- True
-- $> paratodo''' [0, 0, 1] esCero
-- False
-- $> paratodo''' [3, 0, 1] esPositivo
-- False

existe''' :: [a] -> (a -> Bool) -> Bool
existe''' xs t = cuantGen (||) False xs t

-- $> existe''' [2,6,0,1] esCero
-- True
-- $> existe''' [2, -1, -5] esPositivo
-- True
-- $> existe''' "HOLA" esVocal
-- False

sumatoria''' :: [a] -> (a -> Int) -> Int
sumatoria''' xs t = cuantGen (+) 0 xs t

-- $> sumatoria''' [2,-3,4,-5] valorAbsoluto
-- 14
-- $> sumatoria''' [2,4,2] factorial
-- 28

productoria''' :: [a] -> (a -> Int) -> Int
productoria''' xs t = cuantGen (*) 1 xs t

-- $> productoria''' [2,-3,4,-5] valorAbsoluto
-- 120
-- $> productoria''' [2,4,2] factorial
-- 96

-- ejercicio 13*
distanciaEdicion :: [Char] -> [Char] -> Int
distanciaEdicion xs [] = length xs 
distanciaEdicion [] ys = length ys
distanciaEdicion (x:xs) (y:ys)  | x == y = distanciaEdicion xs ys
                                | otherwise = 1 + distanciaEdicion xs ys

-- $> distanciaEdicion "aaaa" "bb"
-- 4
-- $> distanciaEdicion "aa" "a"
-- 1

-- ejercicio 14*
primQueCumplen :: [a] -> (a -> Bool) -> [a]
primQueCumplen xs t = takeWhile t xs

-- $> primQueCumplen ['a', 'e', 'i', 't', 'y'] esVocal
-- "aei"
-- $> primQueCumplen [2,3,-1,-5,4] esPositivo
-- [2,3]

-- ejercicio 15*
{-
a) f :: (a, b) -> ...
f (x , y) = ...
Esta bien tipado, la funcion esta definida usando tuplas y la funcion toma tuplas

b) f :: [(a, b)] -> ...
f (a , b) = ...
Esta mal tipado, la funcion esta definida usando lista de tuplas y la funcion solo toma tuplas

c) f :: [(a, b)] -> ...
f (x:xs) = ...
Esta bien tipado, la funcion esta definida usando lista de tuplas y la funcion toma lista de tuplas

d) f :: [(a, b)] -> ...
f ((x, y) : ((a, b) : xs)) = ...
Esta mal tipado, la funcion esta definida usando lista de tuplas y la funcion toma lista de tuplas
pero no cubre todos los casos

e) f :: [(Int, a)] -> ...
f [(0, a)] = ...
Esta bien tipado, la funcion esta definida usando lista de tuplas con tal vez distintos tipos y la
funcion toma lista de tuplas con 0 como Int usando pattern-matching y una variable de cualquier tipo,
cubre todos los casos

f ) f :: [(Int, a)] -> ...
f ((x, 1) : xs) = ...
Esta mal tipado, la funcion esta definida usando lista de tuplas con tal vez distintos tipos y la
funcion toma lista de tuplas con una variable de cualquier tipo pero tomando 1 como segundo elemento
de la tupla, siendo que esta definida la funcion con a, que si bien puede tomar el tipo de Int, no se
aprovecha el que pueda tomar cualquier tipo de variable

g) f :: (Int -> Int) -> Int -> ...
f a b = ...
Esta mal tipado, la funcion esta definida usando una funcion que toma Int y devuelve Int, y toma otro
Int, pero la funcion toma dos Int

h) f :: (Int -> Int) -> Int -> ...
f a 3 = ...
Esta mal tipado, la funcion esta definida usando una funcion que toma Int y devuelve Int, y toma otro
Int, pero la funcion toma dos Int, uno de ellos predefinido como 3

i) f :: (Int -> Int) -> Int -> ...
f 0 1 2 = ...
Esta mal tipado

-}

-- ejercicio 16*
{-
a) f :: (a, b) -> b
f (x, y) = y

b) f :: (a, b) -> c
f (x y) = z

c) f :: (a -> b) -> a -> b
f t x = t x

d) f :: (a -> b) -> [a] -> [b]
f t xs = t xs 
-}