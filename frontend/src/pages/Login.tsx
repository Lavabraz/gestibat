import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

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
    <div className="min-h-screen bg-bg-global flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-card-bg rounded-card p-8 shadow-lg">
          <div className="text-center mb-8">
            <div className="h-16 bg-primary rounded-input flex items-center justify-center mb-4">
              <span className="text-white text-2xl font-bold">GestiBat</span>
            </div>
            <h1 className="text-2xl font-bold text-primary">GestiBat</h1>
            <p className="text-slate-600 mt-2">
              Connectez-vous pour gerer le patrimoine
            </p>
          </div>

          {error && (
            <div className="bg-alert-red/10 text-alert-red p-3 rounded-input mb-4 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-slate-700 mb-1"
              >
                Identifiant
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="Entrez votre identifiant"
                required
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-slate-700 mb-1"
              >
                Mot de passe
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-input focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="Entrez votre mot de passe"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded-input transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Connexion en cours...' : 'Se connecter'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            &copy; 2026 - Ambert Livradois Forez
          </p>
        </div>
      </div>
    </div>
  );
}
