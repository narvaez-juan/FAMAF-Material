package subscription;

/*Esta clase abstrae el contenido de una sola suscripcion que ocurre en 
lista de suscripciones que figuran en el archivo de suscrpcion (json) */

public class Subscription{
	
	private String url;
	private String urlType;
	private String download=null;
	
	public Subscription(String url, String urltype, String download){
		this.url = url;
		this.urlType = urltype;
		this.download = download;
	}

	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}

	public String getUrlType() {
		return urlType;
	}
	public void setUrlType(String urlType) {
		this.urlType = urlType;
	}

	public String getDownload() {
		return download;
	}
	public void setDownload(String urlType) {
		this.download = download;
	}

	@Override
	public String toString() {
		return "{url=" + getUrl() + ", urlType=" + getUrlType() + "}";
	}
	
	public void prettyPrint(){
		System.out.println(this.toString());
	}

	
	

	
	
	
}
