import Constants from 'expo-constants';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = Constants.expoConfig.extra.API_URL || 'http://localhost:8000';

async function searchDocuments(query, numResults) {
  const storedToken = await AsyncStorage.getItem('token');
  const encoded_query = encodeURIComponent(query);
  const response = await fetch(`${API_URL}/search?query=${encoded_query}&num_results=${numResults}`, {
    headers: {
      'Authorization': `Bearer ${storedToken}`
    }
  });
  const data = await response.json();
  return data;
}

async function searchQuestions(question, numResults) {
  const storedToken = await AsyncStorage.getItem('token');
  const encoded_query = encodeURIComponent(question);
  const response = await fetch(`${API_URL}/question?question=${encoded_query}&num_results=${numResults}`, {
    headers: {
      'Authorization': `Bearer ${storedToken}`
    }
  });
  const data = await response.json();
  return data;
}

export { searchDocuments, searchQuestions };