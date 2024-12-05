-- ejercicio 1 a
data Carrera = Matematica | Fisica | Computacion | Astronomia

-- ejercicio 1 b
titulo :: Carrera -> String
titulo Matematica = "Licenciatura en Matematica"
titulo Fisica = "Licenciatura en Fisica"
titulo Computacion = "Licenciatura en Ciencias de la Computacion"
titulo Astronomia = "Licenciatura en Astronomia"

-- $> titulo Fisica
-- "Licenciatura en Fisica"
-- $> titulo Computacion
-- "Licenciatura en Ciencias de la Computacion"


-- ejercicio 1 c
data NotaBasica = Do | Re | Mi | Fa | Sol | La | Si deriving (Eq, Ord, Show)

-- ejercicio 1 d
cifradoAmericano :: NotaBasica -> Char
cifradoAmericano Do = 'C'
cifradoAmericano Re = 'D'
cifradoAmericano Mi = 'E'
cifradoAmericano Fa = 'F'
cifradoAmericano Sol = 'G'
cifradoAmericano La = 'A'
cifradoAmericano Si = 'B'

-- $> cifradoAmericano Do
-- 'C'
-- $> cifradoAmericano Sol
-- 'G'



-- ejercicio 2 a
-- data NotaBasica = Do | Re | Mi | Fa | Sol | La | Si deriving (Eq, Ord, Show)

-- ejercicio 3 a
minimoElemento :: (Ord a) => [a] -> a
minimoElemento [x] = x
minimoElemento (x:xs) = min x (minimoElemento xs)

-- ejercicio 3 b
minimoElemento' :: (Ord a, Bounded a) => [a] -> a
minimoElemento' []		= maxBound
minimoElemento' [x]		= x
minimoElemento' (x:xs)	= min x (minimoElemento' xs)

-- ejercicio 3 c
-- $> minimoElemento [Fa, La, Sol, Re, Fa]
-- Re
-- $> minimoElemento' [Fa, La, Sol, Re, Fa]
-- Re



-- ejercicio 4 a

-- Tipos algebraicos sin parametros (aka enumerados)
data Zona = Arco | Defensa | Mediocampo | Delantera deriving Show
data TipoReves = DosManos | UnaMano deriving Show
data Modalidad = Carretera | Pista | Monte | BMX deriving Show
data PiernaHabil = Izquierda | Derecha deriving Show

-- Sinonimos de tipo
type Altura = Int
type NumCamiseta = Int
type ManoHabil = PiernaHabil

-- Deportista es un tipo algebraico con constructores parametricos
data Deportista = Ajedrecista
        | Ciclista Modalidad
        | Velocista Altura
        | Tenista TipoReves ManoHabil Altura
        | Futbolista Zona NumCamiseta PiernaHabil Altura deriving Show

-- ejercicio 4 b
-- El tipo de constructor ciclista es Deportista

-- ejercicio 4 c
contar_velocistas :: [Deportista] -> Int
contar_velocistas [] = 0
contar_velocistas (Velocista a:xs) = 1 + contar_velocistas xs
contar_velocistas (Ajedrecista:xs) = 0 + contar_velocistas xs
contar_velocistas (Ciclista a:xs) = 0 + contar_velocistas xs
contar_velocistas (Tenista a b c:xs) = 0 + contar_velocistas xs
contar_velocistas (Futbolista a b c d:xs) = 0 + contar_velocistas xs

-- $> contar_velocistas [Tenista DosManos Derecha 185, Ajedrecista, Velocista 180]
-- 1
-- $> contar_velocistas [Velocista 180, Futbolista Arco 1 Izquierda 182, Velocista 176]   
-- 2


-- ejercicio 4 d
contar_futbolistas :: [Deportista] -> Zona -> Int
contar_futbolistas [] z = 0
contar_futbolistas (Futbolista Arco _ _ _:xs) Arco = 1 + contar_futbolistas xs Arco
contar_futbolistas (Futbolista Defensa _ _ _:xs) Defensa = 1 + contar_futbolistas xs Defensa
contar_futbolistas (Futbolista Mediocampo _ _ _:xs) Mediocampo = 1 + contar_futbolistas xs Mediocampo
contar_futbolistas (Futbolista Delantera _ _ _:xs) Delantera = 1 + contar_futbolistas xs Delantera
contar_futbolistas (Futbolista _ _ _ _:xs) z = 0 + contar_futbolistas xs z
contar_futbolistas (Velocista _:xs) z = 0 + contar_futbolistas xs z
contar_futbolistas (Ajedrecista:xs) z = 0 + contar_futbolistas xs z
contar_futbolistas (Ciclista _:xs) z = 0 + contar_futbolistas xs z
contar_futbolistas (Tenista _ _ _:xs) z = 0 + contar_futbolistas xs z

