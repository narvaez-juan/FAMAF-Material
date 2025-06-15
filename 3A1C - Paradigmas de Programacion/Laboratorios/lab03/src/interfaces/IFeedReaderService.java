package interfaces;

import feed.Feed;
import httpRequest.HttpRequester;
import namedEntity.heuristic.Heuristic;
import parser.RedditParser;
import parser.RssParser;
import subscription.SingleSubscription;

public interface IFeedReaderService {
    public void printFeedResults();
    public void printFeedEntitiesByHeuristic(Heuristic heuristic);

    // Método para obtener y parsear un feed según el tipo de url
    public static Feed getParsedFeed(SingleSubscription subscription, int paramIndex, HttpRequester requester) throws Exception {
        String url = subscription.getFeedToRequest(paramIndex);
        String urlType = subscription.getUrlType();
        String stringFeed = requester.getFeed(url);
        System.out.println("Feed extraido de: " + url);

        switch (urlType) {
            case "reddit":
                RedditParser redditParser = new RedditParser(stringFeed, subscription.getUrl());
                return redditParser.parse();
            case "rss":
                RssParser rssParser = new RssParser(stringFeed, subscription.getUrl());
                return rssParser.parse();
            default:
                System.err.println("Tipo de feed no soportado: " + urlType);
                return null;
        }
    }
}
