import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, TouchableOpacity } from 'react-native';
import appStyles from '../styles/appStyles';
import signInStyles from '../styles/signInStyles';
import base64 from 'base-64';

const SignInPage = ({ onTokenReceived }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:8001/token', {
        method: 'POST',
        headers: {
          'Authorization': `Basic ${base64.encode(`${username}:${password}`)}`        }
      });

      if (response.status === 401) {
        setError('Invalid username or password');
        return;
      }

      const data = await response.json();
      onTokenReceived(data.access_token);

    } catch (error) {
      console.log(error);
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <SafeAreaView style={appStyles.parentContainer}>
      <View style={appStyles.container}>
        {/* <Text style={signInStyles.title}>Sign In</Text> */}
        <TextInput
          style={signInStyles.input}
          autoCapitalize="none"
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          style={signInStyles.input}
          autoCapitalize="none"
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <TouchableOpacity style={signInStyles.buttonContainer} onPress={handleSubmit}>
          <Text style={appStyles.button}>Sign In</Text>
        </TouchableOpacity>
        {error ? (
          <View style={signInStyles.errorCard}>
            <Text style={signInStyles.errorText}>{error}</Text>
          </View>
        ) : null}
      </View>
    </SafeAreaView>
  );
};

export default SignInPage;
