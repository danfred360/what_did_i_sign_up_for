import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, Pressable } from 'react-native';
import signInStyles from '../styles/signInStyles';
import mainStyles from '../styles/main';
import base64 from 'base-64';
import Constants from 'expo-constants';

const SignInPage = ({ onTokenReceived }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showSignUp, setShowSignUp] = useState(false);
  const AUTH_URL = Constants.expoConfig.extra.AUTH_URL || 'http://localhost:8001/token';

  const handleSignIn = async () => {
    try {
      const response = await fetch(`${AUTH_URL}/token`, {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${base64.encode(`${username}:${password}`)}`
        }
      });

      if (response.status === 401) {
        setError('Invalid username or password');
        return;
      }

      const data = await response.json();
      onTokenReceived(data.access_token);

    } catch (error) {
      setError('An error occurred. Please try again later.');
    }
  };

  const handleSignUp = async () => {
    try {
      const response = await fetch(`${AUTH_URL}/create_user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.status !== 200) {
        setError('Sign up failed');
        return;
      }

      const data = await response.json();
      onTokenReceived(data.access_token);

    } catch (error) {
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <SafeAreaView style={mainStyles.parent_container}>
      <View style={mainStyles.form_area}>
      <Text style={mainStyles.title}>{showSignUp ? 'SIGN UP' : 'SIGN IN'}</Text>
        <View style={mainStyles.form_group}>
          <TextInput
            style={mainStyles.form_style}
            autoCapitalize="none"
            placeholder="Username"
            value={username}
            onChangeText={setUsername}
          />
        </View>
        <View style={mainStyles.form_group}>
          <TextInput
            style={mainStyles.form_style}
            autoCapitalize="none"
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
        </View>
        <View style={mainStyles.form_group_horizontal}>
          <Pressable style={mainStyles.btn} onPress={showSignUp ? handleSignUp : handleSignIn}>
            <Text style={mainStyles.text}>{showSignUp ? 'Sign Up' : 'Sign In'}</Text>
          </Pressable>
          <Pressable style={mainStyles.btn} onPress={() => setShowSignUp(!showSignUp)}>
            <Text style={mainStyles.text}>
              {showSignUp ? 'Switch to Sign In' : 'Switch to Sign Up'}</Text>
          </Pressable>
          {error ? (
            <View style={signInStyles.errorCard}>
              <Text style={signInStyles.errorText}>{error}</Text>
            </View>
          ) : null}
        </View>
      </View>
    </SafeAreaView>
  );
};

export default SignInPage;
