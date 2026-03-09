const createDataGenerator = () => {
  const fakeNames = ['Laura', 'Leandro', 'Gonzalo', 'Matias', 'Diego', 'Andres', 'Santiago', 'Jeremias'];
  const fakeLastNames = ['Brandan', 'Ramos', 'Peralta', 'Lee', 'Lis', 'Luna', 'Avalos', 'Luque'];

  const createContact = (tags) => {
    // Random name and lastname
    const randomName = fakeNames[Math.floor(Math.random() * fakeNames.length)];
    const randomLastName = fakeLastNames[Math.floor(Math.random() * fakeLastNames.length)];
    
    // Generate random email based on name
    const emailDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'ingsoft.com'];
    const randomDomain = emailDomains[Math.floor(Math.random() * emailDomains.length)];
    const randomEmail = `${randomName.toLowerCase()}.${randomLastName.toLowerCase()}@${randomDomain}`;
    
    // Generate random phone numbers
    const generatePhoneNumber = () => {
      const exchange = Math.floor(Math.random() * 9) + 1;
      const number = Math.floor(Math.random() * 900000) + 100000;
      return `(351) ${exchange}${number}`;
    };
    
    // Random tags selection
    const randomTagsCount = Math.floor(Math.random() * (tags.length + 1)); // 0 to all tags
    const shuffledTags = [...tags].sort(() => 0.5 - Math.random());
    const selectedTags = shuffledTags.slice(0, randomTagsCount).map(tag => tag.id);
    
    // 50% chance of having a backup phone
    const hasBackupPhone = Math.random() > 0.5;
    
    return {
      name: randomName,
      lastname: randomLastName,
      email: randomEmail,
      phone_main: generatePhoneNumber(),
      phone_backup: hasBackupPhone ? generatePhoneNumber() : '',
      tags: selectedTags
    };
  };

  return {
    createContact,
  };
};

export {
  createDataGenerator
};