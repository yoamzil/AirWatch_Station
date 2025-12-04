import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Thermometer, Droplets, Wind, BarChart3, Bot, Leaf } from "lucide-react";
import { useState, useEffect } from "react";

const THINGSBOARD_BASE = "http://localhost:9090/api";
const DEVICE_ID = "da8c8990-cfbc-11f0-8614-c1208bd774e4";
const USERNAME = "tenant@thingsboard.org";
const PASSWORD = "tenant";

// Helper to safely parse telemetry values
const parseValue = (arr: any[]) => arr?.[0]?.value != null ? Number(arr[0].value) : 0;

export const useAirQualityData = () => {
	const [data, setData] = useState({
		temperature: 0,
		humidity: 0,
		airQuality: 0,
		status: "Unknown",
	});

	useEffect(() => {
		let interval: ReturnType<typeof setInterval>;

		const fetchData = async () => {
			try {
				// Step 1: Get JWT token
				const loginRes = await fetch(`${THINGSBOARD_BASE}/auth/login`, {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ username: USERNAME, password: PASSWORD }),
				});
				const loginData = await loginRes.json();
				const token = loginData.token;
				if (!token) throw new Error("No JWT token returned");

				// Step 2: Fetch latest telemetry
				const telemetryRes = await fetch(
					`${THINGSBOARD_BASE}/plugins/telemetry/DEVICE/${DEVICE_ID}/values/timeseries?keys=temperature,humidity,airQuality`,
					{
						headers: { "X-Authorization": `Bearer ${token}` },
					}
				);
				const telemetry = await telemetryRes.json();

				// Step 3: Parse values safely
				const temperature = parseValue(telemetry.temperature);
				const humidity = parseValue(telemetry.humidity);
				const airQuality = parseValue(telemetry.airQuality);

				// Step 4: Determine airQuality status
				const status =
					airQuality === 0
						? "Unknown"
						: airQuality <= 50
							? "Good"
							: airQuality <= 100
								? "Moderate"
								: "Poor";

				// Update state
				setData({ temperature, humidity, airQuality, status });
			} catch (err) {
				console.error("Error fetching ThingsBoard telemetry:", err);
			}
		};

		// Fetch immediately and then every 5 seconds
		fetchData();
		interval = setInterval(fetchData, 5000);

		return () => clearInterval(interval);
	}, []);

	return data;
};


const getairQualityColor = (airQuality: number) => {
	if (airQuality <= 50) return "text-primary";
	if (airQuality <= 100) return "text-yellow-500";
	if (airQuality <= 150) return "text-orange-500";
	return "text-destructive";
};

const Index = () => {
	const airData = useAirQualityData();

	return (
		<div className="min-h-screen hero-gradient">
			{/* Background decorations */}
			<div className="fixed inset-0 overflow-hidden pointer-events-none">
				<div className="absolute top-20 left-10 w-72 h-72 bg-primary/5 rounded-full blur-3xl animate-float" />
				<div className="absolute bottom-20 right-10 w-96 h-96 bg-accent/5 rounded-full blur-3xl animate-float" style={{ animationDelay: "3s" }} />
			</div>

			<div className="relative z-10 container mx-auto px-4 py-8">
				{/* Header */}
				<header className="text-center mb-24 pt-8">
					<div className="flex items-center justify-center gap-3 mb-4 opacity-0 animate-fade-in">
						<div className="p-3 rounded-2xl bg-primary/10">
							<Leaf className="h-8 w-8 text-primary" />
						</div>
					</div>
					<h1 className="font-display text-5xl md:text-6xl font-bold mb-4 opacity-0 animate-fade-in" style={{ animationDelay: "0.1s" }}>
						<span className="gradient-text">AirWatch</span> Station
					</h1>
					<p className="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto opacity-0 animate-fade-in" style={{ animationDelay: "0.2s" }}>
						Real-time environmental monitoring with AI-powered health insights
					</p>
				</header>

				{/* Current Conditions */}
				<section className="mb-16 opacity-0 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
					<h2 className="font-display text-2xl font-semibold text-center mb-8">Current Conditions</h2>
					<div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
						{/* Temperature Card */}
						<div className="stat-card">
							<div className="flex items-center gap-3 mb-4">
								<div className="p-2 rounded-xl bg-primary/10">
									<Thermometer className="h-5 w-5 text-primary" />
								</div>
								<span className="text-muted-foreground font-medium">Temperature</span>
							</div>
							<p className="font-display text-4xl font-bold">
								{airData.temperature.toFixed(1)}
								<span className="text-2xl text-muted-foreground ml-1">°C</span>
							</p>
						</div>

						{/* Humidity Card */}
						<div className="stat-card">
							<div className="flex items-center gap-3 mb-4">
								<div className="p-2 rounded-xl bg-accent/10">
									<Droplets className="h-5 w-5 text-accent" />
								</div>
								<span className="text-muted-foreground font-medium">Humidity</span>
							</div>
							<p className="font-display text-4xl font-bold">
								{airData.humidity.toFixed(0)}
								<span className="text-2xl text-muted-foreground ml-1">%</span>
							</p>
						</div>

						{/* Air Quality Card */}
						<div className="stat-card">
							<div className="flex items-center gap-3 mb-4">
								<div className="p-2 rounded-xl bg-primary/10">
									<Wind className="h-5 w-5 text-primary" />
								</div>
								<span className="text-muted-foreground font-medium">Air Quality</span>
							</div>
							<p className={`font-display text-4xl font-bold ${getairQualityColor(airData.airQuality)}`}>
								{airData.status}
							</p>
							<p className="text-muted-foreground text-sm mt-1">
								{airData.airQuality.toFixed(0)} AQI
							</p>
						</div>
					</div>
				</section>

				{/* Action Buttons */}
				<section className="flex flex-col sm:flex-row gap-4 justify-center items-center opacity-0 animate-fade-in-up" style={{ animationDelay: "0.5s" }}>
					<Link to="/dashboard">
						<Button variant="default" size="lg" className="min-w-[200px] h-14 text-lg font-semibold gap-3 rounded-xl shadow-glow hover:shadow-elevated transition-all duration-300">
							<BarChart3 className="h-5 w-5" />
							View Dashboard
						</Button>
					</Link>
					<Link to="/assistant">
						<Button variant="outline" size="lg" className="min-w-[200px] h-14 text-lg font-semibold gap-3 rounded-xl border-2 hover:bg-secondary/50 transition-all duration-300">
							<Bot className="h-5 w-5" />
							Ask AI Assistant
						</Button>
					</Link>
				</section>

				{/* Footer */}
				<footer className="text-center mt-40 pb-8 text-muted-foreground text-sm opacity-0 animate-fade-in" style={{ animationDelay: "0.7s" }}>
					<p>Air Quality Monitoring Dashboard</p>
				</footer>
			</div>
		</div>
	);
};

export default Index;