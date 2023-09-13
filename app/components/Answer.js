import React from 'react';
import { View, Text, Button } from 'react-native';
import resultStyles from '../styles/resultStyles';

function Answer({ answer, isCollapsed, setIsCollapsed }) {
  return (
    <View style={resultStyles.resultsContainer}>
      <View style={resultStyles.resultsHeader}>
        <Text style={resultStyles.title}>Answer:</Text>
        <Button title={isCollapsed ? "Expand" : "Collapse"} onPress={() => setIsCollapsed(!isCollapsed)} />
      </View>
      {!isCollapsed && (
        <Text style={resultStyles.content}>{answer}</Text>
      )}
    </View>
  );
}

export default Answer;