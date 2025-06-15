package feed;

/*Esta clase modela el contenido de un articulo (ie, un item en el caso del rss feed) */

public class Article {
	private String title;
	private String description;
	private String publicationDate;
	private String link;
		
	public Article(String title, String description, String publicationDate, String link) {
		this.title = title;
		this.description = description;
		this.publicationDate = publicationDate;
		this.link = link;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getPublicationDate() {
		return publicationDate;
	}

	public void setPublicationDate(String publicationDate) {
		this.publicationDate = publicationDate;
	}

	public String getLink() {
		return link;
	}

	public void setLink(String link) {
		this.link = link;
	}
	
	@Override
	public String toString() {
		return 	"\nTitle: " + this.getTitle() + 
				"\nDescription: " + this.getDescription() +
				"\nPublication Date: " + this.getPublicationDate() + 
				"\nLink: " + this.getLink() + "\n";

	}
	
	
	public void prettyPrint() {
		System.out.print(this.toString());
	}
	
}



