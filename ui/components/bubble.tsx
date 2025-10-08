interface BubbleProps {
    message: string
}
export default function Bubble({ message }: BubbleProps) {
    return <div className="border-2 w-min px-3 py-2 m-2 rounded-xl drop-shadow-2xl drop-shadow-amber-200">{message}</div>
}
