import React, { useState } from 'react';
import { SafeAreaView, View, Text, TextInput, TouchableOpacity } from 'react-native';
import appStyles from '../styles/appStyles';
import signInStyles from '../styles/signInStyles';

const SignInPage = ({ onSignIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    onSignIn(username, password);
  };

  return (
    <SafeAreaView style={appStyles.parentContainer}>
      <View style={appStyles.container}>
        <Text style={signInStyles.title}>Sign In</Text>
        <TextInput
          style={signInStyles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
        />
        <TextInput
          style={signInStyles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />
        <TouchableOpacity onPress={handleSubmit}>
          <Text style={signInStyles.button}>Sign In</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

export default SignInPage;