-- $> contar_futbolistas [Velocista 180, Futbolista Arco 1 Izquierda 182, Velocista 176] Arco  
-- 1
-- $> contar_futbolistas [Velocista 180, Futbolista Arco 1 Izquierda 182, Velocista 176] Delantera
-- 0


-- ejercicio 4 e
esFutbolistaEn :: Zona -> Deportista -> Bool
esFutbolistaEn Arco (Futbolista Arco _ _ _) = True
esFutbolistaEn Defensa (Futbolista Defensa _ _ _) = True
esFutbolistaEn Mediocampo (Futbolista Mediocampo _ _ _) = True
esFutbolistaEn Delantera (Futbolista Delantera _ _ _) = True
esFutbolistaEn z _ = False

contar_futbolistas' :: [Deportista] -> Zona -> Int
contar_futbolistas' [] z = 0
contar_futbolistas' xs z = length (filter (esFutbolistaEn z) xs)

-- $> contar_futbolistas' [Velocista 180, Futbolista Arco 1 Izquierda 182, Velocista 176] Arco  
-- 1
-- $> contar_futbolistas' [Velocista 180, Futbolista Arco 1 Izquierda 182, Velocista 176] Delantera
-- 0



-- ejercicio 5 a
sonidoNatural :: NotaBasica -> Int
sonidoNatural Do = 0
sonidoNatural Re = 2
sonidoNatural Mi = 4
sonidoNatural Fa = 5
sonidoNatural Sol = 7
sonidoNatural La = 9
sonidoNatural Si = 11

-- $> sonidoNatural Do
-- 0
-- $> sonidoNatural Sol
-- 7


-- ejercicio 5 b
data Alteracion = Bemol | Natural | Sostenido

-- ejercicio 5 c
data NotaMusical = Nota NotaBasica Alteracion

-- ejercicio 5 d
sonidoCromatico :: NotaMusical -> Int
sonidoCromatico (Nota n Bemol) = (sonidoNatural n) - 1
sonidoCromatico (Nota n Natural) = (sonidoNatural n)
sonidoCromatico (Nota n Sostenido) = (sonidoNatural n) + 1

-- sonidoCromatico (Nota Do Bemol)
-- -1
-- sonidoCromatico (Nota Si Sostenido)
-- 12


-- ejercicio 5 e
instance Eq NotaMusical
    where 
            n1 == n2 = sonidoCromatico n1 == sonidoCromatico n2
    
-- ejercicio 5 f
instance Ord NotaMusical
    where
            n1 >= n2 = sonidoCromatico n1 >= sonidoCromatico n2
            n1 <= n2 = sonidoCromatico n1 <= sonidoCromatico n2



-- ejercicio 6 a
primerElemento :: [a] -> Maybe a
primerElemento [] = Nothing
primerElemento xs = Just (head xs)

-- $> primerElemento [Sol, La, Si, Do]
-- Just Sol
-- $> primerElemento "hola"
-- Just 'h'

-- ejercicio 7
data Cola = VaciaC | Encolada Deportista Cola deriving Show

-- ejercicio 7 a 1
atender :: Cola -> Maybe Cola
atender VaciaC = Nothing
atender (Encolada d c) = Just c

-- atender VaciaC
-- Nothing
-- atender (Encolada Ajedrecista (Encolada (Velocista 176) VaciaC))
-- Just (Encolada (Velocista 176) VaciaC)


-- ejercicio 7 a 2
encolar :: Deportista -> Cola -> Cola
encolar d VaciaC = Encolada d VaciaC
encolar d c = Encolada d c

-- $> encolar Ajedrecista VaciaC
-- Encolada Ajedrecista VaciaC
-- $> encolar Ajedrecista (Encolada (Velocista 180) VaciaC)
-- Encolada Ajedrecista (Encolada (Velocista 180) VaciaC)
-- $> encolar (Futbolista Arco 1 Derecha 180) (Encolada Ajedrecista (Encolada (Velocista 180) VaciaC))
-- Encolada (Futbolista Arco 1 Derecha 180) (Encolada Ajedrecista (Encolada (Velocista 180) VaciaC))


-- ejercicio 7 a 3
busca :: Cola -> Zona -> Maybe Deportista
busca VaciaC z = Nothing
busca (Encolada (Futbolista Arco i j k) c) Arco = Just (Futbolista Arco i j k)
busca (Encolada (Futbolista Defensa i j k) c) Defensa = Just (Futbolista Arco i j k)
busca (Encolada (Futbolista Mediocampo i j k) c) Mediocampo = Just (Futbolista Arco i j k)
busca (Encolada (Futbolista Delantera i j k) c) Delantera = Just (Futbolista Arco i j k)
busca (Encolada _ cs) z = busca cs z

