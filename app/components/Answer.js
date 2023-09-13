import React from 'react';
import { View, Text, Button } from 'react-native';
import resultStyles from '../styles/resultStyles';

function Answer({ answer, isCollapsed, setIsCollapsed }) {
  return (
    <View style={resultStyles.resultsContainer}>
      <Text style={resultStyles.content}>{answer}</Text>
    </View>
  );
}

export default Answer;