package parser;


/*
 * Esta clase implementa el parser de feed de tipo reddit (json)
 * pero no es necesario su implemntacion 
 * */

import feed.Article;
import feed.Feed;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.Date;

public class RedditParser extends GeneralParser {
    private String siteName;

    public RedditParser(String source, String siteName) {
        this.siteName = siteName;
        this.source = source;
    }
    @Override
    public Feed parse() throws Exception {
        Feed feed = new Feed(this.siteName);

        // Lee la respuesta JSON
        JSONObject jsonObject = new JSONObject(this.source);

        // Control de la existencia de los campos
        if (!jsonObject.has("data")) return feed;
        JSONObject data = jsonObject.getJSONObject("data");
        if (!data.has("children")) return feed;
        JSONArray children = data.getJSONArray("children");

        for (int i = 0, length = children.length(); i < length; i++) {
            try {
                // Obtención de datos
                JSONObject postData =  children.getJSONObject(i).getJSONObject("data");
                String title = postData.optString("title");
                String text = postData.optString("selftext");
                long createdUtc = postData.optLong("created_utc");
                Date publicationDate = new Date(createdUtc * 1000);
                String link = postData.optString("url");

                // Añadir articulo al feed
                feed.addArticle(new Article(title, text, publicationDate, link));
            }
            catch (Exception e) {
                //Si un post no esta en formato correcto, lo ignora y sigue
                continue;
            }
        }
        return feed;
    }
}
