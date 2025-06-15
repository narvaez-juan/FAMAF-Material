# Puntos Estrellas

### ¿Qué mecanismos permiten funcionar a nombres de dominio como http://中文.tw/ o https://💩.la? 

Los mecanismos que permiten funcionar nombres de dominios como los antes mencionados son las `URL encoding` (Uniform Resource Locator encoding). Tambien conocido como `percent-encoding`, es un método que convierte carácteres non-ASCII (tambien llamados caracteres especiales o caracteres reservados) de una cadena de texto a un '%HH' donde las H son números hexadecimales que corresponden a su valor en el formato de caracteres ASCII, de ahí el nombre del método, convirtiendo el string a un formato válido de URL.

Por otra parte, el estándar de codificación de caracteres mas comun en la web es el formato `UTF-8` (8-bit Unicode Transformation Format) el cual cuenta con una amplia gama de caracteres, permitiendonos trabajar con una gran variedad de URLs con distintos caracteres especiales y tanto con el encoding como el decoding de las URLs.

Para decodificar las URLs, se ignoran los caracteres no reservados, tales como las letras del alfabeto, y se traducen los caracteres especiales codificados, es decir aquellos caracteres que cuentan con '%' y números hexadecimales, a sus caracteres originales.