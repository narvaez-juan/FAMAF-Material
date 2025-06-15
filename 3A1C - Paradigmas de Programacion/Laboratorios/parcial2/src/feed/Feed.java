package feed;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.io.FileNotFoundException;


/*Esta clase modela el concepto de Feed*/

public class Feed {
	String url;
	String type;
	private List<Article> articleList;
	
	public Feed(String url, String type) {
		this.url = url;
		this.type = type;
		this.articleList = new ArrayList<Article>();
	}
	
	public String getUrl(){
		return this.url;
	}
	public String getType(){
		return this.url;
	}
	public List<Article> getArticles(){
		return this.articleList;
	}

	public void addArticle(Article a){
		this.articleList.add(a);
	}
	
	
	@Override
	public String toString() {
		String feedString = "\n---------------------" + this.getUrl() + "---------------------\n";
		for (Article a: getArticles()){
			feedString+=a.toString();
		}
		return feedString;
	}

	public void writeToFile(Feed feed, String path) {
		try (PrintWriter out = new PrintWriter(path)) {
			String feedString = this.toString();
			out.println(feedString);
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}
	
	public void prettyPrint(){
		System.out.println(this.toString());
	}


}
