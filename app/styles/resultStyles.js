import { StyleSheet } from 'react-native';

const resultStyles = StyleSheet.create({
  resultsContainer: {
    backgroundColor: '#fff',
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
    maxHeight: '80%', // add this line to limit the height of the container
    width: '100%',
  },
  resultsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  count: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  result: {
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
  content: {
    fontStyle: 'italic',
  },
  scrollContainer: {
    flex: 1,
  },
});

export default resultStyles;