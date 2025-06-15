package namedEntity.entities;

import namedEntity.NamedEntity;

public class Product extends NamedEntity {
    private boolean isComercial;
    private String producer;

    public Product(String name, String category, int frequency, boolean isComercial, String producer) {
        super(name, category, frequency);
        this.isComercial = isComercial;
        this.producer = producer;
    }

    public boolean isComercial() {
        return isComercial;
    }

    public void setComercial(boolean comercial) {
        isComercial = comercial;
    }

    public String getProducer() {
        return producer;
    }

    public void setProducer(String producer) {
        this.producer = producer;
    }
}
