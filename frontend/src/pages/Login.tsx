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
    <div className="min-h-screen bg-[#00707a] flex p-[22px] md:p-[14px] sm:p-[8px]">
      <div className="flex-1 bg-[#d9d9d9] flex items-center justify-center p-[48px_24px] md:p-[36px_20px] sm:p-[28px_16px]">
        <div className="w-full max-w-[360px] flex flex-col items-center text-center">
          <Logo className="w-full max-w-[320px] h-auto mb-9 md:max-w-[260px] md:mb-7 sm:max-w-[200px] sm:mb-6" />
          <h1 className="m-0 mb-7 text-[1.7rem] font-bold text-[#00707a] tracking-[0.01em] md:text-[1.45rem] md:mb-[22px] sm:text-[1.25rem] sm:mb-5">
            Authentification
          </h1>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded mb-6 text-sm text-center">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="w-full flex flex-col gap-5 sm:gap-4">
            <div className="w-full text-left flex flex-col gap-2">
              <label className="text-[0.95rem] font-bold text-[#00707a]">
                Identifiant
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full py-[11px] px-[14px] border-[1.5px] border-[#00707a] rounded-[8px] bg-[#d9d9d9] text-[#1a1a1a] placeholder:text-[#6b6b6b] focus:outline-none focus:shadow-[0_0_0_3px_rgba(0,112,122,0.25)] focus:bg-white"
                placeholder="Entrez votre identifiant"
                required
              />
            </div>

            <div className="w-full text-left flex flex-col gap-2">
              <label className="text-[0.95rem] font-bold text-[#00707a]">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full py-[11px] px-[14px] border-[1.5px] border-[#00707a] rounded-[8px] bg-[#d9d9d9] text-[#1a1a1a] placeholder:text-[#6b6b6b] focus:outline-none focus:shadow-[0_0_0_3px_rgba(0,112,122,0.25)] focus:bg-white"
                placeholder="Entrez votre mot de passe"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="mt-2 self-center px-[40px] py-[13px] border-none rounded-[999px] bg-[#00707a] text-white text-[1rem] font-bold transition-colors hover:bg-[#00565d] active:translate-y-[1px] sm:w-full sm:px-0"
            >
              {isLoading ? 'Connexion en cours...' : 'Entrer →'}
            </button>
          </form>

          <Link
            to="/forgot-password"
            className="inline-block mt-[22px] text-[#00707a] font-bold text-[0.92rem] no-underline hover:underline"
          >
            Mot de passe oublié ?
          </Link>
        </div>
      </div>
    </div>
  );
}