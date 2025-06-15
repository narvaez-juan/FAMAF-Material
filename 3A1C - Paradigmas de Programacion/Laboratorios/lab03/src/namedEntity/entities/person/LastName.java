package namedEntity.entities.person;

public class LastName extends PersonName {
    private String lastName;

    public LastName(String name, String category, int frequency, int id, String origin, String lastName) {
        super(name, category, frequency, id, origin);
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }
}
