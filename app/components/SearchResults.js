import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import mainStyles from '../styles/main';

function SearchResults({ results }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (!results || !results.results) {
    return null;
  }

  const handleToggleCollapse = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <View style={mainStyles.form_area}>
      <View style={[mainStyles.form_group, isCollapsed ? mainStyles.fixed_container : mainStyles.expandable_container]}>
        <View style={mainStyles.form_header}>
          <Text style={mainStyles.title}>SEARCH RESULTS</Text>
          <TouchableOpacity style={mainStyles.btn} onPress={handleToggleCollapse}>
            <Text style={mainStyles.text}>{isCollapsed ? 'Expand' : 'Collapse'}</Text>
          </TouchableOpacity>
        </View>
        <View style={[mainStyles.form_group, isCollapsed ? mainStyles.fixed_container : mainStyles.expandable_container]}>
          <Text style={mainStyles.countLabel}>Count: {results.count}</Text>
          {/* <ScrollView> */}
          {results.results.map((result) => (
            <View key={result.id} style={mainStyles.item}>
              <Text style={mainStyles.text}>Document ID: {result.document_id}</Text>
              <Text style={mainStyles.paragraph}>{result.content}</Text>
              <Text style={mainStyles.text}>Updated: {result.created_at}</Text>
            </View>
          ))}
          {/* </ScrollView> */}
          <TouchableOpacity style={mainStyles.btn} onPress={handleToggleCollapse}>
            <Text style={mainStyles.text}>{isCollapsed ? 'Expand' : 'Collapse'}</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

export default SearchResults;
