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
    <div className="flex items-center justify-between p-4 bg-card-bg rounded-card shadow-sm">
      <div className="flex-1 max-w-md">
        <form onSubmit={handleSearch} className="relative">
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Rechercher un bâtiment, un agent..."
            className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-slate-500 hover:text-primary"
          >
            🔍
          </button>
        </form>
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 rounded-input hover:bg-slate-200 transition-colors">
          🔔
        </button>
        <button className="p-2 rounded-input hover:bg-slate-200 transition-colors">
          ⚙️
        </button>
      </div>
    </div>
  );
}
