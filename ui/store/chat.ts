import { create } from "zustand";
import { persist, devtools, createJSONStorage } from "zustand/middleware";
import { immer } from "zustand/middleware/immer";

interface HistoryItem {
  role: string;
  content: string;
}

type ChatType = "chat" | "file";

interface ChatState {
  type: ChatType;
  setType: (type: ChatType) => void;
  isFile: boolean;
  setIsFile: (isFile: boolean) => void;
  fileName: string;
  setFileName: (fileName: string) => void;
  history: HistoryItem[];
  setHistory: (history: HistoryItem[]) => void;
  addMessage: (role: string, content: string) => void;
  clearHistory: () => void;
  createNewChat: () => void;
}

const defaultChatHistory: HistoryItem[] = [
  {
    role: "assistant",
    content: "Hello! How can I help you today?",
  },
];

export const useChatStore = create<ChatState>()(
  devtools(
    persist(
      immer((set) => ({
        type: "chat",
        isFile: false,
        fileName: "",
        history: defaultChatHistory,
        setType: (type) => set({ type }),
        setIsFile: (isFile) => set({ isFile }),
        setFileName: (fileName) => set({ fileName }),
        setHistory: (history) => set({ history }),

        addMessage: (role, content) =>
          set((state) => {
            state.history.push({ role, content }); // Immer allows mutation syntax
          }),

        clearHistory: () => set({ history: [] }),

        createNewChat: () =>
          set({
            type: "chat",
            isFile: false,
            fileName: "",
            history: defaultChatHistory,
          }),
      })),
      {
        name: "chat-storage",
        storage: createJSONStorage(() => localStorage),
      },
    ),
  ),
);
