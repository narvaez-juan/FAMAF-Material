-- ejercicio 2
data TipoLadrillo = Ceramico | Hormigon | Tradicional
data UsoDeLadrillo = Pared | Techo
data MaterialViga = CementoHierro | Madera
data MarcaCemento = Minetti | LomaNegra

type Precio = Int
type Largo = Float

-- Ejercicio 2 a
data MaterialesConstruccion = Ladrillo TipoLadrillo UsoDeLadrillo Precio | Vigueta Largo MaterialViga Precio | Cemento MarcaCemento Precio

-- Ejercicio 2 b
cuantasViguetas :: [MaterialesConstruccion] -> MaterialViga -> Int
cuantasViguetas [] _ = 0
cuantasViguetas (Vigueta _ CementoHierro _:xs) CementoHierro = 1 + cuantasViguetas xs CementoHierro
cuantasViguetas (Vigueta _ Madera _:xs) Madera = 1 + cuantasViguetas xs Madera
cuantasViguetas (_:xs) material = cuantasViguetas xs material

{-
*Main> cuantasViguetas [Cemento Minetti 150, Cemento LomaNegra 120, Vigueta 15 CementoHierro 100] CementoHierro
1

*Main> cuantasViguetas [Vigueta 12 Madera 110, Cemento LomaNegra 120, Vigueta 15 CementoHierro 100, Vigueta 10 Madera 105] Madera
2

*Main> cuantasViguetas [Vigueta 12 Madera 110, Cemento LomaNegra 120, Vigueta 15 Madera 100, Vigueta 10 Madera 105] CementoHierro
0


-} 

-- funciones auxiliares para Ladrillo
mismoTipoLadrillo :: TipoLadrillo -> TipoLadrillo -> Bool
mismoTipoLadrillo Ceramico Ceramico = True
mismoTipoLadrillo Hormigon Hormigon = True
mismoTipoLadrillo Tradicional Tradicional = True
mismoTipoLadrillo  _ _ = False

mismoUsoLadrillo :: UsoDeLadrillo -> UsoDeLadrillo -> Bool
mismoUsoLadrillo Pared Pared = True
mismoUsoLadrillo Techo Techo = True
mismoUsoLadrillo _ _ = False

mismoLadrillo :: MaterialesConstruccion -> MaterialesConstruccion -> Bool
mismoLadrillo (Ladrillo t1 u1 _) (Ladrillo t2 u2 _) = (mismoTipoLadrillo t1 t2) && (mismoUsoLadrillo u1 u2)
mismoLadrillo _ _ = False

-- funciones auxiliares para Vigueta
mismoLargo :: Largo -> Largo -> Bool
mismoLargo l1 l2 = l1 == l2

mismoPrecio :: Precio -> Precio -> Bool
mismoPrecio p1 p2 = p1 == p2

mismaVigueta :: MaterialesConstruccion -> MaterialesConstruccion -> Bool
mismaVigueta (Vigueta l1 _ p1) (Vigueta l2 _ p2) = (mismoLargo l1 l2) && (mismoPrecio p1 p2) 
mismaVigueta _ _ = False

-- funciones auxiliares para Cemento
mismaMarca :: MarcaCemento -> MarcaCemento -> Bool
mismaMarca LomaNegra LomaNegra = True
mismaMarca Minetti Minetti = True
mismaMarca _ _ = False

mismoCemento :: MaterialesConstruccion -> MaterialesConstruccion -> Bool
mismoCemento (Cemento m1 _) (Cemento m2 _) = mismaMarca m1 m2
mismoCemento _ _ = False

-- ejercicio 2 c
instance Eq MaterialesConstruccion
    where
            m1 == m2 = (mismoLadrillo m1 m2) || (mismaVigueta m1 m2) || (mismoCemento m1 m2)

{-
*Main> (Ladrillo Hormigon Pared 160) == (Ladrillo Hormigon Pared 140)
True
*Main> (Ladrillo Hormigon Pared 160) == (Ladrillo Ceramico Pared 140)
False

*Main> (Vigueta 12 Madera 10) == (Vigueta 12 Madera 10)
True
*Main> (Vigueta 12 Madera 10) == (Vigueta 12 Madera 15)
False

*Main> (Cemento LomaNegra 150) == (Cemento LomaNegra 120)
True
*Main> (Cemento LomaNegra 150) == (Cemento Minetti 120)
False
-}

-- ejercicio 3 a
data Color = Blanco | Amarillo | Verde deriving Show

type Nombre = String
type Nota1 = Int
type Nota2 = Int
type NotaKata = Int

data NotasDelDOJO = NoHayMasAlumnos | EvolucionDelAlumno Nombre Color Nota1 Nota2 NotaKata NotasDelDOJO

-- ejercicio 3 b
pasaDeCinturon :: NotasDelDOJO -> String -> Bool
pasaDeCinturon NoHayMasAlumnos _ = False
pasaDeCinturon (EvolucionDelAlumno nombre1 Blanco n1 n2 n3 nts) nombre2 | nombre1 == nombre2 = ((n1 > 7) || (n2 > 7)) && (n3 >= 6)
    | otherwise = pasaDeCinturon nts nombre2
pasaDeCinturon (EvolucionDelAlumno nombre1 Amarillo n1 n2 n3 nts) nombre2 | nombre1 == nombre2 = ((n1 > 7) || (n2 > 7)) && (n3 >= 6)
    | otherwise = pasaDeCinturon nts nombre2
pasaDeCinturon (EvolucionDelAlumno nombre1 Verde n1 n2 n3 nts) nombre2 | nombre1 == nombre2 = ((n1 >= 7) && (n2 >= 7)) && (n3 >= 8)
    | otherwise = pasaDeCinturon nts nombre2

{-
*Main> pasaDeCinturon (EvolucionDelAlumno "Juan" Blanco 6 7 6 (EvolucionDelAlumno "Sol" Amarillo 7 6 6 (EvolucionDelAlumno "Pipa" Blanco 6 9 8 NoHayMasAlumnos))) "Juan"
False
*Main> pasaDeCinturon (EvolucionDelAlumno "Juan" Blanco 6 7 6 (EvolucionDelAlumno "Sol" Amarillo 7 6 6 (EvolucionDelAlumno "Pipa" Blanco 6 9 8 NoHayMasAlumnos))) "Pipa"
True
*Main> pasaDeCinturon (EvolucionDelAlumno "Juan" Blanco 6 7 6 (EvolucionDelAlumno "Lalo" Verde 7 7 9 (EvolucionDelAlumno "Pipa" Blanco 6 9 8 NoHayMasAlumnos))) "Lalo"
True
-}

-- ejercicio 3 c
devolverColorK2 :: NotasDelDOJO -> String -> Maybe Color
devolverColorK2 NoHayMasAlumnos _ = Nothing
devolverColorK2 (EvolucionDelAlumno nombre1 c _ _ _ nts) nombre2 | nombre1 == nombre2 = Just c
    | otherwise = devolverColorK2 nts nombre2

{-
*Main> devolverColorK2 (EvolucionDelAlumno "Juan" Blanco 6 7 6 (EvolucionDelAlumno "Lalo" Verde 7 7 9 (EvolucionDelAlumno "Pipa" Blanco 6 9 8 NoHayMasAlumnos))) "Juan"
Just Blanco
*Main> devolverColorK2 (EvolucionDelAlumno "Juan" Blanco 6 7 6 (EvolucionDelAlumno "Lalo" Verde 7 7 9 (EvolucionDelAlumno "Pipa" Blanco 6 9 8 NoHayMasAlumnos))) "Lalo"
Just Verde
-}
