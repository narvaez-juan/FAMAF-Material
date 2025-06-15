package namedEntity.heuristic;

public class AllCapsHeuristic extends Heuristic{
    @Override
    public boolean isEntity(String word) {
        // Considera entidad si tiene más de una letra y todas son mayuscula
        return word.length() > 1 && word.equals(word.toUpperCase()) && word.matches("[A-Z]+");
    }

    public static void main(String[] args){
        //AllCapsHeuristic allCapsHeuristic = new AllCapsHeuristic();
    }
}
