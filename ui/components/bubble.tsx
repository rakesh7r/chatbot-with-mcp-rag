import { jsonToMarkdown } from "@/lib/markdown_converter";
import MarkdownPreview from "./markdownPreview";

interface BubbleProps {
  message: any;
}
export default function Bubble({ message }: BubbleProps) {
  console.log("message in bubble:", message);
  return (
    <div className="border-2 max-w-[80%] px-3 py-2 m-2 rounded-xl drop-shadow-2xl drop-shadow-slate-700">
      <MarkdownPreview content={message} />
    </div>
  );
}
