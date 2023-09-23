import React, { useState, useEffect } from 'react';
import { SafeAreaView, ScrollView, View, Text, FlatList } from 'react-native';
import appStyles from '../styles/appStyles';

const Files = () => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/files')
      .then(response => response.json())
      .then(data => setFiles(data))
      .catch(error => console.error(error));
  }, []);

  return (
    <SafeAreaView style={appStyles.parentContainer}>
        <ScrollView>
            <View style={appStyles.container}>
                <Text>Files</Text>
                <FlatList
                    data={files}
                    keyExtractor={item => item.id.toString()}
                    renderItem={({ item }) => (
                    <View>
                        <Text>{item.name}</Text>
                        <Text>{item.description}</Text>
                    </View>
                    )}
                />
            </View>
        </ScrollView>
    </SafeAreaView>
  );
};

export default Files;