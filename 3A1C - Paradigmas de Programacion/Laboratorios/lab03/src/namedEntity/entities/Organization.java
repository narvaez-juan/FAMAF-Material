package namedEntity.entities;

import namedEntity.NamedEntity;

public class Organization extends NamedEntity {
    private int members;
    private String type;

    public Organization(String name, String category, int frequency, int members, String type) {
        super(name, category, frequency);
        this.members = members;
        this.type = type;
    }

    public int getMembers() {
        return members;
    }

    public void setMembers(int members) {
        this.members = members;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
}