-- $> busca (Encolada Ajedrecista VaciaC) Defensa
-- Nothing
-- $> busca (Encolada Ajedrecista (Encolada (Futbolista Arco 1 Derecha 180) VaciaC)) Arco
-- Just (Futbolista Arco 1 Derecha 180)
-- $> busca (Encolada Ajedrecista (Encolada (Futbolista Arco 1 Derecha 180) (Encolada (Futbolista Arco 23 Izquierda 178) VaciaC))) Arco
-- Just (Futbolista Arco 1 Derecha 180)


-- ejercicio 7 b
-- Se parece al tipo lista



-- ejercicio 8
data ListaAsoc a b = Vacia | Nodo a b (ListaAsoc a b) deriving Show

type Diccionario = ListaAsoc String String
type Padron = ListaAsoc Int String

-- ejercicio 8 a
type GuiaTelefonica = ListaAsoc String Int

-- ejercicio 8 b 1
la_long :: ListaAsoc a b -> Int
la_long Vacia = 0
la_long (Nodo a b ls) = 1 + la_long ls

-- la_long Vacia
-- 0
-- $> la_long (Nodo False 2 (Nodo True 3 (Vacia)))
-- 2


-- ejercicio 8 b 2
la_concat :: ListaAsoc a b -> ListaAsoc a b -> ListaAsoc a b
la_concat Vacia Vacia = Vacia
la_concat ls_a Vacia = ls_a
la_concat Vacia ls_b = ls_b
la_concat (Nodo a1 b1 ls_a) ls_b = Nodo a1 b1 (la_concat ls_a ls_b)

-- $> la_concat (Nodo 2 3 (Nodo 100 123 (Vacia))) (Nodo 5 7 (Nodo 101 102 (Vacia)))
-- Nodo 2 3 (Nodo 100 123 (Nodo 5 7 (Nodo 101 102 Vacia)))
-- $> la_concat (Nodo True 'a' (Nodo False 'b' (Nodo True 'c' Vacia))) (Nodo True 'x' Vacia)
-- Nodo True 'a' (Nodo False 'b' (Nodo True 'c' (Nodo True 'x' Vacia)))


-- ejercicio 8 b 3
la_agregar :: (Eq a) => ListaAsoc a b -> a -> b -> ListaAsoc a b
la_agregar Vacia a b = Nodo a b Vacia
la_agregar (Nodo a b ls) n m    | a == n    = Nodo a m ls
                                | otherwise = Nodo a b (la_agregar ls n m)

-- $> la_agregar (Nodo 1 2 (Nodo 8 3 (Vacia))) 3 4
-- Nodo 1 2 (Nodo 8 3 (Nodo 3 4 Vacia))
-- $> la_agregar (Nodo 1 2 (Nodo 8 3 (Vacia))) 8 5
-- Nodo 1 2 (Nodo 8 5 Vacia)


-- ejercicio 8 b 4
la_pares :: ListaAsoc a b -> [(a, b)]
la_pares Vacia = []
la_pares (Nodo a b ls) = (a, b) : la_pares ls

-- $> la_pares (Nodo 1 'a' (Nodo 2 'x' (Nodo 4 'z' Vacia)))
-- [(1,'a'),(2,'x'),(4,'z')]
-- $> la_pares (Nodo True [] (Nodo False [1] (Nodo False [2,3] Vacia)))
-- [(True,[]),(False,[1]),(False,[2,3])]


-- ejercicio 8 b 5
la_busca :: (Eq a) => ListaAsoc a b -> a -> Maybe b
la_busca Vacia _ = Nothing
la_busca (Nodo a b ls) x    | a == x = Just b
                            | otherwise = la_busca ls x

-- $> la_busca (Nodo False 4 (Nodo False 7 (Vacia))) True
-- Nothing
-- $> la_busca (Nodo False 4 (Nodo False 7 (Nodo True 1 Vacia))) True
-- Just 1


-- ejercicio 8 b 6
la_borra :: (Eq a) => a -> ListaAsoc a b -> ListaAsoc a b
la_borra _ Vacia = Vacia
la_borra n (Nodo a b ls)    | n == a    = xl
                        	| otherwise = Nodo a b (la_borra n ls)

-- $> la_borra 9 (Nodo 1 2 (Nodo 8 3 (Vacia))) 
-- Nodo 1 2 (Nodo 8 3 Vacia)
-- $> la_borra 1 (Nodo 1 2 (Nodo 8 3 (Vacia))) 
-- Nodo 8 3 Vacia



-- ejercicio 9
data Arbol a = Hoja | Rama (Arbol a) a (Arbol a)
type Prefijos = Arbol String

-- ejercicio 9 a
a_long :: Arbol a -> Int
a_long Hoja = 0
a_long (Rama a b c) = 1 + (a_long a) + (a_long c)

