{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Eta reduce" #-}
{-# HLINT ignore "Avoid lambda" #-}
{-# HLINT ignore "Avoid lambda using `infix`" #-}
module Pred where

import Dibujo

type Pred a = a -> Bool

--Para la definiciones de la funciones de este modulo, no pueden utilizar
--pattern-matching, sino alto orden a traves de la funcion foldDib, mapDib 

-- Dado un predicado sobre básicas, cambiar todas las que satisfacen
-- el predicado por el resultado de llamar a la función indicada por el
-- segundo argumento con dicha figura.
-- Por ejemplo, `cambiar (== Triangulo) (\x -> Rotar (Basica x))` rota
-- todos los triángulos.
cambiar :: Pred a -> (a -> Dibujo a) -> Dibujo a -> Dibujo a
cambiar pred f = foldDib
    (\x -> if pred x then f x else Basica x)
    r90
    r45
    (+|+)
    apilar 
    juntar
    (^^^)
    where
        apilar _ _ = (.-.) 
        juntar _ _ = (///)

-- Alguna básica satisface el predicado.
anyDib :: Pred a -> Dibujo a -> Bool
anyDib pred dib = foldDib 
    (pred)
    (\x -> x)
    (\x -> x)
    (\x -> x)
    (\_ _ x y -> (x) || (y))
    (\_ _ x y -> (x) || (y))
    (\x y -> (x) || (y))
    dib

-- Todas las básicas satisfacen el predicado.
allDib :: Pred a -> Dibujo a -> Bool
allDib pred dib = foldDib 
    (pred)
    (\x -> x)
    (\x -> x)
    (\x -> x)
    (\_ _ x y -> (x) && (y))
    (\_ _ x y -> (x) && (y))
    (\x y -> (x) && (y))
    dib

-- Hay 4 rotaciones seguidas.
esRot360 :: Pred (Dibujo a)
esRot360 dib = foldDib
    (const 0)
    (\n -> n + 1)
    (\x -> assignXOrZero 4 [x])
    (\x -> assignXOrZero 4 [x])
    (\_ _ x y -> assignXOrZero 4 [x, y])
    (\_ _ x y -> assignXOrZero 4 [x, y])
    (\x y -> assignXOrZero 4 [x, y])
    dib >= 4

-- Hay 2 espejados seguidos.
assignXOrZero :: Int -> [Int] -> Int
assignXOrZero x [] = 0
assignXOrZero  x (n:ns) = if n >= x then x else assignXOrZero x ns

esFlip2 :: Pred (Dibujo a)
esFlip2 dib = foldDib (const 0)
                    (\x -> assignXOrZero 2 [x])
                    (\x -> assignXOrZero 2 [x])
                    (\n -> n+1)
                    (\_ _ x y -> assignXOrZero 2 [x,y])
                    (\_ _ x y -> assignXOrZero 2 [x,y])
                    (\ x y -> assignXOrZero 2 [x,y])
                    dib >= 2

data Superfluo = RotacionSuperflua | FlipSuperfluo
                deriving (Eq, Show)

-- Chequea si el dibujo tiene una rotacion superflua
errorRotacion :: Dibujo a -> [Superfluo]
errorRotacion dib = case dib of
    Basica dib -> []
    Rotar(Rotar(Rotar(Rotar dib))) -> RotacionSuperflua : errorRotacion dib
    Rotar dib -> errorRotacion dib
    Rotar45 dib -> errorRotacion dib
    Espejar dib -> errorRotacion dib
    Apilar _ _ dib1 dib2 -> errorRotacion dib1 ++ errorRotacion dib2
    Juntar _ _ dib1 dib2 -> errorRotacion dib1 ++ errorRotacion dib2
    Encimar dib1 dib2 -> errorRotacion dib1 ++ errorRotacion dib2

{-
errorRotacion = foldDib
    (const [])                           -- Basica
    rotar                               -- Rotar
    (\x -> x)                           -- Rotar45
    (\x -> x)                           -- Espejar
    (\_ _ x y -> x ++ y)                -- Apilar
    (\_ _ x y -> x ++ y)                -- Juntar
    (\x y -> x ++ y)                    -- Encimar
    where
        rotar (RotacionSuperflua : xs) = RotacionSuperflua : xs
        rotar (RotacionSuperflua:_:_:_:xs) = RotacionSuperflua : xs
        rotar xs = if length xs >= 3 then RotacionSuperflua : xs else xs
-}


-- Chequea si el dibujo tiene un flip superfluo
errorFlip :: Dibujo a -> [Superfluo]
errorFlip dib = case dib of
    Basica dib -> []
    Espejar(Espejar dib) -> FlipSuperfluo : errorFlip dib
    Rotar dib -> errorFlip dib
    Rotar45 dib -> errorFlip dib
    Espejar dib -> errorFlip dib
    Apilar _ _ dib1 dib2 -> errorFlip dib1 ++ errorFlip dib2
    Juntar _ _ dib1 dib2 -> errorFlip dib1 ++ errorFlip dib2
    Encimar dib1 dib2 -> errorFlip dib1 ++ errorFlip dib2

---Aplica todos los chequeos y acumula todos los errores, y
-- sólo devuelve la figura si no hubo ningún error.
checkSuperfluo :: Dibujo a -> Either [Superfluo] (Dibujo a)
checkSuperfluo dib = let errores = errorRotacion dib ++ errorFlip dib
                        in if errores /= []
                        then Left errores
                        else Right dib
