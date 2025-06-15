-- Sacar del esqueleto final!
{-# OPTIONS_GHC -Wno-unrecognised-pragmas #-}
{-# HLINT ignore "Use camelCase" #-}
{-# HLINT ignore "Eta reduce" #-}
module Interp where
import Graphics.Gloss
import Graphics.Gloss.Data.Vector
import qualified Graphics.Gloss.Data.Point.Arithmetic as V

import Dibujo

{-
import Graphics.Gloss
main = display (InWindow "Nice Window" (200, 200) (10, 10)) white (Circle 80)

data Display = InWindow String (Int, Int) (Int, Int) | FullScreen
-}

{-
data Picture = 
        Blank
      | Polygon Path
      | Line Path
      | Circle Float
      | Color Color Picture
      | Pictures [Picture]  
      | ...
-}

{-
type Point = (Float, Float)
type Vector = Point
type Path = [Point]
-}
-- Gloss provee el tipo Vector y Picture.
type ImagenFlotante = Vector -> Vector -> Vector -> Picture
type Interpretacion a = a -> ImagenFlotante

mitad :: Vector -> Vector
mitad = (0.5 V.*)

-- Interpretaciones de los constructores de Dibujo

--interpreta el operador de rotacion
interp_rotar :: ImagenFlotante -> ImagenFlotante
interp_rotar f origen ancho altura = 
  f (origen V.+ ancho) altura ( V.negate ancho) 

--interpreta el operador de rotacion 45
interp_rotar45 :: ImagenFlotante -> ImagenFlotante
interp_rotar45 f d w h = 
  f (d V.+ mitad (w V.+ h)) (mitad (w V.+ h)) (mitad (h V.- w))

--interpreta el operador de espejar
interp_espejar :: ImagenFlotante -> ImagenFlotante
interp_espejar f d w h = f (d V.+ w) (V.negate w) h

--interpreta el operador de apilar
interp_apilar :: Float -> Float -> ImagenFlotante -> ImagenFlotante -> ImagenFlotante
interp_apilar weightA weightB f1 f2 d w h = 
  pictures [f1 d1 w h1, f2 d w h2]
        where
          totalWeight = weightA + weightB
          proportion1 = weightA / totalWeight
          proportion2 = weightB / totalWeight
          h1 = proportion1 V.* h
          h2 = proportion2 V.* h
          d1 = d V.+ h2

--interpreta el operador de juntar
interp_juntar :: Float -> Float -> ImagenFlotante -> ImagenFlotante -> ImagenFlotante
interp_juntar weightA weightB f1 f2 d w h = 
  pictures [f1 d w1 h, f2 d2 w2 h]
        where
            pesoTotal = weightA + weightB 
            proporcion1 = weightA / pesoTotal
            proporcion2 = weightB / pesoTotal
            w1 = proporcion1 V.* w
            w2 = proporcion2 V.* w
            d2 = d V.+ w1

--interpreta el operador de encimar
interp_encimar :: ImagenFlotante -> ImagenFlotante -> ImagenFlotante
interp_encimar f1 f2 d w h = pictures[f1 d w h, f2 d w h]

--interpreta cualquier expresion del tipo Dibujo a
--utilizar foldDib 
interp :: Interpretacion a -> Dibujo a -> ImagenFlotante
interp interpAny dib = foldDib
    interpAny
    interp_rotar 
    interp_rotar45 
    interp_espejar 
    interp_apilar 
    interp_juntar 
    interp_encimar
    dib
