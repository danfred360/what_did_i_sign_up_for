import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import Home from './views/Home';
import About from './views/About';
import Files from './views/Files';
import SignIn from './views/SignIn';

const Drawer = createDrawerNavigator();

export default function App() {
  const [token, setToken] = useState(null);

  const handleSignIn = async (username, password) => {
    const response = await fetch('http://localhost:8001/token', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${btoa(`${username}:${password}`)}`
      }
    });
    const data = await response.json();
    setToken(data.access_token);
  }

  if (!token) {
    return (
      <SignIn onSignIn={handleSignIn} />
    );
  }

  return (
    <NavigationContainer>
      <Drawer.Navigator initialRouteName="Home">
        <Drawer.Screen name="Home" component={Home} />
        <Drawer.Screen name="Files" component={Files} />
        <Drawer.Screen name="About" component={About} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}