import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { listCollections } from '../utils/api';
import mainStyles from '../styles/main';

export default function CollectionTray({ setSelectedCollectionId }) {
  const [collections, setCollections] = useState([]);
  const [activeCollectionId, setActiveCollectionId] = useState(null);

  useEffect(() => {
    const fetchCollections = async () => {
      try {
        const collectionData = await listCollections();
        setCollections(collectionData);
        setActiveCollectionId(collectionData[0].id);
        setSelectedCollectionId(collectionData[0].id);
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

  return (
    <View style={mainStyles.collectionTray}>
      {collections.map((collection) => (
        <TouchableOpacity
          key={collection.id}
          onPress={() => handleSelectCollection(collection.id)}
          style={activeCollectionId === collection.id ? mainStyles.collectionItemActive : mainStyles.collectionItem}
        >
          <Text style={mainStyles.text}>{collection.name}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}
