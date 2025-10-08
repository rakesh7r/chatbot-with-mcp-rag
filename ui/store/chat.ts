import { create } from "zustand"
import { persist, createJSONStorage } from "zustand/middleware"

interface HistoryItem {
    role: string
    content: string
}

type ChatType = "chat" | "file"

interface ChatState {
    type: ChatType
    setType: (type: ChatType) => void
    isFile: boolean
    setIsFile: (isFile: boolean) => void
    fileName: string
    setFileName: (fileName: string) => void
    history: HistoryItem[]
    setHistory: (history: HistoryItem[]) => void
    addMessage: (role: string, content: string) => void
    clearHistory: () => void
    createNewChat: () => void
}

export const useChatStore = create<ChatState>()(
    persist<ChatState>(
        (set) => ({
            type: "chat",
            isFile: false,
            fileName: "",
            history: [],
            setType: (type) => set({ type }),
            setIsFile: (isFile) => set({ isFile }),
            setFileName: (fileName) => set({ fileName }),
            setHistory: (history) => set({ history }),
            addMessage: (role, content) =>
                set((state) => ({
                    history: [...state.history, { role, content }],
                })),
            clearHistory: () => set({ history: [] }),
            createNewChat: () => set({ type: "chat", isFile: false, fileName: "", history: [] }),
        }),
        {
            name: "chat-storage",
            storage: createJSONStorage(() => localStorage), // ✅ ensures proper storage interface
        }
    )
)
