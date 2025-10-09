import { useEffect, useRef, useState } from "react"
import { Input } from "./ui/input"
import Bubble from "./bubble"
import { Button } from "./ui/button"
import { ArrowUp, Paperclip } from "lucide-react"
import { fileChat, getStorkInsights, sendChat, uploadFile } from "@/services/api.service"
import { useChatStore } from "@/store/chat"

export default function ChatContainer() {
    const promptRef = useRef<HTMLInputElement>(null)
    const [prompt, setPrompt] = useState<string>("")
    const { addMessage, history, setIsFile, isFile, isStockChat } = useChatStore()
    const inputRef = useRef<HTMLInputElement>(null)
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState<boolean>(false)

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
        } else {
            promptRef.current?.focus()
        }
        return
    }

    const sendMessageHandler = async () => {
        try {
            setLoading(true)
            if (isStockChat) {
                const resposne = await getStorkInsights(prompt)
                addMessage("assistant", resposne)
            } else if (isFile) {
                const response = await fileChat({
                    prompt,
                    history: [],
                    filename: file?.name,
                })
                addMessage("assistant", response)
            } else {
                const resposne = await sendChat({
                    prompt,
                    history: [],
                })
                addMessage("assistant", resposne)
            }
            setPrompt("")
            setTimeout(() => {
                const chatContainer = document.querySelector(".chat-container") as HTMLDivElement
                chatContainer.scrollTop = chatContainer.scrollHeight
            }, 100)
            setLoading(false)
        } catch (error) {
            setLoading(false)
            console.error("Error sending message:", error)
        }
    }

    const handleClick = () => {
        inputRef.current?.click()
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (file) {
            setLoading(true)
            uploadFile(file)
                .then((response) => {
                    console.log("File uploaded successfully:", response)
                    setLoading(false)
                })
                .catch((error) => {
                    console.error("Error uploading file:", error)
                    setLoading(false)
                })
            setFile(file)
            setIsFile(true)
        }
    }

    return (
        <div className="flex flex-col overflow-y-auto p-4 w-[60vw]">
            <div className="h-[85vh] mb-24 chat-container overflow-y-auto">
                {history.map((msg, index) => (
                    <div key={index} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                        <Bubble message={typeof msg.content === "string" ? msg.content : JSON.stringify(msg.content)} />
                    </div>
                ))}
            </div>
            <div className="fixed bottom-5 w-[60vw] flex justify-start items-center gap-2 bg-background p-2 rounded-xl shadow-md">
                <>
                    <input disabled={isFile} ref={inputRef} type="file" className="hidden" onChange={handleChange} />
                    <Button disabled={loading || isFile} size="icon" type="button" onClick={handleClick}>
                        <Paperclip className="h-4 w-4" />
                    </Button>
                </>
                <Input
                    disabled={loading}
                    placeholder="enter your message here"
                    ref={promptRef}
                    className="w-full"
                    value={prompt}
                    onChange={onPromptChange}
                    onKeyDown={onPromptKeyDown}
                />
                <Button disabled={loading} size={"icon"} className="float-right" onClick={sendMessageHandler}>
                    <ArrowUp />
                </Button>
            </div>
        </div>
    )
}
