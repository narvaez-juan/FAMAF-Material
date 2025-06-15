package parser;

import feed.Feed;

/*Esta clase modela los atributos y metodos comunes a todos los distintos tipos de parser existentes en la aplicacion*/
public abstract class Parser {
    public static Feed parse(String feedString, String url, String type){
        Feed feed = null;
        if (type.equals("rss")){
            RssParser p = new RssParser();
            feed = p.parseRss(feedString,url,type);
        
        }else if (type.equals("reddit")){
            RedditParser p = new RedditParser();
            feed = p.parseReddit(feedString,url,type);
         
        }else if (type.equals("localhost")){
            LocalhostParser p = new LocalhostParser();
            feed = p.parseLocalhost(feedString,url,type);
        }

        return feed;

    }
} 
