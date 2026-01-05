import qs from "qs";

export const chatUrls = {
  chat: "/api/chat",
  uploadPdf: "/api/upload-pdf",
  fileChat: "/api/file-chat",
};

export const mcpUrls = {
  planner: (req: string) => `/api/mcp/planner?${qs.stringify({ req })}`,
};
