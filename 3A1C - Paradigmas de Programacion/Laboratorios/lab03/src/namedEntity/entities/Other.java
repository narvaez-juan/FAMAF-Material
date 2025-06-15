package namedEntity.entities;

import namedEntity.NamedEntity;

public class Other extends NamedEntity {
    private String comments;

    public Other(String name, String category, int frequency, String comments) {
        super(name, category, frequency);
        this.comments = comments;
    }

    public String getOther() {
        return comments;
    }

    public void setOther(String comments) {
        this.comments = comments;
    }
}
