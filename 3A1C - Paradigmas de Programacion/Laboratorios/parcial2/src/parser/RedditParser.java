package parser;

import feed.Feed;

/*
 * Esta clase implementa el parser de feed de tipo reddit (json)
 * pero no es necesario su implementacion.
 * */

public class RedditParser extends Parser {

     public Feed parseReddit(String redditFeed,String url, String type){
      Feed feed = new Feed(url,type);

      /*FALTA IMPLEMENTAR Y NO HAY QUE HACERLO */
      
      return feed;
     }

}
