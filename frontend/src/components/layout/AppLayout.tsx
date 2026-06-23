import { Outlet } from 'react-router-dom';
import SideNavBar from './SideNavBar';
import TopSearchBar from './TopSearchBar';

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-[#e0e0e0]">
      <div className="flex">
        <SideNavBar />
        <main className="flex-1 p-6">
          <TopSearchBar />
          <div className="mt-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}