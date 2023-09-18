import React, { useEffect, useState } from 'react';
import { View, Text, Pressable, TextInput, ScrollView } from 'react-native';
import { listCollections, createCollection } from '../utils/api';
import mainStyles from '../styles/main';

export default function CollectionTray({ setSelectedCollectionId }) {
    const [collections, setCollections] = useState([]);
    const [activeCollectionId, setActiveCollectionId] = useState(null);
    const [showForm, setShowForm] = useState(false);
    const [newCollectionName, setNewCollectionName] = useState('');
    const [response, setResponse] = useState(null);

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const collectionData = await listCollections();
                setCollections(collectionData);
                setActiveCollectionId(collectionData[0]?.id);
                setSelectedCollectionId(collectionData[0]?.id);
            } catch (error) {
                console.error("Failed to fetch collections:", error);
            }
        };

        fetchCollections();
    }, []);

    const handleSelectCollection = (id) => {
        setActiveCollectionId(id);
        setSelectedCollectionId(id);
    };

    const handleSubmit = async () => {
        try {
            const newCollection = await createCollection(newCollectionName);
            setCollections([...collections, newCollection]);
            setResponse(`Collection added: ${newCollection.name}`);
            setNewCollectionName('');
            setShowForm(false);
        } catch (error) {
            console.error("Failed to add collection:", error);
        }
    };

    return (
        <View style={mainStyles.form_area}>
            <Text style={mainStyles.title}>COLLECTIONS</Text>
            <View style={mainStyles.form_group_horizontal}>
                <ScrollView horizontal={true}>
                {collections.map((collection) => (
                    <Pressable
                        key={collection.id}
                        onPress={() => handleSelectCollection(collection.id)}
                        style={activeCollectionId === collection.id ? mainStyles.btn_active : mainStyles.btn}
                    >
                        <Text style={mainStyles.text}>{collection.name}</Text>
                    </Pressable>
                ))}
                <Pressable onPress={() => setShowForm(!showForm)} style={mainStyles.btn}>
                    <Text style={mainStyles.text}>+</Text>
                </Pressable>
                </ScrollView>
            </View>
            <View style={mainStyles.form_group}>
                {showForm && (
                    <View>
                        <TextInput
                            placeholder="Enter new collection name"
                            value={newCollectionName}
                            onChangeText={setNewCollectionName}
                            style={mainStyles.form_style}
                        />
                        <Pressable onPress={handleSubmit} style={mainStyles.btn}>
                            <Text style={mainStyles.text}>Submit</Text>
                        </Pressable>
                        {response && <Text>{response}</Text>}
                    </View>
                )}
            </View>
        </View>
    );
}
