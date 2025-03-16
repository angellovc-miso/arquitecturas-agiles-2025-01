
const generateRandomText = () => {
    const adjectives = ['Fast', 'Cool', 'Smart', 'Brave', 'Sneaky'];
    const animals = ['Tiger', 'Elephant', 'Shark', 'Eagle', 'Wolf'];
  
    return `${adjectives[Math.floor(Math.random() * adjectives.length)]}${animals[Math.floor(Math.random() * animals.length)]}${Math.floor(Math.random() * 10000000)}`;
}

module.exports = {
    generateRandomText
}