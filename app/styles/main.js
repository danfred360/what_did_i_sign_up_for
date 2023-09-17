import { StyleSheet, Dimensions, Platform } from 'react-native';

const mainStyles = StyleSheet.create({
    parent_container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#D1C4E9',
        padding: Platform.select({
            ios: 40,
            android: 20,
            web: 40,
            default: 20,
        }),
    },
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#7b4397',
    },
    fixed_container: {
        maxHeight: 125,
        overflow: 'hidden',
    },
    expandable_container: {
        maxHeight: 'auto',
    },
    form_area: {
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
        borderRadius: 20,
        shadowColor: '#52206b',
        shadowOffset: {
            width: 30,
            height: 35,
        },
        shadowOpacity: 0.2,
        shadowRadius: 2,
        width: '90%',
        margin: Platform.select({
            ios: 20,
            android: 20,
            web: 20,
            default: 20,
        }),
    },
    form_area_dynamic_width: {
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
        borderRadius: 20,
        shadowColor: '#52206b',
        shadowOffset: {
            width: 30,
            height: 35,
        },
        shadowOpacity: 0.2,
        shadowRadius: 2,
        flex: 1,
        margin: Platform.select({
            ios: 40,
            android: 20,
            web: 40,
            default: 20,
        }),
    },
    settings_area: {
        position: 'absolute',
        right: 20, // Positioned to the right of the settings button
        top: 0, // Aligns to the top of the settings button
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
        borderRadius: 20,
        shadowColor: '#52206b',
        shadowOffset: {
            width: 30,
            height: 35,
        },
        shadowOpacity: 0.2,
        shadowRadius: 2,
        width: 100,
        margin: Platform.select({
            ios: 40,
            android: 40,
            web: 40,
            default: 20,
        }),
    },
    item: {
        backgroundColor: '#E0E0E0',
        borderRadius: 20,
        padding: 10,
        margin: 10,
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    title: {
        color: '#7b4397',
        fontWeight: '900',
        fontSize: 24,
        marginTop: 20,
    },
    sub_title: {
        fontWeight: '600',
        marginVertical: 5,
    },
    text: {
        fontSize: 16,
        color: '#333',
    },
    paragraph: {
        margin: 20,
    },
    link: {
        fontWeight: '800',
    },
    form_group: {
        flexDirection: 'column',
        alignItems: 'baseline',
        margin: 20,
        justifyContent: 'flex-start',
    },
    form_style: {
        borderWidth: 2,
        borderColor: '#000',
        shadowColor: '#000',
        shadowOffset: {
            width: 3,
            height: 4,
        },
        shadowOpacity: 1,
        width: 290,
        padding: 12,
        borderRadius: 4,
        fontSize: 15,
    },
    form_style_focused: {
        translateY: 4,
        shadowOffset: {
            width: 1,
            height: 2,
        },
    },
    btn: {
        padding: 15,
        marginVertical: 30,
        width: 310,
        fontSize: 15,
        backgroundColor: '#7b4397',
        borderRadius: 30,
        fontWeight: '800',
        shadowColor: '#000',
        shadowOffset: {
            width: 5,
            height: 5,
        },
        shadowOpacity: 1,
    },
    btn_focused: {
        translateY: 4,
        shadowOffset: {
            width: 1,
            height: 2,
        },
    },
    toggleButtonGroup: {
        flexDirection: 'row',
        marginBottom: 20,
    },
    toggleButton: {
        padding: 10,
        borderRadius: 4,
        marginHorizontal: 10,
        backgroundColor: '#ccc',
    },
    toggleButtonActive: {
        backgroundColor: '#7b4397',
    },
    settingsTrayContainer: {
        position: 'absolute',
        top: Platform.select({
            ios: 60,
            android: 20,
            web: 40,
            default: 20,
        }),
        right: 20,  // Padding from right
        zIndex: 1,
      },
      settingsButton: {
        backgroundColor: 'gray',
        width: 50,
        height: 50,
        borderRadius: 25,
        justifyContent: 'center',
        alignItems: 'center',
      },
      settingsButtonText: {
        color: 'white',
        fontSize: 24,
      },
      trayMenu: {
        backgroundColor: 'white',
        width: '100%',
        borderRadius: 10,
      },
      trayMenuItem: {
        padding: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
      },
      collectionTray: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#fff',
        borderRadius: 20,
        margin: Platform.select({
          ios: 40,
          android: 20,
          web: 40,
          default: 20,
        }),
      },
      collectionItem: {
        backgroundColor: '#E0E0E0',
        borderRadius: 50,
        padding: 20,
        margin: 10,
      },
      collectionItemActive: {
        backgroundColor: '#7b4397',
        borderRadius: 50,
        padding: 20,
        margin: 10,
      },
});

export default mainStyles;