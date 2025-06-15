import subscription.Subscription;
import subscription.Subscriptions;
import Request.Requester;
import parser.Parser;
import feed.Feed;


public class FeedReaderMain_ej3 {
	public static void main(String[] args) {
	
		Subscriptions sub = new Subscriptions("config/subscriptions_ej3.json");
		for (Subscription s: sub.getSubscriptions()){
			Requester request = new Requester(s.getUrl(),s.getUrlType());
			Feed feed = Parser.parse(request.getResponse(), request.getUrl() ,request.getType()); 
			feed.prettyPrint();
		}		
	}

}
