import { Outlet } from 'react-router-dom';
import SideNavBar from './SideNavBar';
import TopSearchBar from './TopSearchBar';

export default function AppLayout() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#d9d9d9' }}>
      <div style={{ display: 'flex' }}>
        <SideNavBar />
        <main style={{ flex: 1, padding: '1.5rem' }}>
          <TopSearchBar />
          <div style={{ marginTop: '1.5rem' }}>
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}