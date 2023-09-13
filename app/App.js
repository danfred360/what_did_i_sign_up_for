import React, { useState } from 'react';
import { StyleSheet, Text, SafeAreaView, ScrollView, TextInput, Button, ActivityIndicator, View } from 'react-native';

function SearchResults({ results }) {
  return (
    <ScrollView style={styles.resultsContainer}>
      <Text style={styles.title}>Search Results:</Text>
      <Text style={styles.count}>Count: {results.count}</Text>
      {results.results.map((result) => (
        <View key={result.id} style={styles.result}>
          <Text>ID: {result.id}</Text>
          <Text>Document ID: {result.document_id}</Text>
          <Text style={styles.content}>Content: {result.content}</Text>
          <Text>Created At: {result.created_at}</Text>
        </View>
      ))}
    </ScrollView>
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
  content: {
    fontWeight: 'bold',
    marginTop: 5,
    marginBottom: 10,
  },
  loading: {
    marginTop: 20,
  },
});

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const encoded_query = encodeURIComponent(searchTerm);
      const num_results = 5;
      const response = await fetch(`http://localhost:8000/search?query=${encoded_query}&num_results=${num_results}`);
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      setSearchResults(`Error: ${error}`);
    }
    setIsLoading(false);
  };

  return (
    <SafeAreaView style={parentStyles.parentContainer}>
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
        {isLoading && <ActivityIndicator style={styles.loading} />}
        {searchResults && <SearchResults results={searchResults} />}
      </View>
    </SafeAreaView>
  );
}