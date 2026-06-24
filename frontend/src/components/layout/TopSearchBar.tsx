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
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '1rem',
      backgroundColor: '#1e1e1e',
      color: 'white',
      borderRadius: '15px',
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
    }}>
      <div style={{ flex: 1, maxWidth: '42rem' }}>
        <form onSubmit={handleSearch} style={{ position: 'relative' }}>
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Rechercher un batiment, un contact..."
            style={{
              width: '100%',
              padding: '0.5rem 1rem',
              backgroundColor: 'rgba(255,255,255,0.1)',
              border: '1px solid rgba(255,255,255,0.2)',
              borderRadius: '15px',
              color: 'white',
              fontSize: '1rem',
              outline: 'none',
            }}
          />
          <button
            type="submit"
            style={{
              position: 'absolute',
              right: '0.75rem',
              top: '50%',
              transform: 'translateY(-50%)',
              color: 'rgba(255,255,255,0.7)',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '1.25rem',
            }}
          >
            🔍
          </button>
        </form>
      </div>
      <div style={{ marginLeft: '1.5rem', fontWeight: '500', color: 'white' }}>
        Dashboard
      </div>
    </div>
  );
}