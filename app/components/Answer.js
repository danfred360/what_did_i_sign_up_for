import { useState, useRef } from 'react';
import { View, Text, Pressable, ScrollView } from 'react-native';
import resultStyles from '../styles/resultStyles';
import appStyles from '../styles/appStyles'

function Answer({ answer, isCollapsed, setIsCollapsed }) {
  const [maxHeight, setMaxHeight] = useState(undefined);
  const contentRef = useRef(null);

  const handleCollapse = () => {
    setIsCollapsed(!isCollapsed)
    handleLayout;
  };

  const handleLayout = () => {
    if (contentRef.current) {
      const height = contentRef.current.clientHeight;
      setMaxHeight(height + 40); // add some extra padding to the height
    }
  };

  return (
    <View style={[resultStyles.resultsContainer, { maxHeight }]}>
      <View style={resultStyles.resultsHeader}>
        <Text style={resultStyles.title}>Answer</Text>
        {/* <Pressable style={appStyles.buttonContainer} onPress={handleCollapse}>
            <Text style={appStyles.button}>{isCollapsed ? "Expand" : "Collapse"}</Text>
        </Pressable> */}
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