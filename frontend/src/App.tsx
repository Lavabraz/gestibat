import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import BatimentsList from './pages/patrimoine/BatimentsList';
import BatimentDetail from './pages/patrimoine/BatimentDetail';

function Layout() {
  return (
    <div className="min-h-screen bg-bg-global">
      <header className="bg-card-bg shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary">GestiBat</h1>
            </div>
            <nav className="flex items-center space-x-6">
              <a href="/dashboard" className="text-slate-700 hover:text-primary transition-colors">
                Tableau de bord
              </a>
              <a href="/patrimoine/batiments" className="text-slate-700 hover:text-primary transition-colors">
                Patrimoine
              </a>
            </nav>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/patrimoine/batiments" element={<ProtectedRoute><BatimentsList /></ProtectedRoute>} />
          <Route path="/patrimoine/batiments/:id" element={<ProtectedRoute><BatimentDetail /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Layout />
    </AuthProvider>
  );
}