-- $> a_long (Rama (Rama (Hoja) 9 (Hoja)) 1 Hoja)
-- 2
-- $> a_long (Rama (Rama (Hoja) 9 (Hoja)) 1 (Rama (Rama (Rama Hoja 2 Hoja) 7 Hoja) 8 (Rama Hoja 2 Hoja)))
-- 6


-- ejercicio 9 b
a_hojas :: Arbol a -> Int
a_hojas Hoja = 1
a_hojas (Rama a b c) = (a_hojas a) + (a_hojas c)

-- $> a_hojas (Rama (Rama (Hoja) 9 (Hoja)) 1 Hoja)
-- 1
-- $> a_hojas (Rama (Rama (Hoja) 9 (Hoja)) 1 (Rama (Rama (Rama Hoja 2 Hoja) 7 Hoja) 8 (Rama Hoja 2 Hoja)))
-- 3


-- ejercicio 9 c
a_inc :: Num a => Arbol a -> Arbol a
a_inc Hoja = Hoja
a_inc (Rama a b c) = Rama (a_inc a) (b + 1) (a_inc c)

-- $> a_inc (Rama (Rama (Hoja) 9 (Hoja)) 1 (Rama (Rama (Rama Hoja 2 Hoja) 7 Hoja) 8 (Rama Hoja 2 Hoja)))
-- Rama (Rama Hoja 10 Hoja) 2 (Rama (Rama (Rama Hoja 3 Hoja) 8 Hoja) 9 (Rama Hoja 3 Hoja))
-- $> a_inc (Rama (Rama (Hoja) 9 (Hoja)) 1 Hoja)
-- Rama (Rama Hoja 10 Hoja) 2 Hoja


-- ejercicio 9 d
a_map :: (a -> b) -> Arbol a -> Arbol b
a_map f Hoja = Hoja
a_map f (Rama a b c) = Rama (a_map f a) (f b) (a_map f c)

-- $> a_map (*7) (Rama (Rama (Hoja) 9 (Hoja)) 1 Hoja)
-- Rama (Rama Hoja 63 Hoja) 7 Hoja
-- $> a_map (/5) (Rama (Rama (Hoja) 9 (Hoja)) 1 Hoja)
-- Rama (Rama Hoja 1.8 Hoja) 0.2 Hoja



-- ejercicio 10 a
data ABB a = VacioABB | RamaABB (ABB a) a (ABB a)
	deriving (Show)

-- ejercicio 10 b
insertarABB :: Ord a => a -> ABB a -> ABB a
insertarABB x VacioABB = RamaABB VacioABB x VacioABB
insertarABB x (RamaABB ri n rd)	| x <= n = RamaABB (insertarABB x ri) n rd
								| otherwise = RamaABB ri n (insertarABB x rd)

-- $> insertarABB 4 (RamaABB VacioABB 7 VacioABB)
-- RamaABB (RamaABB VacioABB 4 VacioABB) 7 VacioABB
-- $> insertarABB 2 (RamaABB (RamaABB VacioABB 4 (RamaABB (RamaABB VacioABB 1 VacioABB)
--    3 VacioABB)) 7 VacioABB)
-- RamaABB (RamaABB (RamaABB VacioABB 2 VacioABB) 4 (RamaABB (RamaABB VacioABB 1 VacioABB)
-- 3 VacioABB)) 7 VacioABB



-- ejercicio 10 c
buscarABB :: Eq a => a -> ABB a -> Bool
buscarABB _ VacioABB = False
buscarABB x (RamaABB ri n rd)	| x == n = True
								| otherwise = buscarABB x ri || buscarABB x rd

-- $> buscarEnArbol 2 (RamaABB (RamaABB VacioABB 4 (RamaABB (RamaABB VacioABB 1 VacioABB)
--    3 VacioABB)) 7 VacioABB)
-- False
-- $> buscarEnArbol 7 (RamaABB (RamaABB VacioABB 4 (RamaABB (RamaABB VacioABB 1 VacioABB)
--    3 VacioABB)) 7 VacioABB)
-- True


-- ejercicio 10 d
mayorQueTodos :: Ord a => a -> ABB a -> Bool
mayorQueTodos _ VacioABB = True
mayorQueTodos x (RamaABB ri n rd)
  | x > n = mayorQueTodos x ri && mayorQueTodos x rd
  | otherwise = False

menorQueTodos :: Ord a => a -> ABB a -> Bool
menorQueTodos _ VacioABB = True
menorQueTodos x (RamaABB ri n rd)
  | x < n = menorQueTodos x ri && menorQueTodos x rd
  | otherwise = False

verificarABB :: Ord a => ABB a -> Bool
verificarABB VacioABB = True
verificarABB (RamaABB ri n rd) = mayorQueTodos n ri && menorQueTodos n rd

-- $> verificarABB RamaABB (RamaABB VacioABB 10 VacioABB) 2 (RamaABB VacioABB 11 VacioABB) 
-- False
