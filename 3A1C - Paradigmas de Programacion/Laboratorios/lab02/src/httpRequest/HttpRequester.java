package httpRequest;


/* Esta clase se encarga de realizar efectivamente el pedido de feed al servidor de noticias
 * Leer sobre como hacer una http request en java
 * https://www.baeldung.com/java-http-request
 * */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class HttpRequester {
	
	public String getFeed(String urlFeed){
		String feed = null;

		try {
            // Creamos el objeto URL y la conexión
            URL url = new URL(urlFeed);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            // Seteamos timeouts para conectar y para leer
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);

            // Ejecutamos el pedido
            int status = conn.getResponseCode();

            if (status != HttpURLConnection.HTTP_OK) {
                throw new IOException("Falla en la consulta HTTP. Status: " + status);
            }

            try (BufferedReader in = new BufferedReader(
                    new InputStreamReader(conn.getInputStream())
            ))
            {
                // Leemos la respuesta
                String inputLine;
                StringBuffer content = new StringBuffer();
                while ((inputLine = in.readLine()) != null) {
                    content.append(inputLine);
                }
                feed = content.toString();
            } finally {
                // Cerramos la conexion
                conn.disconnect();
            }

        } catch (MalformedURLException e) {
			System.out.println("ERROR: El URL dado no es válido");
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return feed;
	}

}
