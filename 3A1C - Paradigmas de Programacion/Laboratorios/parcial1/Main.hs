module Main where
import Dibujo
import Interp
import Graphics.Gloss
import System.Environment

--Expresiones de Dibujo (Int,Int) para Testing Sintactico
dib1 = Basica (2,4)
dib2 = Basica (3,5)
dib3 = Rotar dib1
dib4 = Rotar dib2
dib5 = Apilar 1 1 dib1 dib2
dib6 = Encimar dib1 dib2
dib7 = Encimar dib4 (Rotar dib5)


main :: IO ()
main = do
    args <- getArgs
    let ej = head args

    case ej of
        "1a" -> do
            putStrLn "TESTING FUNCION TOBOOL:"
            if toBool dib1 == Basica True then putStrLn "Ok" else putStrLn "Fail"
            if toBool dib2 == Basica False then putStrLn "Ok" else putStrLn "Fail"
            if toBool dib3 == Rotar (Basica True) then putStrLn "Ok" else putStrLn "Fail"
            if toBool dib4 == Rotar (Basica False) then putStrLn "Ok" else putStrLn "Fail"
            if toBool dib5 == Apilar 1 1 (Basica True) (Basica False) then putStrLn "Ok" else putStrLn "Fail"
            if toBool dib6 == Encimar (Basica True) (Basica False) then putStrLn "Ok" else putStrLn "Fail"

        "1b" -> do
            putStrLn "TESTING FUNCION TOBOOL2:"
            if toBool2 dib1 == Basica True then putStrLn "Ok" else putStrLn "Fail"
            if toBool2 dib2 == Basica False then putStrLn "Ok" else putStrLn "Fail"
            if toBool2 dib3 == Rotar (Basica True) then putStrLn "Ok" else putStrLn "Fail"
            if toBool2 dib4 == Rotar (Basica False) then putStrLn "Ok" else putStrLn "Fail"
            if toBool2 dib5 == Apilar 1 1 (Basica True) (Basica False) then putStrLn "Ok" else putStrLn "Fail"
            if toBool2 dib6 == Encimar (Basica True) (Basica False) then putStrLn "Ok" else putStrLn "Fail"

        "1c" -> do
            putStrLn "TESTING FUNCION PROFUNDIDAD:"
            if profundidad dib1 == 1 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad dib3 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad dib5 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad dib6 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad dib7 == 4 then putStrLn "Ok" else putStrLn "Fail"

        "1d" -> do
            putStrLn "TESTING FUNCION PROFUNDIDAD2:"
            if profundidad2 dib1 == 1 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad2 dib3 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad2 dib5 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad2 dib6 == 2 then putStrLn "Ok" else putStrLn "Fail"
            if profundidad2 dib7 == 4 then putStrLn "Ok" else putStrLn "Fail"

        "2a" -> do
            putStrLn "TESTING FUNCION INTERP_BASICA:"
            let win = InWindow "Paradigmas 2025 - Parcial 1" (1000,1000) (0,0)
            display win white ((interp_apilar 1 1 (interp_basica True) (interp_basica False)) (0,0) (100,0) (0,100))  

        "2b" -> do
            putStrLn "TESTING FUNCION INTERP:"
            let win = InWindow "Paradigmas 2025 - Parcial 1" (1000,1000) (0,0)
                dib = Apilar 1 1 (Rotar (Basica True)) (Basica False) 
            display win white (interp dib (0,0) (100,0) (0,100))  

        "3" -> do
            putStrLn "TESTING OPERADOR RESIZE:"
            let win = InWindow "Paradigmas 2025 - Parcial 1" (1000,1000) (0,0)
                dib = Encimar (Encimar (Resize 1 (Basica True)) (Resize 2 (Basica True))) (Resize 3 (Basica True))        
            display win white (interp dib (0,0) (100,0) (0,100))

        otherwise -> putStrLn "Numero de Ejercicio Incorrecto"

