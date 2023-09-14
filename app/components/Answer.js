import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import resultStyles from '../styles/resultStyles';
import appStyles from '../styles/appStyles'

function Answer({ answer, isCollapsed, setIsCollapsed }) {
  return (
    <View style={resultStyles.resultsContainer}>
      <View style={resultStyles.resultsHeader}>
        <Text style={resultStyles.title}>Answer</Text>
        <TouchableOpacity style={appStyles.buttonContainer} onPress={() => setIsCollapsed(!isCollapsed)}>
            <Text style={appStyles.button}>{isCollapsed ? "Expand" : "Collapse"}</Text>
        </TouchableOpacity>
      </View>
      {!isCollapsed && (
        <ScrollView>
          <View style={resultStyles.result}>
            <Text style={resultStyles.content}>{answer}</Text>
          </View>
        </ScrollView>
      )}
    </View>
  );
}

export default Answer;