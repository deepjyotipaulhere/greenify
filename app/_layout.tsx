import { useColorScheme } from '@/hooks/useColorScheme';
import * as eva from '@eva-design/eva';
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { ApplicationProvider } from '@ui-kitten/components';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';
import { default as theme } from '../constants/custom-theme.json'; // <-- Import app theme

export default function RootLayout() {
	const colorScheme = useColorScheme();
	const [loaded] = useFonts({
		SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
	});

	if (!loaded) {
		// Async font loading only occurs in development.
		return null;
	}

	return (
		<ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
			<ApplicationProvider {...eva} theme={{ ...eva.dark, ...theme }}>
				<Stack>
					<Stack.Screen name="(tabs)" options={{ headerShown: false }} />
					<Stack.Screen name="+not-found" />
				</Stack>
				<StatusBar style="auto" />
			</ApplicationProvider>
		</ThemeProvider>
	);
}
