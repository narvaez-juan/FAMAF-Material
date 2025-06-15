package namedEntity.entities;

import namedEntity.NamedEntity;

import java.text.SimpleDateFormat;

public class Date extends NamedEntity {
    private SimpleDateFormat exactDate;

    public Date(String name, String category, int frequency, SimpleDateFormat exactDate) {
        super(name, category, frequency);
        this.exactDate = exactDate;
    }

    public SimpleDateFormat getExactDate() {
        return exactDate;
    }

    public void setExactDate(SimpleDateFormat exactDate) {
        this.exactDate = exactDate;
    }
}
