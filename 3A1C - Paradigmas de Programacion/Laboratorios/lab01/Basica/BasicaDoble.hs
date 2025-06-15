module Basica.BasicaDoble where
import Dibujo
import Interp
import Basica.Comun

data FigGeometrica = Triangulo | Rectangulo | Circulo | Cuadrado | TrianguloVioleta
       deriving (Eq, Show)

ejemplo :: Dibujo FigGeometrica
ejemplo = Apilar 1 1 (Basica Triangulo) (Rotar (Basica TrianguloVioleta))

interpBas :: FigGeometrica -> ImagenFlotante
interpBas Triangulo = triangulo
interpBas TrianguloVioleta = trianguloVioleta