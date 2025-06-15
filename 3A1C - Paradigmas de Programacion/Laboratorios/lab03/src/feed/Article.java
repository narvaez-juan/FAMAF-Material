package feed;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.function.BiFunction;
import scala.Serializable;

import namedEntity.NamedEntity;
import namedEntity.heuristic.Heuristic;
import namedEntity.entities.*;
import namedEntity.entities.person.Person;
import namedEntity.entities.person.Name;
import namedEntity.entities.person.LastName;
import namedEntity.entities.person.PersonName;
import namedEntity.entities.place.Place;
import namedEntity.entities.place.Country;
import namedEntity.entities.place.City;
import namedEntity.entities.place.Direction;

/*Esta clase modela el contenido de un articulo (ie, un item en el caso del rss feed) */

public class Article implements Serializable {
	private String title;
	private String text;
	private Date publicationDate;
	private String link;
	
	private List<NamedEntity> namedEntityList = new ArrayList<NamedEntity>();
	
	
	public Article(String title, String text, Date publicationDate, String link) {
		super();
		this.title = title;
		this.text = text;
		this.publicationDate = publicationDate;
		this.link = link;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Date getPublicationDate() {
		return publicationDate;
	}

	public void setPublicationDate(Date publicationDate) {
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
		return "Article [title=" + title + ", text=" + text + ", publicationDate=" + publicationDate + ", link=" + link
				+ "]";
	}
	
	
	
	public NamedEntity getNamedEntity(String namedEntity){
		for (NamedEntity n: namedEntityList){
			if (n.getName().compareTo(namedEntity) == 0){				
				return n;
			}
		}
		return null;
	}

	public List<NamedEntity> getNamedEntitiesList() {
		return new ArrayList<>(this.namedEntityList);
	}
	
	private static final Map<String, BiFunction<String, String, NamedEntity>> categoryEntityMap = new HashMap<>();
	static {
		categoryEntityMap.put("Person", (word, category) -> new Person(word, category, 1, 0));
		categoryEntityMap.put("PersonName", (word, category) -> new PersonName(word, category, 1, 0, ""));
		categoryEntityMap.put("Name", (word, category) -> new Name(word, category, 1, 0, "", ""));
		categoryEntityMap.put("LastName", (word, category) -> new LastName(word, category, 1, 0, "", ""));
		categoryEntityMap.put("Place", (word, category) -> new Place(word, category, 1, null));
		categoryEntityMap.put("Country", (word, category) -> new Country(word, category, 1, null, 0, ""));
		categoryEntityMap.put("City", (word, category) -> new City(word, category, 1, null, 0, "", false));
		categoryEntityMap.put("Direction", (word, category) -> new Direction(word, category, 1, null, 0, "", false, ""));
		categoryEntityMap.put("Organization", (word, category) -> new Organization(word, category, 1, 0, ""));
		categoryEntityMap.put("Product", (word, category) -> new Product(word, category, 1, false, ""));
		categoryEntityMap.put("Event", (word, category) -> new Event(word, category, 1, null, false));
		categoryEntityMap.put("Date", (word, category) -> new namedEntity.entities.Date(word, category, 1, null));
		categoryEntityMap.put("Other", (word, category) -> new Other(word, category, 1, ""));
	}

	private NamedEntity createEntityByCategory(String word, String category) {
		return categoryEntityMap.getOrDefault(
			category,
			(w, c) -> new NamedEntity(w, c, 1)
		).apply(word, category);
	}

	public void computeNamedEntities(Heuristic h){
		String text = this.getTitle() + " " +  this.getText();  
		String charsToRemove = ".,;:()'!?\n";
		for (char c : charsToRemove.toCharArray()) {
			text = text.replace(String.valueOf(c), "");
		}
		for (String s: text.split(" ")) {
			if (h.isEntity(s)){
				NamedEntity ne = this.getNamedEntity(s);
				if (ne == null) {
					String category = h.getCategory(s);
					if (category == null) {
						category = "Other";
					}
					ne = createEntityByCategory(s, category);
					this.namedEntityList.add(ne);
				} else {
					ne.incFrequency();
				}
			}
		} 
	}

	
	public void prettyPrint() {
		System.out.println("**********************************************************************************************");
		System.out.println("Title: " + this.getTitle());
		System.out.println("Publication Date: " + this.getPublicationDate());
		System.out.println("Link: " + this.getLink());
		System.out.println("Text: " + this.getText());
		System.out.println("**********************************************************************************************");
		
	}
	
	public static void main(String[] args) {
		  Article a = new Article("This Historically Black University Created Its Own Tech Intern Pipeline",
			  "A new program at Bowie State connects computing students directly with companies, bypassing an often harsh Silicon Valley vetting process",
			  new Date(),
			  "https://www.nytimes.com/2023/04/05/technology/bowie-hbcu-tech-intern-pipeline.html"
			  );
		 
		  a.prettyPrint();
	}
	
	
}



