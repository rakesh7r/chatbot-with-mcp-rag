"use client";
import ChatContainer from "@/components/chatContainer";
import { useChatStore } from "@/store/chat";

export default function Home() {
  return (
    <main className="flex flex-row justify-center items-center">
      <ChatContainer />
    </main>
  );
}
