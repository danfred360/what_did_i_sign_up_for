import { StyleSheet } from 'react-native';

const appStyles = StyleSheet.create({
  parentContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#D1C4E9', // light purple background
    padding: 20,
  },
  container: {
    backgroundColor: '#B39DDB', // slightly darker purple
    borderRadius: 20,
    padding: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  searchButton: {
    backgroundColor: '#FFEB3B', // yellow button
    borderRadius: 20,
    paddingHorizontal: 10,
  },
  resultsContainer: {
    backgroundColor: '#E0E0E0', // grey result items
    borderRadius: 20,
    padding: 10,
    margin: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
});

export default appStyles;