import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

function SearchResults({ results }) {
  return (
    <View style={styles.resultsContainer}>
      <Text style={styles.title}>Search Results:</Text>
      <Text style={styles.count}>Count: {results.count}</Text>
      <View style={styles.results}>
        {results.results.map((result) => (
          <View key={result.id} style={styles.result}>
            <Text>ID: {result.id}</Text>
            <Text>Document ID: {result.document_id}</Text>
            <Text>Content: {result.content}</Text>
            <Text>Created At: {result.created_at}</Text>
          </View>
        ))}
      </View>
    </View>
  );
}

const parentStyles = StyleSheet.create({
  parentContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
});

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  searchContainer: {
    flexDirection: 'row',
    marginBottom: 10,
  },
  searchBar: {
    flex: 1,
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginRight: 10,
    paddingHorizontal: 10,
  },
  resultsContainer: {
    backgroundColor: '#f2f2f2',
    borderRadius: 10,
    padding: 10,
    margin: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  count: {
    marginBottom: 10,
  },
  results: {
    alignItems: 'center',
  },
  result: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 10,
    marginBottom: 10,
    width: '100%',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
});

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(null);

  const handleSearch = async () => {
    try {
      const encoded_query = encodeURIComponent(searchTerm);
      const num_results = 5;
      const response = await fetch(`http://localhost:8000/search?query=${encoded_query}&num_results=${num_results}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      setSearchResults(`Error: ${error}`);
    }
  };

  return (
    <View style={parentStyles.parentContainer}>
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
        {searchResults && <SearchResults results={searchResults} />}
      </View>
    </View>
  );
}