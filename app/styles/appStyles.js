import { StyleSheet, Dimensions, Platform } from 'react-native';

const windowHeight = Dimensions.get('window').height;
const windowWidth = Dimensions.get('window').width - 40;;

const appStyles = StyleSheet.create({
  parentContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#D1C4E9',
    padding: Platform.select({
      ios: 40,
      android: 20,
      web: 40,
      default: 20,
    }),
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
    width: windowWidth,
    alignSelf: 'center',
    maxHeight: windowHeight - 100,
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
  button: {
    backgroundColor: '#FFEB3B',
    fontWeight: 'bold',
  },
  buttonContainer: {
    backgroundColor: '#FFEB3B',
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 10,
    justifyContent: 'center',
    alignItems: 'center',
    width: 100,
  },
});

export default appStyles;