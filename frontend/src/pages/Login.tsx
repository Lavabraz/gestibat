import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Logo from '../components/Logo';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      await login(username, password);
    } catch (err) {
      setError('Identifiants invalides. Veuillez reessayer.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-slate-800 mb-6">Authentification</h1>
            <Logo />
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded mb-6 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Identifiant
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Entrez votre identifiant"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Entrez votre mot de passe"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-slate-800 hover:bg-slate-900 text-white font-medium py-3 px-4 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              <span>{isLoading ? 'Connexion en cours...' : 'Entrer'}</span>
              {!isLoading && (
                <span className="text-xl">→</span>
              )}
            </button>
          </form>

          <div className="text-center mt-6">
            <Link to="/forgot-password" className="text-blue-600 hover:text-blue-800 text-sm">
              Mot de passe oublié ?
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}