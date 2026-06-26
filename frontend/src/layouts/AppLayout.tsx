import { NavLink } from "react-router-dom";
import { Activity, Bluetooth, Database, Radio, Settings } from "lucide-react";

type AppLayoutProps = {
  children: React.ReactNode;
};

const links = [
  { to: "/", label: "Dashboard", icon: Activity },
  { to: "/devices", label: "Dispositivos", icon: Bluetooth },
  { to: "/events", label: "Eventos", icon: Database },
  { to: "/rules", label: "Reglas", icon: Settings },
  { to: "/beacon", label: "Baliza", icon: Radio },
  { to: "/triggers", label: "Actividad", icon: Activity }
];

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">BLE</div>
          <div>
            <h1>BLE Hub</h1>
            <p>Wearable event gateway</p>
          </div>
        </div>

        <nav>
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
              >
                <Icon size={18} />
                <span>{link.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <main className="main-content">{children}</main>
    </div>
  );
}
