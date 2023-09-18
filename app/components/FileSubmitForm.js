import React, { useState } from 'react';
import {
    View,
    TextInput,
    Pressable,
    Text,
    TouchableOpacity,
} from 'react-native';
import mainStyles from '../styles/main';
import { loadFile } from '../utils/api';

export default function FileSubmitForm({ collectionId }) {
    const [showForm, setShowForm] = useState(false);
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState(null);

    const handleSubmit = async () => {
        const response = loadFile(collectionId, url);
        setResponse(response);
    };

    return (
        <View style={mainStyles.form_area}>
            <Text style={mainStyles.title}>ADD A FILE</Text>
            <View style={mainStyles.form_group}>
                <TouchableOpacity onPress={() => setShowForm(!showForm)} style={mainStyles.btn}>
                    <Text style={mainStyles.text}>+</Text>
                </TouchableOpacity>
                {showForm && (
                    <View>
                        <TextInput
                            placeholder="Enter a URL"
                            value={url}
                            onChangeText={setUrl}
                            style={mainStyles.form_style}
                        />
                        <Pressable onPress={handleSubmit} style={mainStyles.btn}>
                            <Text style={mainStyles.text}>Submit</Text>
                        </Pressable>
                        {response && <Text>File Added: {response.name}</Text>}
                    </View>
                )}
            </View>
        </View>
    );
};
