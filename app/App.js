import React, { useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import Home from './views/Home';
import About from './views/About';
import Files from './views/Files';
import SignIn from './views/SignIn';

const Drawer = createDrawerNavigator();

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
    <NavigationContainer>
      <Drawer.Navigator initialRouteName="Home">
        <Drawer.Screen name="Home" component={Home} />
        <Drawer.Screen name="Files" component={Files} />
        <Drawer.Screen name="About" component={About} />
        <Drawer.Screen name="Sign Out" component={() => {
          handleSignOut();
          return null;
        }} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}
