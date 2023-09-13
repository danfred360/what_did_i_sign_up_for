import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity } from 'react-native';
import appStyles from '../styles/appStyles';

const SignInPage = ({ onSignIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = () => {
    onSignIn(username, password);
  };

  return (
    <View style={appStyles.container}>
      <Text>Sign In</Text>
      <TextInput
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TouchableOpacity onPress={handleSubmit}>
        <Text>Sign In</Text>
      </TouchableOpacity>
    </View>
  );
};

export default SignInPage;