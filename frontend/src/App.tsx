import { Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "./layouts/AppLayout";
import { DashboardPage } from "./pages/DashboardPage";
import { DevicesPage } from "./pages/DevicesPage";
import { EventsPage } from "./pages/EventsPage";
import { RulesPage } from "./pages/RulesPage";
import { BeaconPage } from "./pages/BeaconPage";
import { RuleTriggersPage } from "./pages/RuleTriggersPage";

export default function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/devices" element={<DevicesPage />} />
        <Route path="/events" element={<EventsPage />} />
        <Route path="/rules" element={<RulesPage />} />
        <Route path="/beacon" element={<BeaconPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
        <Route path="/triggers" element={<RuleTriggersPage />} />
      </Routes>
    </AppLayout>
  );
}
