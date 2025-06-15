package namedEntity.entities.person;

public class PersonName extends Person {
    private String origin;

    public PersonName(String name, String category, int frequency, int id, String origin) {
        super(name, category, frequency, id);
        this.origin = origin;
    }

    public String getOrigin() {
        return origin;
    }

    public void setOrigin(String origin) {
        this.origin = origin;
    }
}
