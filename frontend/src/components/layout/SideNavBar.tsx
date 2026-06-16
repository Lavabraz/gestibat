import { NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const navItems = [
  { path: '/dashboard', label: 'Tableau de bord', icon: '📊' },
  { path: '/patrimoine/batiments', label: 'Patrimoine', icon: '🏢' },
  { path: '/agents', label: 'Agents', icon: '👥' },
  { path: '/travaux', label: 'Travaux', icon: '🔧' },
  { path: '/audit-logs', label: 'Audit', icon: '📜' },
];

export default function SideNavBar() {
  const { user } = useAuth();

  return (
    <aside className="w-64 bg-card-bg rounded-card p-4 shadow-sm h-screen sticky top-0">
      <div className="mb-8">
        <h2 className="text-xl font-bold text-primary">GestiBat</h2>
        <p className="text-sm text-slate-600 mt-1">Gestion du patrimoine</p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              'flex items-center gap-3 px-4 py-3 rounded-input transition-colors ' +
              (isActive
                ? 'bg-primary text-white font-medium'
                : 'text-slate-700 hover:bg-slate-200')
            }
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {user && (
        <div className="absolute bottom-4 left-4 right-4">
          <div className="flex items-center gap-3 p-3 bg-slate-100 rounded-input">
            <div className="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold">
              {user.firstName?.charAt(0) || user.username.charAt(0)}
            </div>
            <div>
              <p className="font-medium text-slate-800">{user.firstName || user.username}</p>
              <p className="text-xs text-slate-500 capitalize">{user.role}</p>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
