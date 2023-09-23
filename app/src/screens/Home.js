import { useState } from 'react';
import {
  View,
  TextInput,
  ActivityIndicator,
  Pressable,
  Text,
  ScrollView
} from 'react-native';
import Answer from '../components/Answer';
import SearchResults from '../components/SearchResults';
import CollectionTray from '../components/CollectionTray';
import FileSubmitForm from '../components/FileSubmitForm';
import searchStyles from '../styles/searchStyles';
import mainStyles from '../styles/main';
import { searchDocuments, searchQuestions } from '../utils/api';

const useSearch = (searchFunction, selectedCollection) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [inputIsFocused, setInputIsFocused] = useState(false);
  const [btnIsFocused, setBtnIsFocused] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const data = await searchFunction(searchTerm, 5, selectedCollection);
      setSearchResults(data);
    } catch (error) {
      setSearchResults(`Error: ${error}`);
    }
    setIsLoading(false);
  };

  return {
    searchTerm,
    setSearchTerm,
    searchResults,
    isLoading,
    handleSearch,
    inputIsFocused,
    setInputIsFocused,
    btnIsFocused,
    setBtnIsFocused,
  };
};

export default function Home() {
  const [selectedCollection, setSelectedCollection] = useState(null);

  const {
    searchTerm: documentSearchTerm,
    setSearchTerm: setDocumentSearchTerm,
    searchResults: documentSearchResults,
    isLoading: documentIsLoading,
    handleSearch: handleDocumentSearch,
    inputIsFocused: searchBarIsFocused,
    setInputIsFocused: setSearchBarIsFocused,
    btnIsFocused: searchBtnIsFocused,
    setBtnIsFocused: setSearchBtnIsFocused,
  } = useSearch(searchDocuments, selectedCollection);

  const {
    searchTerm: questionSearchTerm,
    setSearchTerm: setQuestionSearchTerm,
    searchResults: questionSearchResults,
    isLoading: questionIsLoading,
    handleSearch: handleQuestionSearch,
    inputIsFocused: questionBarIsFocused,
    setInputIsFocused: setQuestionBarIsFocused,
    btnIsFocused: questionBtnIsFocused,
    setBtnIsFocused: setQuestionBtnIsFocused,
  } = useSearch(searchQuestions, selectedCollection);

  const [currentSection, setCurrentSection] = useState('question');

  return (
    <ScrollView>
      <View style={mainStyles.form_area}>
        <Text style={mainStyles.title}>EXPLORE</Text>
        <View style={[mainStyles.form_group_horizontal_centered]}>
          <Pressable
            style={[mainStyles.btn, currentSection === 'question' ? mainStyles.btn_active : {}]}
            onPress={() => setCurrentSection('question')}>
            <Text style={mainStyles.text}>Question</Text>
          </Pressable>
          <Pressable
            style={[mainStyles.btn, currentSection === 'search' ? mainStyles.btn_active : {}]}
            onPress={() => setCurrentSection('search')}>
            <Text style={mainStyles.text}>Search</Text>
          </Pressable>
        </View>
      </View>
      <CollectionTray setSelectedCollectionId={setSelectedCollection} />
      {currentSection === 'question' && (
        <View style={mainStyles.form_area}>
          <Text style={mainStyles.title}>QUESTION</Text>
          <View style={mainStyles.form_group_horizontal}>
            <TextInput
              style={[mainStyles.form_style, questionBarIsFocused ? mainStyles.form_style_focused : null]}
              placeholder="Ask a question..."
              value={questionSearchTerm}
              onChangeText={setQuestionSearchTerm}
              autoCapitalize="none"
              onFocus={() => setQuestionBarIsFocused(true)}
              onBlur={() => setQuestionBarIsFocused(false)}
            />
            <Pressable
              style={[mainStyles.btn, questionBtnIsFocused ? mainStyles.btn_focused : null]}
              onPress={handleQuestionSearch}
              onPressIn={() => setQuestionBtnIsFocused(true)}
              onPressOut={() => setQuestionBtnIsFocused(false)}
            >
              <Text style={mainStyles.text}>Ask</Text>
            </Pressable>
          </View>
        </View>
      )}

      {currentSection === 'question' && questionIsLoading ? (
        <ActivityIndicator style={searchStyles.loading} />
      ) : (
        currentSection === 'question' && questionSearchResults?.answer && (
          <Answer answer={questionSearchResults.answer} />
        )
      )}

      {currentSection === 'search' && (
        <View style={mainStyles.form_area}>
          <Text style={mainStyles.title}>SEARCH</Text>
          <View style={mainStyles.form_group_horizontal}>
            <TextInput
              style={[mainStyles.form_style, searchBarIsFocused ? mainStyles.form_style_focused : null]}
              placeholder="Enter a search query..."
              value={documentSearchTerm}
              onChangeText={setDocumentSearchTerm}
              autoCapitalize="none"
              onFocus={() => setSearchBarIsFocused(true)}
              onBlur={() => setSearchBarIsFocused(false)}
            />
            <Pressable
              style={[mainStyles.btn, searchBtnIsFocused ? mainStyles.btn_focused : null]}
              onPress={handleDocumentSearch}
              onPressIn={() => setSearchBtnIsFocused(true)}
              onPressOut={() => setSearchBtnIsFocused(false)}
            >
              <Text style={mainStyles.text}>Search</Text>
            </Pressable>
          </View>
        </View>
      )}

      {currentSection === 'search' && documentIsLoading ? (
        <ActivityIndicator style={searchStyles.loading} />
      ) : (
        currentSection === 'search' && (
          <SearchResults results={documentSearchResults} /* other props here */ />
        )
      )}
      <FileSubmitForm collectionId={selectedCollection} />
    </ScrollView>
  );
}
