import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import Assistant from "./pages/Assistant";
import NotFound from "./pages/NotFound";

const App = () => (
	<TooltipProvider>
		<Toaster />
		<Sonner />
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Index />} />
				<Route path="/dashboard" element={<Dashboard />} />
				<Route path="/assistant" element={<Assistant />} />
				<Route path="*" element={<NotFound />} />
			</Routes>
		</BrowserRouter>
	</TooltipProvider>
);

export default App;
