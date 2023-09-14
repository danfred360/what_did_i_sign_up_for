import { StyleSheet, Dimensions } from 'react-native';

const windowWidth = Dimensions.get('window').width;
const searchBarWidth = windowWidth - 40;

const searchStyles = StyleSheet.create({
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginVertical: 10,
    padding: 10,
    paddingHorizontal: 20,
    width: searchBarWidth,
  },
  searchBar: {
    flex: 1,
    height: 40,
    borderRadius: 20,
    paddingHorizontal: 10,
    backgroundColor: '#fff',
    marginRight: 10,
  },
  searchButton: {
    width: 80,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'yellow',
    justifyContent: 'center',
    alignItems: 'center',
  },
  searchButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  loading: {
    marginTop: 20,
    marginBottom: 20,
  },
});

export default searchStyles;