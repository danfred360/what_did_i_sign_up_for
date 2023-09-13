import { StyleSheet, Platform, Dimensions } from 'react-native';

const windowWidth = Dimensions.get('window').width;
const searchBarWidth = windowWidth - 40;

const searchStyles = StyleSheet.create({
  searchContainer: {
    flexDirection: 'row',
    marginBottom: 10,
    borderRadius: 20,
    overflow: 'hidden',
    ...Platform.select({
      ios: {
        borderWidth: 1,
        borderColor: 'gray',
      },
      android: {
        borderColor: 'gray',
        borderWidth: 1,
      },
    }),
  },
  searchBar: {
    flex: 1,
    height: 40,
    paddingHorizontal: 10,
    borderRadius: 20,
    marginRight: 10,
    backgroundColor: '#f2f2f2',
    ...Platform.select({
      ios: {
        borderWidth: 1,
        borderColor: 'gray',
      },
      android: {
        borderColor: 'gray',
        borderWidth: 1,
      },
    }),
  },
  searchButton: {
    borderRadius: 20,
    paddingHorizontal: 10,
  },
  loading: {
    marginTop: 20,
  },
});

export default searchStyles;