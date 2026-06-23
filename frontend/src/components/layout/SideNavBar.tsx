import { NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import Logo from '../Logo';

const navItems = [
  { path: '/dashboard', label: 'Tableau de bord', icon: '📊' },
  { path: '/patrimoine/batiments', label: 'Patrimoine', icon: '🏢' },
  { path: '/contacts', label: 'Contacts', icon: '👥' },
  { path: '/travaux', label: 'Travaux', icon: '🔧' },
  { path: '/audit-logs', label: 'Audit', icon: '📜' },
];

export default function SideNavBar() {
  const { user, logout } = useAuth();

  return (
    <aside className="w-64 bg-[#00717a] text-white rounded-card p-4 shadow-sm h-screen sticky top-0">
      <div className="mb-8">
        <Logo className="h-10 w-auto invert brightness-0" />
        <p className="text-sm text-white/80 mt-1">Gestion du patrimoine</p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              'flex items-center gap-3 px-4 py-3 rounded-input transition-colors ' +
              (isActive
                ? 'bg-[#005a60] text-white font-medium'
                : 'text-white/90 hover:bg-[#00858f]')
            }
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {user && (
        <div className="absolute bottom-4 left-4 right-4">
          <div className="flex items-center gap-3 p-3 bg-white/10 rounded-input">
            <div className="w-10 h-10 rounded-full bg-white/20 text-white flex items-center justify-center font-bold">
              {user ? (user.firstName?.charAt(0) || user.username?.charAt(0) || '?') : '?'}
            </div>
            <div>
              <p className="font-medium text-white">{user ? (user.firstName || user.username || 'Utilisateur') : 'Utilisateur'}</p>
              <p className="text-xs text-white/70 capitalize">{user?.role || 'Invite'}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="w-full mt-3 bg-transparent border border-white/30 text-white/90 py-2 rounded-input hover:bg-white/10 transition-colors"
          >
            Deconnexion
          </button>
        </div>
      )}
    </aside>
  );
}