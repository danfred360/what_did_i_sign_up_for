import { useState, useRef } from 'react';
import { View, Text, Pressable, ScrollView } from 'react-native';
import resultStyles from '../styles/resultStyles';
import mainStyles from '../styles/main';

function Answer({ answer }) {
  const [maxHeight, setMaxHeight] = useState(undefined);
  const contentRef = useRef(null);
  const [isCollapsed, setIsCollapsed] = useState(false);

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
    <View style={mainStyles.form_area}>
      <View style={[mainStyles.form_group, isCollapsed ? mainStyles.fixed_container : mainStyles.expandable_container]}>
        <View style={mainStyles.form_header}>
          <Text style={mainStyles.sub_title}>Answer</Text>
          {/* <Pressable style={appStyles.buttonContainer} onPress={handleCollapse}>
            <Text style={appStyles.button}>{isCollapsed ? "Expand" : "Collapse"}</Text>
        </Pressable> */}
        </View>
        {!isCollapsed && (
          <ScrollView>
            <View style={mainStyles.item}>
              <Text style={mainStyles.paragraph}>{answer}</Text>
            </View>
          </ScrollView>
        )}
      </View>
    </View>
  );
}

export default Answer;