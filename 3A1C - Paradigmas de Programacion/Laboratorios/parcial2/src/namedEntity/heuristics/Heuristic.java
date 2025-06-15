package namedEntity.heuristics;

import java.util.HashMap;
import java.util.Map;

import feed.Article;
import feed.Feed;

public abstract class Heuristic {
	Map<String, Integer> namedEntities = new HashMap<String, Integer>();

	protected abstract boolean isEntity(String word);

	public void computeEntities(Feed feed){
		String charsToRemove = ".,;:()'!?\n";
		for (Article a:feed.getArticles()){
			String text = a.getTitle() + " " + a.getDescription();
			for (char c : charsToRemove.toCharArray()) {
				text = text.replace(String.valueOf(c), "");
			}

			for (String word : text.split(" ")) {
				if (isEntity(word) ){
					if (namedEntities.keySet().contains(word)){
						namedEntities.put(word,namedEntities.get(word)+1);
					}else{
						namedEntities.put(word,1);
					}
				}
			}
		}

	}


	public void printEntities(){
		System.out.println();
		for(String entity: namedEntities.keySet()){
			System.out.println(entity + " --> " + namedEntities.get(entity));
		}
		System.out.println();

	}

}
		
