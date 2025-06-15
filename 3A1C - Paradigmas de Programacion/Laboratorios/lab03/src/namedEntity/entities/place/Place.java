package namedEntity.entities.place;

import namedEntity.NamedEntity;
import namedEntity.entities.Other;

public class Place extends NamedEntity {
    private Other other;

    public Place(String name, String category, int frequency, Other other) {
        super(name, category, frequency);
        this.other = other;
    }

    public Other getOther() {
        return other;
    }

    public void setOther(Other other) {
        this.other = other;
    }
}
