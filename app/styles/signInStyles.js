import { StyleSheet } from 'react-native';

const signInStyles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 24,
    textAlign: 'center',
  },
  form: {
    width: '80%',
    alignItems: 'center',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 8,
    paddingHorizontal: 10,
    marginVertical: 8,
    width: '100%',
  },
  buttonContainer: {
    backgroundColor: '#FFEB3B',
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 10,
    justifyContent: 'center',
    alignItems: 'center',
    width: 100,
    width: '100%',
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#007bff',
    borderRadius: 4,
    padding: 12,
    marginVertical: 8,
    width: '100%',
    alignItems: 'center',
    textAlign: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  errorCard: {
    backgroundColor: '#f8d7da',
    borderWidth: 1,
    borderColor: '#f5c6cb',
    borderRadius: 4,
    padding: 8,
    marginTop: 8,
  },
  errorText: {
    color: '#721c24',
    fontSize: 14,
  },
});

export default signInStyles;