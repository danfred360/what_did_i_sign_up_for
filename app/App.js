import React, { useState } from 'react';
import { StyleSheet, Text, SafeAreaView, ScrollView, TextInput, Button, ActivityIndicator, View, Platform, Dimensions } from 'react-native';

function SearchResults({ results, isCollapsed, setIsCollapsed }) {
  if (!results || !results.results) {
    return null;
  }

  return (
    <View style={styles.resultsContainer}>
      <View style={styles.resultsHeader}>
        <Text style={styles.title}>Search Results:</Text>
        <Button title={isCollapsed ? "Expand" : "Collapse"} onPress={() => setIsCollapsed(!isCollapsed)} />
      </View>
      {!isCollapsed && (
        <>
          <Text style={styles.count}>Count: {results.count}</Text>
          {results.results.map((result) => (
            <View key={result.id} style={styles.result}>
              <Text>ID: {result.id}</Text>
              <Text>Document ID: {result.document_id}</Text>
              <Text style={styles.content}>Content: {result.content}</Text>
              <Text>Created At: {result.created_at}</Text>
            </View>
          ))}
        </>
      )}
    </View>
  );
}

function Answer({ answer, isCollapsed, setIsCollapsed }) {
  return (
    <View style={styles.resultsContainer}>
      <View style={styles.resultsHeader}>
        <Text style={styles.title}>Answer:</Text>
        <Button title={isCollapsed ? "Expand" : "Collapse"} onPress={() => setIsCollapsed(!isCollapsed)} />
      </View>
      {!isCollapsed && (
        <Text style={styles.content}>{answer}</Text>
      )}
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
    borderRadius: 20,
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
    borderRadius: 20,
    overflow: 'hidden',
    ...Platform.select({
      ios: {
        borderWidth: 1,
        borderColor: 'gray',
      },
      android: {
        borderColor: 'gray',
        borderWidth: 1,
      },
    }),
  },
  searchBar: {
    flex: 1,
    height: 40,
    paddingHorizontal: 10,
    borderRadius: 20,
    marginRight: 10,
    backgroundColor: '#f2f2f2',
    ...Platform.select({
      ios: {
        borderWidth: 1,
        borderColor: 'gray',
      },
      android: {
        borderColor: 'gray',
        borderWidth: 1,
      },
    }),
  },
  searchButton: {
    borderRadius: 20,
    paddingHorizontal: 10,
  },
  resultsContainer: {
    backgroundColor: '#f2f2f2',
    borderRadius: 20,
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
  resultsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
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
  const [documentSearchTerm, setDocumentSearchTerm] = useState('');
  const [documentSearchResults, setDocumentSearchResults] = useState(null);
  const [documentIsLoading, setDocumentIsLoading] = useState(false);
  const [questionSearchTerm, setQuestionSearchTerm] = useState('');
  const [questionSearchResults, setQuestionSearchResults] = useState(null);
  const [questionIsLoading, setQuestionIsLoading] = useState(false);
  const [documentIsCollapsed, setDocumentIsCollapsed] = useState(false);
  const [questionIsCollapsed, setQuestionIsCollapsed] = useState(false);

  const handleDocumentSearch = async () => {
    setDocumentIsLoading(true);
    try {
      const encoded_query = encodeURIComponent(documentSearchTerm);
      const num_results = 5;
      const response = await fetch(`http://localhost:8000/search?query=${encoded_query}&num_results=${num_results}`);
      const data = await response.json();
      setDocumentSearchResults(data);
    } catch (error) {
      setDocumentSearchResults(`Error: ${error}`);
    }
    setDocumentIsLoading(false);
  };

  const handleQuestionSearch = async () => {
    setQuestionIsLoading(true);
    try {
      const encoded_query = encodeURIComponent(questionSearchTerm);
      const num_results = 5;
      const response = await fetch(`http://localhost:8000/question?question=${encoded_query}&num_results=${num_results}`);
      const data = await response.json();
      setQuestionSearchResults(data);
    } catch (error) {
      setQuestionSearchResults(`Error: ${error}`);
    }
    setQuestionIsLoading(false);
  };

  const windowWidth = Dimensions.get('window').width;
  const searchBarWidth = windowWidth - 40;

  return (
    <SafeAreaView style={parentStyles.parentContainer}>
      <View style={styles.container}>
        <View style={[styles.searchContainer, { width: searchBarWidth }]}>
          <TextInput
            style={styles.searchBar}
            placeholder="Search documents..."
            value={documentSearchTerm}
            onChangeText={(text) => setDocumentSearchTerm(text)}
          />
          <Button title="Search" onPress={handleDocumentSearch} style={styles.searchButton} />
        </View>
        {documentIsLoading && <ActivityIndicator style={styles.loading} />}
        <SearchResults results={documentSearchResults} isCollapsed={documentIsCollapsed} setIsCollapsed={setDocumentIsCollapsed} />
        <View style={[styles.searchContainer, { width: searchBarWidth }]}>
          <TextInput
            style={styles.searchBar}
            placeholder="Ask a question..."
            value={questionSearchTerm}
            onChangeText={(text) => setQuestionSearchTerm(text)}
          />
          <Button title="Ask" onPress={handleQuestionSearch} style={styles.searchButton} />
        </View>
        {questionIsLoading && <ActivityIndicator style={styles.loading} />}
        {questionSearchResults && questionSearchResults.answer ? (
          <Answer answer={questionSearchResults.answer} isCollapsed={questionIsCollapsed} setIsCollapsed={setQuestionIsCollapsed} />
        ) : (
          questionSearchResults && questionSearchResults.results && (
            <SearchResults results={questionSearchResults} isCollapsed={questionIsCollapsed} setIsCollapsed={setQuestionIsCollapsed} />
          )
        )}
      </View>
    </SafeAreaView>
  );
}