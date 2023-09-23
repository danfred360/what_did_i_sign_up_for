import Constants from 'expo-constants';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = Constants.expoConfig.extra.API_URL || 'http://localhost:8000';

async function listCollections() {
  const storedToken = await AsyncStorage.getItem('token');
  const response = await fetch(`${API_URL}/collections`, {
    headers: {
      'Authorization': `Bearer ${storedToken}`
    }
  });
  const data = await response.json();
  return data;
}

async function createCollection(name) {
  try {
    const storedToken = await AsyncStorage.getItem('token');
    const response = await fetch(`${API_URL}/collections`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${storedToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, 'description': 'changeme' }),
    });
    const data = await response.json();
    return data;
  } catch(error) {
    console.error('An error occurred creating collection:', error);
  }
}

async function loadFile(collectionId, url) {
  try {
    const storedToken = await AsyncStorage.getItem('token');
    const response = await fetch(
      `${API_URL}/collections/${collectionId}/load_url?url=${encodeURIComponent(url)}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${storedToken}`,
        },
      }
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('An error occurred loading file:', error);
  }
}

async function searchDocuments(query, numResults, collectionId) {
  const storedToken = await AsyncStorage.getItem('token');
  const encoded_query = encodeURIComponent(query);
  const response = await fetch(`${API_URL}/collections/${collectionId}/search?query=${encoded_query}&num_results=${numResults}`, {
    headers: {
      'Authorization': `Bearer ${storedToken}`
    }
  });
  const data = await response.json();
  return data;
}

async function searchQuestions(question, numResults, collectionId) {
  const storedToken = await AsyncStorage.getItem('token');
  const encoded_query = encodeURIComponent(question);
  const response = await fetch(`${API_URL}/collections/${collectionId}/question?question=${encoded_query}&num_results=${numResults}`, {
    headers: {
      'Authorization': `Bearer ${storedToken}`
    }
  });
  const data = await response.json();
  return data;
}

export { listCollections, createCollection, loadFile, searchDocuments, searchQuestions };