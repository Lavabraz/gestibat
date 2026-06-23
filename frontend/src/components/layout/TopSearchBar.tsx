import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function TopSearchBar() {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate('/patrimoine/batiments?search=' + encodeURIComponent(searchQuery));
    }
  };

  return (
    <div className="flex items-center justify-between p-4 bg-[#1e1e1e] text-white rounded-card shadow-sm">
      <div className="flex-1 max-w-md">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Rechercher..."
            className="w-full px-4 py-2 border border-white/20 bg-white/10 rounded-input focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent text-white placeholder-white/50"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-white/70 hover:text-white"
          >
            🔍
          </button>
        </form>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-white font-medium">Dashboard</span>
        <button className="p-2 rounded-input hover:bg-white/10 transition-colors text-white/70 hover:text-white">
          🔔
        </button>
        <button className="p-2 rounded-input hover:bg-white/10 transition-colors text-white/70 hover:text-white">
          ⚙️
        </button>
      </div>
    </div>
  );
}