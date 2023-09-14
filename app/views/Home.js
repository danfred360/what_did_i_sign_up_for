import React, { useState } from 'react';
import { SafeAreaView, View, TextInput, Button, ActivityIndicator, Dimensions, ScrollView, TouchableOpacity, Text } from 'react-native';
import Answer from '../components/Answer';
import SearchResults from '../components/SearchResults';
import appStyles from '../styles/appStyles';
import searchStyles from '../styles/searchStyles';
import { searchDocuments, searchQuestions } from '../utils/api';

export default function Home() {
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
      const num_results = 5;
      const data = await searchDocuments(documentSearchTerm, num_results);
      setDocumentSearchResults(data);
    } catch (error) {
      setDocumentSearchResults(`Error: ${error}`);
    }
    setDocumentIsLoading(false);
  };

  const handleQuestionSearch = async () => {
    setQuestionIsLoading(true);
    try {
      const num_results = 5;
      const data = await searchQuestions(questionSearchTerm, num_results);
      setQuestionSearchResults(data);
    } catch (error) {
      setQuestionSearchResults(`Error: ${error}`);
    }
    setQuestionIsLoading(false);
  };

  const windowWidth = Dimensions.get('window').width;
  const searchBarWidth = windowWidth - 40;

  return (
    <SafeAreaView style={appStyles.parentContainer}>
        <View style={appStyles.container}>
          <View style={[searchStyles.searchContainer, { width: searchBarWidth }]}>
            <TextInput
              style={searchStyles.searchBar}
              placeholder="Ask a question..."
              value={questionSearchTerm}
              onChangeText={(text) => setQuestionSearchTerm(text)}
              autoCapitalize="none"
            />
            <TouchableOpacity style={appStyles.buttonContainer} onPress={handleQuestionSearch}>
              <Text style={appStyles.button}>Ask</Text>
            </TouchableOpacity>
          </View>
          {questionIsLoading && <ActivityIndicator style={searchStyles.loading} />}
          {questionSearchResults && questionSearchResults.answer ? (
            <Answer answer={questionSearchResults.answer} isCollapsed={questionIsCollapsed} setIsCollapsed={setQuestionIsCollapsed} />
          ) : (
            questionSearchResults && questionSearchResults.results && (
              <SearchResults results={questionSearchResults} isCollapsed={questionIsCollapsed} setIsCollapsed={setQuestionIsCollapsed} />
            )
          )}
          <View style={[searchStyles.searchContainer, { width: searchBarWidth }]}>
            <TextInput
              style={searchStyles.searchBar}
              placeholder="Enter a search query..."
              value={documentSearchTerm}
              onChangeText={(text) => setDocumentSearchTerm(text)}
              autoCapitalize="none"
            />
            <View >
              <TouchableOpacity style={appStyles.buttonContainer} onPress={handleDocumentSearch}>
                <Text style={appStyles.button}>Search</Text>
              </TouchableOpacity>
            </View>
          </View>
          {documentIsLoading && <ActivityIndicator style={searchStyles.loading} />}
          <SearchResults results={documentSearchResults} isCollapsed={documentIsCollapsed} setIsCollapsed={setDocumentIsCollapsed} />
        </View>
    </SafeAreaView>
  );
}