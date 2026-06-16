interface SkeletonLoaderProps {
  type?: 'card' | 'text' | 'circle' | 'list';
  count?: number;
  className?: string;
}

export default function SkeletonLoader({
  type = 'card',
  count = 1,
  className = '',
}: SkeletonLoaderProps) {
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return (
          <div className="bg-card-bg rounded-card p-6 shadow-sm animate-pulse">
            <div className="h-4 bg-slate-300 rounded w-3/4 mb-2"></div>
            <div className="h-8 bg-slate-200 rounded w-1/2"></div>
          </div>
        );
      case 'text':
        return (
          <div className="space-y-2 animate-pulse">
            <div className="h-4 bg-slate-300 rounded w-full"></div>
            <div className="h-4 bg-slate-200 rounded w-3/4"></div>
          </div>
        );
      case 'circle':
        return <div className="w-12 h-12 bg-slate-300 rounded-full animate-pulse"></div>;
      case 'list':
        return (
          <div className="space-y-3 animate-pulse">
            {Array.from({ length: count }).map((_, i) => (
              <div key={i} className="h-12 bg-slate-200 rounded-input"></div>
            ))}
          </div>
        );
      default:
        return <div className="h-20 bg-slate-200 rounded animate-pulse"></div>;
    }
  };

  return (
    <div className={className}>
      {Array.from({ length: count }).map((_, i) => (
        <div key={i}>{renderSkeleton()}</div>
      ))}
    </div>
  );
}
