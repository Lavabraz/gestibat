import { Link, Route, Routes } from "react-router-dom";

function Dashboard() {
  return (
    <section className="rounded-card bg-card-bg p-6 shadow-sm">
      <h2 className="text-2xl font-semibold text-primary">Tableau de bord</h2>
      <p className="mt-2 text-slate-700">
        GestiBat est initialise avec Django + React + Tailwind.
      </p>
    </section>
  );
}

export default function App() {
  return (
    <main className="min-h-screen bg-bg-global p-8 text-slate-900">
      <header className="mb-6 rounded-card bg-card-bg p-6">
        <h1 className="text-4xl font-bold text-primary">GestiBat</h1>
        <nav className="mt-4 flex gap-4">
          <Link className="text-primary hover:text-primary-dark" to="/">
            Accueil
          </Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </main>
  );
}
