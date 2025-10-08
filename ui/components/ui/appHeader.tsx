import { ThemeToggle } from "../themeToggle"

export default function AppHeader() {
    return (
        <header className="p-4 border-b border-b-[#5a5a5a] flex justify-end sticky top-0 backdrop-blur-sm z-10 ">
            <div className="flex-1 text-lg font-medium">MCP Rag Excercise</div>
            <ThemeToggle />
        </header>
    )
}
