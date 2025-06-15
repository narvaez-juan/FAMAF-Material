package parser;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import subscription.SingleSubscription;
import subscription.Subscription;

/*
 * Esta clase implementa el parser del archivo de suscripción (json)
*/

public class SubscriptionParser extends GeneralParser {
    public SubscriptionParser(String filePath) {
        this.source = filePath;
    }

    @Override
    public Subscription parse() throws FileNotFoundException, IOException {
        Subscription subscription = new Subscription(this.source);

        // Lee el archivo JSON
        String jsonString = new String(Files.readAllBytes(Paths.get(this.source)));

        // Parsea el contenido JSON
        JSONArray jsonArray = new JSONArray(jsonString);

        // Itera sobre el array de suscripciones
        for (int i = 0, arr_len = jsonArray.length(); i < arr_len; i++) {
            JSONObject jsonObject = jsonArray.getJSONObject(i);

            String url = jsonObject.getString("url");
            String urlType = jsonObject.getString("urlType");
            JSONArray urlParams = jsonObject.getJSONArray("urlParams");

            // Crea una nueva SingleSubscription
            SingleSubscription singleSubscription = new SingleSubscription(url, null, urlType);

            // Añade los parámetros URL a la SingleSubscription
            for (int j = 0, param_len = urlParams.length(); j < param_len; j++) {
                singleSubscription.setUrlParams(urlParams.getString(j));
            }

            // Añade la SingleSubscription a la lista de suscripciones
            subscription.addSingleSubscription(singleSubscription);
        }

        return subscription;
    }
}
