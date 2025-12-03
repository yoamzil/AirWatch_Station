import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { ArrowLeft, ExternalLink, Leaf } from "lucide-react";

// Read dashboard URL from Vite env. If not set, fall back to a placeholder string.
const PUBLIC_DASHBOARD_URL: string = (import.meta.env.VITE_DASHBOARD_URL as string) || "PUBLIC_DASHBOARD_URL";

const Dashboard = () => {
	const isPlaceholder =
		!PUBLIC_DASHBOARD_URL ||
		PUBLIC_DASHBOARD_URL === "PUBLIC_DASHBOARD_URL" ||
		PUBLIC_DASHBOARD_URL.includes("your_public_dashboard_url") ||
		PUBLIC_DASHBOARD_URL.trim() === "";

	return (
		<div className="min-h-screen bg-background flex flex-col">
			{/* Header */}
			<header className="flex items-center justify-between px-4 py-3 border-b border-border bg-card/50 backdrop-blur-sm">
				<div className="flex items-center gap-4">
					<Link to="/">
						<Button variant="ghost" size="sm" className="gap-2">
							<ArrowLeft className="h-4 w-4" />
							Back
						</Button>
					</Link>
					<div className="p-1.5 rounded-lg bg-primary/10">
						<Leaf className="h-4 w-4 text-primary" />
					</div>
					<h1 className="font-display text-lg font-semibold">Dashboard</h1>
				</div>
			</header>

			{/* Dashboard iframe or placeholder */}
			{isPlaceholder ? (
				<div className="flex-1 flex items-center justify-center p-8">
					<div className="glass-card p-8 max-w-lg text-center">
						<div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
							<ExternalLink className="h-8 w-8 text-primary" />
						</div>
						<h2 className="font-display text-2xl font-bold mb-4">Dashboard Not Configured</h2>
						<p className="text-muted-foreground mb-6">
							To display your dashboard, replace <code className="px-2 py-1 bg-muted rounded text-sm font-mono">PUBLIC_DASHBOARD_URL</code> in <code className="px-2 py-1 bg-muted rounded text-sm font-mono">src/pages/Dashboard.tsx</code> with your actual dashboard URL.
						</p>
					</div>
				</div>
			) : (
				<iframe
					src={PUBLIC_DASHBOARD_URL}
					className="flex-1 w-full border-0"
					title="Dashboard"
					allow="fullscreen"
				/>
			)}
		</div>
	);
};

export default Dashboard;