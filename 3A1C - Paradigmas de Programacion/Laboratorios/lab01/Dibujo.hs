{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Eta reduce" #-}
module Dibujo where

-- Definir el lenguaje via constructores de tipo
data Dibujo a = 
      Basica a
    | Rotar (Dibujo a)
    | Rotar45 (Dibujo a)  
    | Espejar (Dibujo a) 
    | Apilar Float Float (Dibujo a) (Dibujo a) 
    | Juntar Float Float (Dibujo a) (Dibujo a)
    | Encimar (Dibujo a) (Dibujo a)
    deriving (Eq, Show)


-- Composición n-veces de una función con sí misma.
comp :: (a -> a) -> Int -> a -> a
comp f n a  | n < 0     = error "El segundo argumento debe ser positivo"
            | n == 0    = a
            | otherwise = f (comp f (n-1) a) 


-- Rotaciones de múltiplos de 90.
r45 :: Dibujo a -> Dibujo a
r45 dib = Rotar45 dib

r90 :: Dibujo a -> Dibujo a
r90 dib = Rotar dib

r180 :: Dibujo a -> Dibujo a
r180 dib = comp r90 2 dib

r270 :: Dibujo a -> Dibujo a
r270 dib = comp r90 3 dib


-- Pone una figura junto a otra que es su espejo
(+|+) :: Dibujo a -> Dibujo a
(+|+) dib = Espejar dib


-- Pone una figura sobre la otra, ambas ocupan el mismo espacio.
(.-.) :: Dibujo a -> Dibujo a -> Dibujo a
(.-.) dib1 dib2 = Apilar 1 1 dib1 dib2


-- Pone una figura al lado de la otra, ambas ocupan el mismo espacio.
(///) :: Dibujo a -> Dibujo a -> Dibujo a
(///) dib1 dib2 = Juntar 1 1 dib1 dib2


-- Superpone una figura con otra.
(^^^) :: Dibujo a -> Dibujo a -> Dibujo a
(^^^) dib1 dib2 = Encimar dib1 dib2


-- Dadas cuatro dibujos las ubica en los cuatro cuadrantes.
cuarteto :: Dibujo a -> Dibujo a -> Dibujo a -> Dibujo a -> Dibujo a
cuarteto dib1 dib2 dib3 dib4 = (.-.) ((///) dib1 dib2) ((///) dib3 dib4)


-- Una dibujo repetido con las cuatro rotaciones, superpuestas.
encimar4 :: Dibujo a -> Dibujo a
encimar4 dib = (^^^) dib $ (^^^) (r90 dib) $ (^^^) (r180 dib) (r270 dib) 


-- Cuadrado con la misma figura rotada i * 90, para i ∈ {0, ..., 3}.
-- No confundir con encimar4!
ciclar :: Dibujo a -> Dibujo a
ciclar dib = cuarteto dib (r90 dib) (r180 dib) (r270 dib)


-- Transfomar un valor de tipo a como una Basica.
pureDib :: a -> Dibujo a
pureDib = Basica


-- map para nuestro lenguaje.
mapDib :: (a -> b) -> Dibujo a -> Dibujo b
mapDib f (Basica a) = Basica (f a)
mapDib f (Rotar d) = Rotar (mapDib f d)
mapDib f (Rotar45 d) = Rotar45 (mapDib f d)
mapDib f (Espejar d) = Espejar (mapDib f d)
mapDib f (Apilar x y d1 d2) = Apilar x y (mapDib f d1) (mapDib f d2)
mapDib f (Juntar x y d1 d2) = Juntar x y (mapDib f d1) (mapDib f d2)
mapDib f (Encimar d1 d2) = Encimar (mapDib f d1) (mapDib f d2)


-- Funcion de fold para Dibujos a
foldDib :: (a -> b) -> 
       (b -> b) -> 
       (b -> b) -> 
       (b -> b) ->
       (Float -> Float -> b -> b -> b) -> 
       (Float -> Float -> b -> b -> b) -> 
       (b -> b -> b) ->
       Dibujo a -> 
       b
foldDib base rotar rotar45 espejar apilar juntar encimar dib =
       case dib of
              Basica a -> base a
              Rotar d -> rotar (rec d)
              Rotar45 d -> rotar45 (rec d)
              Espejar d -> espejar (rec d)
              Apilar x y d1 d2 -> apilar x y (rec d1) (rec d2)
              Juntar x y d1 d2 -> juntar x y (rec d1) (rec d2)
              Encimar d1 d2 -> encimar (rec d1) (rec d2)
       where rec = foldDib base rotar rotar45 espejar apilar juntar encimar
