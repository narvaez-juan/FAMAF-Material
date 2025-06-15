package namedEntity.entities.person;

public class Name extends PersonName{
    private String alternativeForm;
    
    public Name(String name, String category, int frequency, int id, String origin, String alternativeForm) {
        super(name, category, frequency, id, origin);
        this.alternativeForm = alternativeForm;
    }

    public String getAlternativeForm() {
        return alternativeForm;
    }

    public void setAlternativeForm(String alternativeForm) {
        this.alternativeForm = alternativeForm;
    }
}
