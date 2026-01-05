import React from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export default function MarkdownPreview({ content }: { content: string }) {
    return (
        <div className="markdown-body break-words prose max-w-full">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </div>
    )
}
