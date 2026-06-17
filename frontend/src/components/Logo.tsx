export default function Logo() {
  return (
    <div className="flex items-center justify-center space-x-4">
      <div className="w-20 h-20 relative">
        <svg viewBox="0 0 100 100" className="w-full h-full">
          <path d="M50 20 C30 20, 20 40, 20 60 C20 80, 40 90, 50 85 C60 90, 80 80, 80 60 C80 40, 70 20, 50 20 Z" fill="#00AEEF"/>
          <path d="M50 30 C40 30, 35 45, 35 55 C35 65, 45 75, 50 70 C55 75, 65 65, 65 55 C65 45, 60 30, 50 30 Z" fill="#00A859"/>
          <path d="M50 40 C45 40, 42 50, 42 58 C42 66, 50 70, 50 65 C50 60, 58 58, 58 50 C58 42, 55 40, 50 40 Z" fill="#FBBF24"/>
        </svg>
      </div>
      <div className="flex flex-col">
        <span className="text-2xl font-bold text-slate-800 tracking-wide">AMBERT</span>
        <span className="text-xl font-medium text-slate-700 tracking-wider">LIVRADOIS</span>
        <span className="text-xl font-medium text-slate-700 tracking-wider">FOREZ</span>
      </div>
    </div>
  );
}