package Request;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;


/* Esta clase se encarga de realizar efectivamente el pedido de feed al servidor de noticias via http-request*/

public abstract class LocalhostRequester {

	public static String getResponse(String urlServer){
		//Obtengo la response del servidor local
		String response = null;
        try {
            response = Files.readString(Path.of(urlServer));
        } catch (IOException e) {
            e.printStackTrace();
        }

		return response;
	}

}
