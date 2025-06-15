package namedEntity.heuristics;

import java.util.HashMap;
import java.util.Map;

import feed.Article;
import feed.Feed;

public class ParityHeuristic extends Heuristic {

    protected boolean isEntity(String word) {
        return word.length() > 1 && (word.length() % 2 == 0);
    }
}
