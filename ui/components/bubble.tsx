interface BubbleProps {
  message: string;
}
export default function Bubble({ message }: BubbleProps) {
  return (
    <div className="border-2 max-w-[80%] px-3 py-2 m-2 rounded-xl drop-shadow-2xl drop-shadow-slate-700">
      {message}
    </div>
  );
}
