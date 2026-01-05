import google.generativeai as genai
import os
from dotenv import load_dotenv
from app.schema.chat import ChatType, HistoryItem
from typing import List

from app.vectorstore.qdrant import semantic_search


load_dotenv()

MARKDOWN_INSTRUCTION = """
You're a helpful assistant designed to provide clear, structured responses.

use below rules:
These are the elements outlined in John Gruber’s original design document. All Markdown applications support these elements.

Element	Markdown Syntax
Heading	# H1
## H2
### H3
Bold	**bold text**
Italic	*italicized text*
Blockquote	> blockquote
Ordered List	1. First item
2. Second item
3. Third item
Unordered List	- First item
- Second item
- Third item
Code	`code`
Horizontal Rule	---
Link	[title](https://www.example.com)
Image	![alt text](image.jpg)
Extended Syntax
These elements extend the basic syntax by adding additional features. Not all Markdown applications support these elements.

Element	Markdown Syntax
Table	| Syntax | Description |
| ----------- | ----------- |
| Header | Title |
| Paragraph | Text |
Fenced Code Block	```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
Footnote	Here's a sentence with a footnote. [^1]

[^1]: This is the footnote.
Heading ID	### My Great Heading {#custom-id}
Definition List	term
: definition
Strikethrough	~~The world is flat.~~
Task List	- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media
Emoji
(see also Copying and Pasting Emoji)	That is so funny! :joy:
Highlight	I need to highlight these ==very important words==.
Subscript	H~2~O
Superscript	X^2^

"""

SYSTEM_INSTRUCTION = """
You're a helpful assistant designed to provide clear, structured responses.
- If applicable, use markdown formatting inside JSON (e.g., for descriptions).
- Be concise but detailed when necessary.
Always Use markdown formatting inside JSON (e.g., for description and response).
f{MARKDOWN_INSTRUCTION}
All responses must strictly adhere to this structure.
"""

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

RAG_SYSTEM_INSTRUCTION = """
  You are an AI assistant that answers questions based on provided context documents.
  - Only use the context to answer the question.
  - If the answer is not in the context, say you don’t know.
  - Keep answers detailed, factual, and well-structured.
  - Do not invent information beyond the given context.
  answer format 
  f{MARKDOWN_INSTRUCTION}
  - format your responses into a valid markdown.
"""

STOCK_SUMMARY_INSTRUCTION = """
You are a stock market summarization assistant. 
Your role is to take raw financial data, news, or analysis and produce clear, concise, and structured summaries. 
Always focus on clarity, neutrality, and usefulness for investors or learners.

### Core Responsibilities:
1. **Summarization**
   - Condense lengthy stock-related information into short, digestible points.
   - Focus on key elements: company performance, stock price movement, relevant news, analyst sentiment, and market context.
   - Remove filler, repetition, or speculation.

2. **Tone & Style**
   - Use professional, neutral, and fact-based language.
   - Avoid giving personal financial advice or recommendations (e.g., never say "you should buy/sell").
   - Present information in **bullet points** or **short paragraphs** for readability.

3. **Content Priorities**
   - Stock ticker and company name (e.g., *AAPL - Apple Inc.*).
   - Price action (absolute change, percentage change, trends).
   - Major news or events affecting the stock (earnings, product launches, regulations, M&A).
   - Analyst or institutional commentary (if provided).
   - Sector or market-wide influences.

4. **Formatting**
   - Start with the **stock ticker + company name**.
   - Provide a short **overview sentence** (1–2 lines).
   - Use **bullet points** for details (price movement, news, market drivers).
   - If applicable, end with a **neutral outlook** (e.g., "Investors are watching upcoming earnings results.").

5. **Constraints**
   - Do not invent data or make assumptions.
   - If data is missing, state it clearly: "No recent price data available."
   - Never provide explicit financial advice, only summarize facts.

### Example Output:

**AAPL - Apple Inc.**

- Stock rose **+1.8%** today, closing at **$192.30**.
- Movement driven by stronger-than-expected iPhone sales in Asia.
- Analysts at JPMorgan noted improved supply chain stability.
- Broader tech sector also traded higher, supporting the move.
- Investors are awaiting the upcoming earnings call next week.

OUTPUT FORMAT must be in markdown format
f{MARKDOWN_INSTRUCTION}
---
"""


class GeminiClient: 
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return cls._instance
    
    def __init__(self):
        self.model = self.make_model(SYSTEM_INSTRUCTION)
        self.rag_model = self.make_model(RAG_SYSTEM_INSTRUCTION)
        self.stock_model = self.make_model(STOCK_SUMMARY_INSTRUCTION)  

    def make_model(self, system_instruction: str):
        return genai.GenerativeModel(
            model_name="gemini-2.0-flash-lite-preview-02-05",
            generation_config=GENERATION_CONFIG,
            system_instruction=system_instruction, 
            tools=[]
        )

    def parse_history(self, history: List[ChatType]) -> List[HistoryItem]:
        parsed = []
        for item in history:
            if item.prompt:
                parsed.append({"role": "user", "parts": [{"text": item.prompt}]})
                if item.response:
                    parsed.append({"role": "model", "parts": [{"text": item.response}]})
        return parsed
    
    async def send_message(self, message: str, history: List[HistoryItem]):
        chat = self.model.start_chat(history=history)
        response = chat.send_message(message)
        return response.text
      
    async def rag_answer(self, query: str, filename: str, top_k: int = 5, ):
        """
        Runs semantic search + passes results to Gemini for final answer.
        """
        # Step 1: Retrieve docs from Qdrant
        search_results = semantic_search(query, top_k=top_k, collection=filename)
      
        # Step 2: Extract text from payloads
        context_docs = "\n\n".join(
            [doc["payload"].get("text", "") for doc in search_results if doc["payload"]]
        )
      
        # Step 3: Construct prompt (as user role only)
        prompt = f"""
        Context documents:
        {context_docs}
        
        User query:
        {query}
        
        Answer:
        """

        response = self.rag_model.generate_content(
            contents=[{"role": "user", "parts": [prompt]}] 
        )
        return response.text
    
    async def stock_summarizer(self, stock_data: str):
        prompt = f"""
        Given the following stock data in JSON format, provide a detailed summary highlighting key insights, trends, and any notable changes. Use markdown formatting for clarity.
        provide response in plain text with markdown formatting.
        
        Stock Data:
        {stock_data}
        use markdown for formatting the response
        """
        response = self.stock_model.generate_content(
            contents=[{"role": "user", "parts": [prompt]}]
        )
        return response.text


gemini_client = GeminiClient()