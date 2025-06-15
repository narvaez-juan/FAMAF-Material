package Request;

public class Requester {
    private String url;
    private String type;
	private String response = null;

	public Requester(String url, String type){
        this.url = url;
        this.type = type;
        switch (type) {
            case "rss":
                this.response = HttpRequester.getResponse(url);                
                break;
            case "reddit":              
                this.response = HttpRequester.getResponse(url);                
                break;
            case "localhost": 
                this.response = LocalhostRequester.getResponse(url);
                break;
            default:
                break;
        }
    }
    
    public String getResponse(){
		return this.response;
	}
    public String getType(){
		return this.type;
	}
    public String getUrl(){
		return this.url;
	}

}
