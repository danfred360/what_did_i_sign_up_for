import React from 'react';
import { View, Text, Button } from 'react-native';
import resultStyles from '../styles/resultStyles';

function SearchResults({ results, isCollapsed, setIsCollapsed }) {
  if (!results || !results.results) {
    return null;
  }

  return (
    <View style={resultStyles.resultsContainer}>
      <View style={resultStyles.resultsHeader}>
        <Text style={resultStyles.title}>Search Results:</Text>
        <Button title={isCollapsed ? "Expand" : "Collapse"} onPress={() => setIsCollapsed(!isCollapsed)} />
      </View>
      {!isCollapsed && (
        <>
          <Text style={resultStyles.count}>Count: {results.count}</Text>
          {results.results.map((result) => (
            <View key={result.id} style={resultStyles.result}>
              <Text>ID: {result.id}</Text>
              <Text>Document ID: {result.document_id}</Text>
              <Text style={resultStyles.content}>Content: {result.content}</Text>
              <Text>Created At: {result.created_at}</Text>
            </View>
          ))}
        </>
      )}
    </View>
  );
}

export default SearchResults;