{-
-- DEFINICIONES 
Algoritmo: Secuencia finita de instrucciones precisas que resuelve problemas
Maquina de Turing (MT): fijar la nocion de algoritmo y lo que es computable, consta de:
    Cinta (hoja de papel infinita)
    Cabezal (lector/escritor)
    Operaciones, tales como leer, escribir, borrar, desplazarse

Maquinas de Turing -> Programacion Imperativa
Calculo Lambda     -> Programacion Funcional

Compilador: programa que transforma codigo escrito de un lenguaje a otro de mas bajo nivel, que pueda
entender la computadora.
Interprete: Programa que transforma codigo escrito de un lenguaje a otro, ejecutando tambien las
instrucciones que este codigo define.

HASKELL = Sistema de tipo estatico, funcionalmente puro, perezoso,, conciso, declarativo, polimorfico,
concurrente, tipado fuerte

-- DATOS
Tipos de datos: Bool, Int, Float, Char, String ([Char]), Tuple, List

Clase de tipos:
Num, incluye a los tipos numericos.
Ord, incluye a los tipos cuyos elementos tienen orden.
Eq, incluye a los tipos que soportan comparaciones por igualdad.
Enum, incluye a los tipos que tienen constantes finitas o infinitas.

-- TABLA DE PRECEDENCIA (mas arriba, mayor precedencia)
^                   potencia
*, /                producto y division
+, -                suma y resta
=, <, <=, >, >=     operadores de comparacion

-- FUNCION
Diremos que una funcion le "asigna" a los elementos de un conjunto, llamado dominio, elementos de otro
conjunto, llamado codominio. La notacion:

f : A -> B

indica que f es una funcion con dominio A y codominio B. La definicion de una funcion tiene la forma
f.x =. ⟨expresion que depende de x⟩donde f es el nombre de la funcion y x es/son la/s variable/s 
independiente/s.

Los tipos de los argumentos se listan primero, siguiendo el orden en el que seran llamados por la funcion,
y en ultimo lugar se coloca el tipo del resultado de evaluar la funcion.

-- FUNCION POR CASOS
Una definicion por casos de una funcion tendra la siguiente forma general:

f.x = ( . B0 -> f0
2 B1 -> f1
...
2 Bn -> fn
)
donde las Bi son expresiones de tipo booleano, llamadas guardas y las fi son expresiones del mismo tipo que
el resultado de f. Para un argumento dado el valor de la funcion se corresponde con la expresion cuya 
guarda es verdadera para ese argumento.
Al trabajar con expresiones booleanas se hace necesario incorporar a nuestro formalismo los operadores
^, ∨, ¬ que pueden ser utilizados para combinar dos formulas para obtener una nueva formula. En haskell
estos operadores se escriben && , || y not, respectivamente.

Pattern matching: Busca patrones con argumentos de valores constantes.

-- TUPLAS

-- LISTAS
Una lista (o secuencia) es una coleccion ordenada de valores, que deben ser todos del mismo tipo.

Denotamos a la lista vacia con [ ], al primer elemento de la lista con x y al resto de elementos con xs.

OPERADORES:

:   constructor     x:y:[] = [x,y]          return lista [x:xs]
#   cardinal        #xs = length xs         return # de elementos
!   indice          xs ! n = xs !! n        return indice, zero indexed
↑   tomar           xs ↑ n = take n xs      return lista de primeros n elementos      
↓   tirar           xs ↓ n = drop n xs      return lista sin primeros n elementos
++                  xs ++ ys = xs ++ ys     return lista xs seguido de lista ys
head xs devuelve el primer elemento de una lista 
tail xs devuelve una sublista de lista xs sin primer elemento

-- FUNCIONES RECURSIVAS
f :: [a] -> tipo de resultado
f [] = resultado de lista vacia                         -- caso base
f (x:xs) = resultado definido usando (f xs) y x         -- caso recursivo o caso inductivo

Tipos de funciones recursivas:
Fold:   Dada una lista, devuelve un valor resultante de combinar los elementos de la lista
Filter: Dada una lista, devuelve otra lista resultado de la primera, filtrada por condiciones
Map:    Dada una lista, devuelve otra lista resultado de la primera, aplicando funciones
Zip:    Dada una lista, devuelve otra lista de pares con elementos de la primera y segunda lista
Unzip:  Dada una lista de tuplas, devuelve una lista de alguna de las proyecciones de la tupla

-- INDUCCION
Hipotesis Inductiva
Caso base
Paso inductivo

-- NIVELES DE PRECEDENCIA 
 √ , (.)^n          Raiz cuadrada y Potenciacion
*, /                Multiplicacion y Division
max, min            Maximo y Minimo
+, -                Suma y Resta
=, <,>,<=,=>        Operadores de Comparacion
¬                   Negacion
∨,  ∧               Disyuncion y Conjuncion
⇒ , ⇐              Implicacion y Consecuencia
≡ , ≢               Equivalencia y Discrepancia

Los operadores ∧, ∨, ≡, ≢  son asociativos y conmutativos.

Las reglas de precedencia y asociatividad nos permiten eliminar paréntesis sin cambiar el significado.


-- FORMULAS FORM
Definamos el conjunto de formulas FORM  del lenguaje de logica proposicional:

True y False, pertenecen a FORM.
Sea PROP = {p,q,r,....} un conjunto de simbolos proposicionales, todos los elementos de PROP pertenecen a
FORM.
Si A pertenece a FORM, entonces (¬A) pertenece a FORM.
Si A y B pertenecen a FORM, entonces:
(A ∨ B) pertenece a FORM es la disyuncion.
(A ∧ B) pertenece a FORM es la conjuncion.
(A ⇒ B) pertenece a FORM es la implicacion.
(A ⇐ B) pertenece a FORM es la consecuencia.
(A ≡ B) pertenece a FORM es la equivalencia. 
(A ≢ B) pertenece a FORM es la discrepancia. 

-- VALIDEZ Y SATISFACIBILIDAD
Una formula es valida si es verdadera para todo valor de sus variables.
Una formula es satisfacible si es verdadera para algun o algunos valores de sus variables.
Una formula es no valida si es falsa para algun o algunos valores de sus variables. 
Una formula es insatisfacible (o no satisfacible) si es falsa para todo valor de sus variables. 


En una tabla de verdad, como determinamos si una formula es:

Valida: verificar que todas las filas de la tabla de verdad, se me hagan Verdaderas (V).
No va lida: verificar si al menos una fila hace la formula Falsa.
Satisfacible: verificar, si al menos una fila, me hace la formula V.
No satisfacible: ninguna fila resulta en V (todas en F).


-- CALCULO 
Un calculo es un mecanismo completamente sintactico que nos permite, analizando la forma de las formulas,
aplicar pasos de razonamiento para demostrar la validez de las mismas.

Mecanismo sintactico: porque no asigna valores de verdad a las variables.
Pasos de razonamiento: reglas de inferencia.


Si una formula es válida entonces es satisfacible. 
Si una formula es insatisfacible entonces no válida
Si  P es válida, ¬P es insatisfacible.
Si P es satisfacible, ¬P puede ser satisfacible o no.  


Calculo Proposicional
Consiste de un conjunto de axiomas y reglas de inferencia, a partir de los cuales podemos generar todos
los teoremas de la lógica proposicional.

TEOREMA
Todo lo que puedo demostrar es un teorema, y también es una fórmula válida. Esto se da gracias a que el
cálculo es correcto y completo:
Correcto: las fórmulas que se derivan usando los axiomas y reglas del cálculo, son válidas.
Completo: cualquier fórmula válida puede ser derivada en el cálculo a partir de los axiomas y las reglas.

DEMOSTRACION
Una demostración es una secuencia de fórmulas de la lógica proposicional, donde cada paso se justifica
con los axiomas del CP, las reglas del CP, y fórmulas que ya se han demostrado que son teoremas. El
objetivo es demostrar que una fórmula es un teorema, o equivalentemente (por corrección), que la fórmula
es válida.


Axiomas de la Equivalencia, Discrepancia y Negación 

A1 Asociatividad equivalencia:      
 ((P ≡ Q) ≡ R) ≡ (P ≡ (Q ≡ R)) 
A2 Conmutatividad equivalencia:         
 P ≡ Q ≡ Q ≡ P
A3 Neutro equivalencia:      
 (P ≡ True) ≡ P 
A4 Definición de Negación:    
 ¬(P ≡ Q) ≡ ¬P ≡ Q 
A5 Definición de False:  
 False ≡ ¬True   
A6 Definición de discrepancia:       
 P /≡ Q ≡ ¬(P ≡ Q)

Axiomas de Disyunción y Conjunción

A7 Asociatividad disyunción:
(P ∨ Q) ∨ R ≡ P ∨ (Q ∨ R) 
A8 Conmutatividad disyunción:
P ∨ Q ≡ Q ∨ P
A9 Idempotencia disyunción: 
P ∨ P ≡ P
A10 Distributividad disyunción con equivalencia: 
P ∨ (Q ≡ R) ≡ (P ∨ Q) ≡ (P ∨ R)
A11 Tercero excluido:  
P ∨ ¬P 
A12 Regla dorada: 
P ∧ Q ≡ P ≡ Q ≡ P ∨ Q

Axiomas de la implicacion

A13 Definición de implicación:
P ⇒ Q ≡ P ∨ Q ≡ Q 
A14 Definición de consecuencia:
P ⇐ Q ≡ P ∨ Q ≡ P


Sintaxis y Semántica en Lógica de Predicados

Cuantificador Universal:
<∀x : R.x : T.x >‘’Para todo valor de x, si R.x se cumple, entonces T.x se cumple”

Cuantificador Existencial:
<∃x : R.x : T.x>	‘’Existe al menos un valor de x, R.x se cumple, y T.x también se cumple”

A R.x lo llamamos Rango y a T.x lo llamamos término. 

Rango: el rango es un predicado Booleano (es decir, que se evalúa a V o F), que expresa una propiedad
sobre las variables cuantificadas. El Rango se encarga de filtrar algunos de los posibles valores posibles
de la variable cuantificada.

Término: el término es la propiedad que tienen que satisfacer aquellos elementos que hayan pasado el
filtro del rango, para que la fórmula sea verdadera.


Axiomas del Calculo de Predicado

A1 Intercambio entre rango y término de ∀:  <∀x : r.x : t.x> ≡ <∀x :: r.x ⇒ t.x> ≡ <∀x :: (¬r.x) ∨ (t.x)>

A2 Regla de término de ∀: <∀x :: t.x> ∧ <∀x :: s.x> ≡ <∀x :: t.x ∧ s.x>

A3 Distributividad de ∨ con ∀: Z ∨ <∀x :: t.x> ≡ <∀x :: Z ∨ t.x>,  si x no es una variable libre en Z

A4 Rango unitario de ∀: <∀x : x = A : t.x> ≡ t.A donde A representa una constante del universo

A5 Definición de ∃: <∃x : r.x : t.x> ≡ ¬ <∀x : r.x : ¬t.x>

A6 Intercambio de cuantificadores del ∀: <∀x :: <∀y :: t.x.y>> ≡ <∀y :: <∀x :: t.x.y>>
-}
