package subscription;

import java.util.ArrayList;
import java.util.List;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.json.JSONArray;
import org.json.JSONException;

/*Esta clse abstrae el contenido de todo el archivo de suscripciones (config/subscriptions.json)*/
public class Subscriptions {
	private String subscriptionFilePath;
	private List<Subscription> subscriptionsList;
	
	
	public Subscriptions(String subscriptionFilePath){
		this.subscriptionFilePath = subscriptionFilePath;
		this.subscriptionsList = new ArrayList<Subscription>();

		try {
			String jsonString = new String(Files.readAllBytes(Paths.get(subscriptionFilePath)));
			JSONArray jsonArray = new JSONArray(jsonString);
			for (int i = 0; i < jsonArray.length(); i++) {
				String url = jsonArray.getJSONObject(i).getString("url");
				String urlType = jsonArray.getJSONObject(i).getString("urlType");
				String download = null;
				if (jsonArray.getJSONObject(i).has("download")) {
					download = jsonArray.getJSONObject(i).getString("download");
				}
				Subscription sb = new Subscription(url,urlType,download);
				this.addSubscription(sb);

			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}


	public void addSubscription(Subscription s) {
		this.subscriptionsList.add(s);
	}
	
	public List<Subscription> getSubscriptions(){
		return this.subscriptionsList;
	}

	@Override
	public String toString() {
		String str ="[";
		for (Subscription sub: this.subscriptionsList){
			str += sub.toString() + ",\n";
		}
		return str.substring(0, str.length()-2) + "]";
	}	
	
	public void prettyPrint(){
		System.out.println(this.toString());
	}

}
