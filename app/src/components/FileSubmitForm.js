import React, { useState } from 'react';
import {
    View,
    TextInput,
    Text,
    Pressable,
    ActivityIndicator
} from 'react-native';
import mainStyles from '../styles/main';
import { loadFile } from '../utils/api';

export default function FileSubmitForm({ collectionId }) {
    const [showForm, setShowForm] = useState(false);
    const [url, setUrl] = useState('');
    const [response, setResponse] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async () => {
        setResponse('');
        setIsLoading(true);
        const response = await loadFile(collectionId, url);
        setResponse(response);
        console.log(response);
        setIsLoading(false);
    };

    return (
        <View style={mainStyles.form_area}>
            <Text style={mainStyles.title}>ADD A FILE</Text>
            
                <Pressable onPress={() => setShowForm(!showForm)} style={mainStyles.btn}>
                    <Text style={mainStyles.text}>{showForm ? '-' : '+'}</Text>
                </Pressable>
                {showForm && (
                    <View>
                        <View style={mainStyles.form_group_horizontal}>
                        <TextInput
                            placeholder="Enter a URL"
                            value={url}
                            onChangeText={setUrl}
                            style={mainStyles.form_style}
                        />
                        <Pressable onPress={handleSubmit} style={mainStyles.btn}>
                            <Text style={mainStyles.text}>Submit</Text>
                        </Pressable>
                        </View>
                        {isLoading && (
                            <ActivityIndicator style={mainStyles.loading} />
                        )}
                        {response && (
                            <View style={mainStyles.item}>
                                <Text style={mainStyles.sub_title}>{response.name}</Text>
                                <Text style={mainStyles.text}>Description: </Text>
                                <Text style={mainStyles.paragraph}>{response.description}</Text>
                                <Text style={mainStyles.text}>Created: </Text>
                                <Text style={mainStyles.paragraph}>{response.created_at}</Text>
                            </View>
                        )}
                    </View>
                )}
        </View>
    );
};
