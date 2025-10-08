import { useEffect, useRef, useState } from "react"
import { Input } from "./ui/input"
import Bubble from "./bubble"
import { Button } from "./ui/button"
import { ArrowUp } from "lucide-react"
import { send } from "process"
import { sendChat } from "@/services/api.service"
import { useChatStore } from "@/store/chat"

export default function ChatContainer() {
    const promptRef = useRef<HTMLInputElement>(null)
    const [prompt, setPrompt] = useState<string>("")
    const { addMessage } = useChatStore()

    useEffect(() => {
        promptRef.current?.focus()
    }, [])

    const onPromptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPrompt(e.target.value)
    }

    const onPromptKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            addMessage("user", prompt)
            sendMessageHandler()
            return
        }
        return
    }

    const sendMessageHandler = async () => {
        try {
            const resposne = await sendChat({
                prompt,
                history: [],
            })
            addMessage("assistant", resposne.answer)

            setPrompt("")
        } catch (error) {
            console.error("Error sending message:", error)
        }
    }

    return (
        <div className="flex flex-col overflow-y-auto p-4 w-[60vw] ">
            <div className="h-[85vh]">
                <Bubble message="hello" />
            </div>
            <div className="fixed bottom-5 w-[60vw] flex justify-start items-center gap-2 bg-background p-2 rounded-xl shadow-md">
                <Input placeholder="enter your message here" ref={promptRef} className="w-full" value={prompt} onChange={onPromptChange} onKeyDown={onPromptKeyDown} />
                <Button size={"icon"} className="float-right" onClick={sendMessageHandler}>
                    <ArrowUp />
                </Button>
            </div>
        </div>
    )
}
