import React, { useState } from 'react';
import { View, Text, Pressable } from 'react-native';
import mainStyles from '../styles/main';

export default function SettingsTray({ handleSignOut }) {
  const [isTrayOpen, setIsTrayOpen] = useState(false);

  return (
    <View style={mainStyles.settingsTrayContainer}>
      <Pressable onPress={() => setIsTrayOpen(!isTrayOpen)} style={mainStyles.settingsButton}>
        <Text style={mainStyles.settingsButtonText}>≡</Text>
      </Pressable>
      {isTrayOpen && (
        <View style={mainStyles.settings_area}>
          <Pressable onPress={handleSignOut} style={mainStyles.trayMenuItem}>
            <Text>Sign Out</Text>
          </Pressable>
          <Pressable onPress={() => console.log('foo')} style={mainStyles.trayMenuItem}>
            <Text>About</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}
