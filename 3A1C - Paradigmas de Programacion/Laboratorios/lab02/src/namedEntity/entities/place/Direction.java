package namedEntity.entities.place;

import namedEntity.entities.Other;

public class Direction extends City{
    private String address;

    public Direction(String name,
                     String category,
                     int frequency,
                     Other other,
                     int population,
                     String officialLanguage,
                     boolean isCapital,
                     String address) {
        super(name, category, frequency, other, population, officialLanguage, isCapital);
        this.address = address;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }
}
