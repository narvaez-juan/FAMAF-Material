package namedEntity.entities.place;

import namedEntity.entities.Other;

public class Country extends Place{
    private int population;
    private String officialLanguage;

    public Country(String name, String category, int frequency, Other other, int population, String officialLanguage) {
        super(name, category, frequency, other);
        this.population = population;
        this.officialLanguage = officialLanguage;
    }

    public int getPopulation() {
        return population;
    }

    public void setPopulation(int population) {
        this.population = population;
    }

    public String getOfficialLanguage() {
        return officialLanguage;
    }

    public void setOfficialLanguage(String officialLanguage) {
        this.officialLanguage = officialLanguage;
    }
}
