import axiosClient from "@/config/axiosConfig";
import { chatUrls, mcpUrls } from "@/constants/urls.const";

interface ChatPayload {
    prompt: string;
    history: { role: string; content: string }[];
    filename?: string;
}

export const sendChat = async (payload: ChatPayload) => {
    const response = await axiosClient.post(chatUrls.chat, payload);
    return response.data;
}


export const uploadPdf =async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axiosClient.post(chatUrls.uploadPdf, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
}

export const fileChat = async (payload: ChatPayload) => {
    const response = await axiosClient.post(chatUrls.fileChat, payload);
    return response.data;
}

