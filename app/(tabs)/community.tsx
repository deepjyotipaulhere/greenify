import Ionicons from '@expo/vector-icons/Ionicons';
import { Button, Layout, ListItem, useTheme } from '@ui-kitten/components';
import { Image } from 'expo-image';
import { useState } from 'react';
import { ScrollView, StyleSheet, useWindowDimensions } from 'react-native';

export default function TabTwoScreen() {
	const { width } = useWindowDimensions()
	const theme = useTheme()

	const [loading, setLoading] = useState(false)

	const startMatching = () => {
		fetch("https://greenify-service-g0fre7fva8fxcmhs.centralindia-01.azurewebsites.net/community", {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'Accept': 'application/json',
			},
			body: JSON.stringify({
				users: [
					{ name: 'User', plants: ['Gulmohar Tree', 'Oak Tree', 'Cashew Tree'] },
					{ name: 'Jonathan', plants: ['Aloe Vera', 'Amaranth', 'Angel Trumpet'] },
					{ name: 'Shyamal', plants: ['Bamboo', 'Cacao', 'Coffee'] },
					{ name: 'Daniel', plants: ['Cotton', 'Olive', 'Oil Palm'] },
				]
			})
		}).then(response => response.json()).then(data => {
			console.log(data);
		})
	}

	return (
		<ScrollView>
			<Layout style={{ flex: 1 }}>
				<Image source={require('../../assets/images/community.png')} style={{ width: width, height: 300 }} contentFit='cover' />
				<ListItem title='Me' description='A set of React Native components' accessoryLeft={props => <Ionicons name="person-circle" size={32} color={theme['color-primary-default']} />} />
				<ListItem title='Jonathan' description='100m away' />
			</Layout>
			<Button style={{ margin: 15 }} onPress={startMatching}>Start Matching</Button>
		</ScrollView>
	);
}

const styles = StyleSheet.create({
	headerImage: {
		color: '#808080',
		bottom: -90,
		left: -35,
		position: 'absolute',
	},
	titleContainer: {
		flexDirection: 'row',
		gap: 8,
	},
});
