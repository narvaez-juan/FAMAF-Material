package namedEntity.entities.place;

import namedEntity.entities.Other;

public class City extends Country{
    private boolean isCapital;

    public City(String name, String category, int frequency, Other other, int population, String officialLanguage, boolean isCapital) {
        super(name, category, frequency, other, population, officialLanguage);
        this.isCapital = isCapital;
    }

    public boolean isCapital() {
        return isCapital;
    }

    public void setCapital(boolean capital) {
        isCapital = capital;
    }
}
