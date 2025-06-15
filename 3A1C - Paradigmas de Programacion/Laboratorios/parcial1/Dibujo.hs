module Dibujo where

-- Definicion  del lenguaje
data Dibujo a = Basica a
              | Rotar (Dibujo a)
              | Apilar Int Int (Dibujo a) (Dibujo a)
              | Encimar (Dibujo a) (Dibujo a)
              | Resize Float (Dibujo a) --resize
              deriving(Show, Eq)


-- Funcion Map (de Basicas) para nuestro sub-lenguaje.
mapDib :: (a -> b) -> Dibujo a -> Dibujo b
mapDib f (Basica x) = Basica (f x)
mapDib f (Rotar d1) = Rotar (mapDib f d1)
mapDib f (Apilar n m d1 d2) = Apilar n m (mapDib f d1) (mapDib f d2)
mapDib f (Encimar d1 d2) = Encimar (mapDib f d1) (mapDib f d2)
mapDib f (Resize n d) = Resize n (mapDib f d) --resize


-- Funcion Fold para nuestro sub-lenguaje.
foldDib :: (a -> b) -> (b -> b) ->
       (Int -> Int -> b -> b -> b) ->
       (b -> b -> b) ->
       (Float -> b -> b) -> --resize
       Dibujo a -> b

foldDib sB sR sA sEn sRe d =
    let foldDibRecursiva = foldDib sB sR sA sEn sRe
    in case d of
        Basica x -> sB x
        Rotar d -> sR $ foldDibRecursiva d
        Apilar m n d1 d2 -> sA m n (foldDibRecursiva d1) (foldDibRecursiva d2)
        Encimar d1 d2 -> sEn (foldDibRecursiva d1) (foldDibRecursiva d2)
        Resize n d -> sRe n (foldDibRecursiva d)


-- Funcion auxiliar para EJERCICIO 1-a, 1-b
esMultiplo :: (Int, Int) -> Bool
esMultiplo (x,y)
    | mod x y == 0 = True
    | mod y x == 0 = True
    | otherwise = False

--(EJERCICIO 1-a)
toBool:: Dibujo (Int,Int) -> Dibujo Bool
toBool (Basica (x,y))
    | esMultiplo (x,y) = Basica (True)
    | otherwise = Basica (False)
toBool (Rotar dib) = Rotar (toBool dib)
toBool (Apilar x y dib1 dib2) = Apilar x y (toBool dib1) (toBool dib2)
toBool (Encimar dib1 dib2) = Encimar (toBool dib1) (toBool dib2)

--(EJERCICIO 1-b)
toBool2:: Dibujo (Int,Int) -> Dibujo Bool
toBool2 (Basica (x, y)) = mapDib esMultiplo (Basica (x,y))
toBool2 dib = mapDib esMultiplo dib

--(EJERCICIO 1-c)
profundidad:: Dibujo a -> Int
profundidad (Basica x) = 1
profundidad (Rotar dib) = 1 + profundidad dib
profundidad (Apilar _ _ dib1 dib2) = 1 + max (profundidad dib1) (profundidad dib2)
profundidad (Encimar dib1 dib2) = 1 + max (profundidad dib1) (profundidad dib2)
profundidad (Resize _ dib) = 1 + profundidad dib

--(EJERCICIO 1-d)
profundidad2:: Dibujo a -> Int
profundidad2 dib = foldDib
    (const 1)
    (\n -> 1 + n)
    (\_ _ d1 d2 -> 1 + max (d1) (d2))
    (\d1 d2 -> 1 + max (d1) (d2))
    (\r d -> 1 + d)
    dib

