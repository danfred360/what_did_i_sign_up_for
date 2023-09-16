import { useState } from 'react';
import {
  SafeAreaView,
  View,
  TextInput,
  ActivityIndicator,
  Pressable,
  Text,
} from 'react-native';
import Answer from '../components/Answer';
import SearchResults from '../components/SearchResults';
import searchStyles from '../styles/searchStyles';
import mainStyles from '../styles/main';
import { searchDocuments, searchQuestions } from '../utils/api';

const useSearch = (searchFunction) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [inputIsFocused, setInputIsFocused] = useState(false);
  const [btnIsFocused, setBtnIsFocused] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      const data = await searchFunction(searchTerm, 5);
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
    isCollapsed,
    setIsCollapsed,
    handleSearch,
    inputIsFocused,
    setInputIsFocused,
    btnIsFocused,
    setBtnIsFocused,
  };
};

export default function Home(handleSignOut) {
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
    results
  } = useSearch(searchDocuments);

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
  } = useSearch(searchQuestions);

  const [currentSection, setCurrentSection] = useState('question');

  return (
    <View>
      <View style={mainStyles.form_area}>
        <Text style={mainStyles.title}>EXPLORE</Text>

        <View style={mainStyles.toggleButtonGroup}>
          <Pressable
            style={[mainStyles.toggleButton, currentSection === 'question' ? mainStyles.toggleButtonActive : {}]}
            onPress={() => setCurrentSection('question')}>
            <Text style={mainStyles.text}>Questions</Text>
          </Pressable>
          <Pressable
            style={[mainStyles.toggleButton, currentSection === 'search' ? mainStyles.toggleButtonActive : {}]}
            onPress={() => setCurrentSection('search')}>
            <Text style={mainStyles.text}>Search</Text>
          </Pressable>
        </View>
      </View>
      {currentSection === 'question' && (
        <View style={mainStyles.form_area}>
          <View style={mainStyles.form_group}>
            <Text style={mainStyles.sub_title}>Question</Text>
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
          <View style={mainStyles.form_group}>
            <Text style={mainStyles.sub_title}>Search</Text>
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
    </View>
  );
}
