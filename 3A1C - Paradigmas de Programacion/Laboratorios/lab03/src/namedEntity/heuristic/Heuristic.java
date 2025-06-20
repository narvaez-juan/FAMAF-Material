package namedEntity.heuristic;

import java.util.Map;
import scala.Serializable;

public abstract class Heuristic implements Serializable {

	private static Map<String, String> categoryMap = Map.of(
			"Microsft", "Company", 
			"Apple", "Company", 
			"Google", "Company",
			"Musk", "Person",
			"Biden", "Person",
			"Trump", "Person",
			"Messi", "Person",
			"Federer", "Person",
			"USA", "Country",
			"Thanks", "Country"
			);
	
	
	public String getCategory(String entity){
		return categoryMap.get(entity);
	}
	
	
	public abstract boolean isEntity(String word);
		
}
