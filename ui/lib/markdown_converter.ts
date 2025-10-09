export function jsonToMarkdown(obj: any, indent = 1): string {
    const spaces = "  ".repeat(indent)

    if (Array.isArray(obj)) {
        return obj.map((item) => `${spaces}- ${jsonToMarkdown(item, indent + 1).trimStart()}`).join("\n")
    }

    if (typeof obj === "object" && obj !== null) {
        return Object.entries(obj)
            .map(([key, value]) => {
                if (typeof value === "object") {
                    return `${spaces}**${key}:**\n${jsonToMarkdown(value, indent + 1)}`
                }
                return `${spaces}**${key}:** ${value}`
            })
            .join("\n")
    }

    return `${obj}`
}
