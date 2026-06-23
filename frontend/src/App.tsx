import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AppLayout from './components/layout/AppLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import BatimentsList from './pages/patrimoine/BatimentsList';
import BatimentDetail from './pages/patrimoine/BatimentDetail';
import TravauxList from './pages/travaux/TravauxList';
import TravauxDetail from './pages/travaux/TravauxDetail';
import AgentsList from './pages/users/AgentsList';
import InvestissementsList from './pages/travaux/InvestissementsList';
import ContactsList from './pages/Contact';

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/travaux" element={<TravauxList />} />
          <Route path="/travaux/:id" element={<TravauxDetail />} />
          <Route path="/travaux/investissements" element={<InvestissementsList />} />
          <Route path="/patrimoine/batiments" element={<BatimentsList />} />
          <Route path="/patrimoine/batiments/:id" element={<BatimentDetail />} />
          <Route path="/contacts" element={<ContactsList />} />
          <Route path="/users/agents" element={<AgentsList />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}