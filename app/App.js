import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = async () => {
    try {
      const encoded_query = encodeURIComponent(searchTerm);
      const num_results = 5;
      const response = await fetch(`http://localhost:8000/search?query=${encoded_query}&num_results=${num_results}`);
      const data = await response.json();
      console.log(`data: ${JSON.stringify(data)}`)
      setSearchResults(JSON.stringify(data));
    } catch (error) {
      setSearchResults(`Error: ${error}`);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.searchBar}
          placeholder="Search..."
          value={searchTerm}
          onChangeText={(text) => setSearchTerm(text)}
        />
        <Button title="Search" onPress={handleSearch} />
      </View>
      {searchResults && <Text>{searchResults}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  searchContainer: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  searchBar: {
    borderWidth: 2,
    borderColor: '#ccc',
    borderRadius: 4,
    width: 200,
    height: 40,
    paddingLeft: 8,
    paddingRight: 8,
  },
});
