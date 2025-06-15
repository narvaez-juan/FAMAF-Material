package Services;

import namedEntity.heuristic.Heuristic;

public interface IFeedReaderService {
    public void printFeedResults();
    public void printFeedEntitiesByHeuristic(Heuristic heuristic);
}
