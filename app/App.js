import { useState, useEffect } from 'react';
import { SafeAreaView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Home from './screens/Home';
import SignIn from './screens/SignIn';
import mainStyles from './styles/main'; 
import SettingsTray from './components/SettingsTray';


export default function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const fetchToken = async () => {
      const storedToken = await AsyncStorage.getItem('token');
      if (storedToken) {
        setToken(storedToken);
      }
    };
    fetchToken();
  }, []);

  const storeToken = async (value) => {
    await AsyncStorage.setItem('token', value);
    setToken(value);
  };

  const handleSignOut = async () => {
    await AsyncStorage.removeItem('token');
    setToken(null);
  };

  if (!token) {
    return (
      <SignIn onTokenReceived={storeToken} />
    );
  }

  return (
    <SafeAreaView style={mainStyles.parent_container}>
      <SettingsTray handleSignOut={handleSignOut} />
      <Home handleSignOut={handleSignOut} />
    </SafeAreaView>
  );
}
