import Constants from 'expo-constants';

const API_URL = Constants.expoConfig.extra.API_URL || 'http://localhost:8000';

async function searchDocuments(query, numResults) {
  const encoded_query = encodeURIComponent(query);
  const response = await fetch(`${API_URL}/search?query=${encoded_query}&num_results=${numResults}`);
  const data = await response.json();
  return data;
}

async function searchQuestions(question, numResults) {
  const encoded_query = encodeURIComponent(question);
  const response = await fetch(`${API_URL}/question?question=${encoded_query}&num_results=${numResults}`);
  const data = await response.json();
  return data;
}

export { searchDocuments, searchQuestions };