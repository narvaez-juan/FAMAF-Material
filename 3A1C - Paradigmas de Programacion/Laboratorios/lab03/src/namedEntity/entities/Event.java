package namedEntity.entities;

import namedEntity.NamedEntity;


public class Event extends NamedEntity {
    private Date date;
    private boolean isRecurrent;

    public Event(String name, String category, int frequency, Date date, boolean isRecurrent) {
        super(name, category, frequency);
        this.date = date;
        this.isRecurrent = isRecurrent;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public boolean isRecurrent() {
        return isRecurrent;
    }

    public void setRecurrent(boolean recurrent) {
        isRecurrent = recurrent;
    }
}
