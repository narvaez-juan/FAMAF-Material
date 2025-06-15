package namedEntity.entities.person;

import namedEntity.NamedEntity;

public class Person extends NamedEntity {
    private int id;

    public Person(String name, String category, int frequency, int id) {
        super(name, category, frequency);
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }
}
