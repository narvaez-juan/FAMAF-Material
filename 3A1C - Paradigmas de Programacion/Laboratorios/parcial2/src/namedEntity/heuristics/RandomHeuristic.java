package namedEntity.heuristics;

import java.util.Random;


public class RandomHeuristic extends Heuristic {	
	private Random rnd = new Random();

	protected boolean isEntity(String word){
		return ((int)(rnd.nextDouble() * 100)) % 2 == 0;						
	}
	
}
