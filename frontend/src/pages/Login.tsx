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
      setError('Identifiants invalides. Veuillez réessayer.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="bg-white rounded-lg shadow-lg p-8 border-4 border-[#005F5F]">
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-[#005F5F] mb-6">Authentification</h1>
            <div className="flex justify-center">
              <Logo />
            </div>
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded mb-6 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-6">
            <div>
              <label className="block text-sm font-medium text-[#005F5F] mb-2">
                Identifiant
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 border-2 border-[#005F5F] rounded-md focus:outline-none focus:ring-2 focus:ring-[#00AEEF] focus:border-transparent bg-white"
                placeholder="Entrez votre identifiant"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[#005F5F] mb-2">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border-2 border-[#005F5F] rounded-md focus:outline-none focus:ring-2 focus:ring-[#00AEEF] focus:border-transparent bg-white"
                placeholder="Entrez votre mot de passe"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-[#005F5F] hover:bg-[#004B4B] text-white font-medium py-3 px-4 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              <span>{isLoading ? 'Connexion en cours...' : 'Entrer'}</span>
              {!isLoading && (
                <span className="text-xl">→</span>
              )}
            </button>
          </form>

          <div className="text-center mt-6">
            <Link to="/forgot-password" className="text-[#005F5F] hover:text-[#004B4B] text-sm">
              Mot de passe oublié ?
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}