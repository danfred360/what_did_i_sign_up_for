import { View, Text, Button, TouchableOpacity, ScrollView } from 'react-native';
import resultStyles from '../styles/resultStyles';
import appStyles from '../styles/appStyles';

function SearchResults({ results, isCollapsed, setIsCollapsed }) {
  if (!results || !results.results) {
    return null;
  }

  return (
    <View style={resultStyles.resultsContainer}>
      <View style={resultStyles.resultsHeader}>
        <Text style={resultStyles.title}>Search Results</Text>
        <TouchableOpacity style={appStyles.buttonContainer} onPress={() => setIsCollapsed(!isCollapsed)}>
          <Text style={appStyles.button}>{isCollapsed ? "Expand" : "Collapse"}</Text>
        </TouchableOpacity>
      </View>
      {!isCollapsed && (
        <ScrollView>
        <View style={resultStyles.scrollContainer}>
          
            <View style={resultStyles.results}>
              <Text style={resultStyles.count}>Count: {results.count}</Text>
              {results.results.map((result) => (
                <View key={result.id} style={resultStyles.result}>
                  <Text>Document ID: {result.document_id}</Text>
                  <Text style={resultStyles.content}>{result.content}</Text>
                  <Text>Updated: {result.created_at}</Text>
                </View>
              ))}
            </View>
          
        </View>
        </ScrollView>
      )}
    </View>
  );
}

export default SearchResults;