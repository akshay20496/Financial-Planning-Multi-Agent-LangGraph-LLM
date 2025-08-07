
# 🧠 Financial-Planning-Multi-Agent-LangGraph-LLM

AI-powered financial planning assistant that uses **LangGraph**, **LLMs**, and a **multi-agent architecture** to deliver personalized investment advice tailored to Indian users.

## 🚀 What It Does

Given a simple text input (like "I want to save for my child's education"), this app:

- Parses and understands the financial goal using an LLM (Gemini)
- Analyzes the user's profile (age, income, location, goal, reason, etc.)
- Determines risk appetite
- Allocates assets based on profile and goal
- Suggests Indian ETFs across asset classes
- Fetches live ETF prices using `yfinance`
- Returns a detailed investment strategy & summary

Supports Indian financial goals like:

✅ Real estate  
✅ Gold investing  
✅ Retirement planning  
✅ Marriage  
✅ Child education  
✅ Emergency fund  
✅ Tax saving  
✅ Vacation planning  
...and more!

---

## 🧠 Tech Stack

| Layer        | Tools Used                                 |
|--------------|---------------------------------------------|
| LLM          | Gemini 2.5 Flash (via LangChain wrapper)    |
| Graph Engine | LangGraph (`StateGraph`)                    |
| Agents       | Modular Multi-Agent architecture            |
| UI           | Streamlit                                   |
| Market Data  | `yfinance`                                  |
| Embedding    | N/A (no vector store used in this version)  |

---

## 📸 UI Demo

<img width="1816" height="922" alt="Screenshot (352)" src="https://github.com/user-attachments/assets/a1b1a045-84b8-42c8-8688-6535565d57b6" />

---

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/Financial-Planning-Multi-Agent-LangGraph-LLM.git
   cd Financial-Planning-Multi-Agent-LangGraph-LLM
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key**
   - Create a `.env` file:
     ```
     gemini_key=your_google_generative_ai_key_here
     ```

4. **Run the Streamlit app**
   ```bash
   python -m streamlit run app.py
   ```

---

## ✨ Example Prompt

```text
I am a 29-year-old with an annual income of ₹60 lakhs.
I live in Pune, India.
My financial goal is to invest in real estate in Purandar, Pune. 
Because a new airport is being planned there.
I have an investment horizon of 20 years.
Can you help me plan my investments accordingly in the Indian market?
```
---

## 📂 Project Structure

```
├── app.py               # Streamlit frontend
├── graph.py             # LangGraph setup
├── agents.py            # All multi-agent logic
├── llm.py               # Gemini LLM wrapper
├── requirements.txt     # Python dependencies
└── .env                 # API key (you create this)
```

---

## 🙌 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Google Generative AI](https://ai.google/discover/generative-ai/)
- [Streamlit](https://streamlit.io/)
- [Yahoo Finance via yfinance](https://pypi.org/project/yfinance/)

---

## 🧑‍💻 Author

Built with ❤️ by Akshay Ghatage  
For demos, ideas or questions, feel free to connect!

---

## 📄 License

MIT License – free to use, modify, and share.
