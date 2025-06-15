package Request;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;


/* Esta clase se encarga de realizar efectivamente el pedido de feed al servidor de noticias via http-request*/

public abstract class HttpRequester {

	public static String getResponse(String urlServer){
		//Obtengo la response del servidor via http-request
		String response = null;
		try{
			URL url = new URL(urlServer);
			HttpURLConnection con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
	
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				content.append(inputLine);
			}
			in.close();
			response = content.toString();
			
		}catch(Exception e){
			e.printStackTrace();
		}

		return response;
	}

}
