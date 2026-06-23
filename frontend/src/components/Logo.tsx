export default function Logo({ className = "" }: { className?: string }) {
  return (
    <div className={"flex items-center gap-2 text-white " + className}>
      <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center text-primary font-bold text-xl">
        ALF
      </div>
    </div>
  );
}