"use client";
import { MessageCirclePlus } from "lucide-react";
import { ThemeToggle } from "../themeToggle";
import { Button } from "./button";
import { useChatStore } from "@/store/chat";

export default function AppHeader() {
  const { createNewChat, isStockChat, setStockChat } = useChatStore();
  const onSwitchToStock = () => {
    setStockChat(!isStockChat);
  }
  return (
    <header className="p-4 border-b border-b-[#5a5a5a] flex justify-end sticky top-0 backdrop-blur-sm z-10 ">
      <div className="flex-1 text-lg font-medium gap-2">MCP Rag Excercise</div>
      <div className="flex items-center gap-2">
        <Button className="" size={'sm'} onClick={onSwitchToStock}>
          {isStockChat ? "Switch to Chat" : "Switch to Stock Insights"}
        </Button>
        <Button
          size={"icon"}
          className="bg-transparent text-white hover:text-black"
          onClick={createNewChat}
        >
          <MessageCirclePlus />
        </Button>
        <ThemeToggle />
      </div>
    </header>
  );
}
