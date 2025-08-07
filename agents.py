import yfinance as yf
import pandas as pd 
import re
import json
import os
from llm import LLM

class MultiAgent:
    def __init__(self):
        self.model = LLM("gemini-2.5-flash", 0.3).get_model()

    # ==== 1. User Query Parser ====
    def parse_user_query(self, state):
        user_query = state["user_input"]
        prompt = f"""
        Extract structured data from this user query. Return only raw JSON:

        \"\"\"{user_query}\"\"\"

        Format:
        {{
            "age": 29,
            "goal": "retirement / gold / child education / real estate / emergency fund / insurance / marriage / tax saving / vacation",
            "income": 6000000,
            "horizon": 25,
            "location": "Pune",
            "reason": "Purandar is growing due to airport"
        }}
        """
        result = self.model.predict(prompt).strip()
        print("🔎 Raw LLM output:", result)  # <-- Add this for debugging

        # --- extract JSON from LLM output ---
        match = re.search(r'\{.*?\}', result, re.DOTALL)
        if match:
            try:
                extracted = json.loads(match.group(0))
                print("✅ Extracted JSON:", extracted)  # <-- Add this too
                state["user_input"] = extracted
            except Exception as e:
                state["error"] = f"Parse failed after regex: {e}\nRaw match: {match.group(0)}"
                print(state["error"])  # Log the error clearly

        return state

    # ==== 2. Profile Analyzer ====
    def profile_analyzer(self, state):
        if "error" in state:
            return state

        profile = state["user_input"]

        # ✅ Check type safety
        if isinstance(profile, str):
            state["error"] = "❌ profile_analyzer expected dict, got string instead."
            return state
        
        prompt = f"""
        Analyze this user profile in the Indian financial context:
        - Age: {profile['age']}
        - Goal: {profile['goal']}
        - Investment Horizon: {profile['horizon']} 
        - Income: ₹{profile['income']}
        - Location: {profile['location']}
        - Reason: {profile['reason']}

        Give a short summary and note any key financial constraints.
        """
        state["profile_summary"] = self.model.predict(prompt)
        return state

    # ==== 3. Risk Model ====
    def risk_model(self,state):
        profile = state["user_input"]
        prompt = f"""
        Based on the user's age ({profile['age']}) and investment horizon ({profile['horizon']}), 
        estimate their risk tolerance (low, medium, high) in the Indian market. Give a 1-line justification.
        """
        state["risk_profile"] = self.model.predict(prompt)
        return state

    # ==== 4. Asset Allocator ====
    def asset_allocator(self, state):
        prompt = f"""
        You are a SEBI-registered Indian financial advisor.

        Based on the user's risk profile: "{state['risk_profile']}", suggest an ideal asset allocation.

        Respond in strict JSON format:
        {{
        "stocks": 60,
        "bonds": 30,
        "cash": 10
        }}

        - Ensure total = 100
        - Do not include any explanation or commentary
        """
        raw = self.model.predict(prompt).strip()

        # Try to parse clean JSON
        try:
            allocation = json.loads(re.search(r'\{.*?\}', raw, re.DOTALL).group(0))
            state["allocation"] = allocation
        except Exception as e:
            state["allocation"] = raw  # fallback in case parsing fails
            state["error"] = f"⚠️ Allocation parse failed: {e}\nRaw output:\n{raw}"

        return state

    # ==== 5. Investment Suggestion ====
    def investment_suggestion(self, state):
        profile = state["user_input"]
        allocation = state["allocation"]
        goal = profile.get("goal", "").lower()
        location = profile.get("location", "")
        reason = profile.get("reason", "")

        prompt = f"""
        You are a certified Indian financial advisor.

        The user has the following profile:
        - Age: {profile['age']}
        - Income: ₹{profile['income']}
        - Investment Horizon: {profile['horizon']} years
        - Goal: {goal}
        - Location: {location}
        - Reason: {reason}
        - Risk profile: {state['risk_profile']}
        - Suggested Allocation: {allocation}

        Recommend a goal-specific investment strategy. If the goal is:
        - Gold: suggest suitable gold ETFs
        - Real Estate: suggest REITs or related ETFs
        - Retirement: suggest diversified long-term equity ETFs
        - Tax saving: suggest ELSS or NPS-like strategies
        - Emergency fund: suggest highly liquid options
        - Vacation / marriage / education: suggest low-to-medium risk SIPs

        Use this list of ETFs:
        - Stocks: NIFTYBEES.NS, ICICINIFTY.NS, KOTAKNIFTY.NS
        - Bonds: GILT10Y.NS, BHARATBOND.NS
        - Cash: LIQUIDETF.NS, ICICILIQUID.NS
        - Gold: GOLDETF.NS, SOVEREIGNGOLD.NS, HDFCGOLD.NS
        - Real Estate: REITETF.NS, REALTYETF.NS, NIFTYREALTY.NS

        Give recommendations for **each relevant category only**. For example, if goal is gold, include gold ETFs + asset plan. If it’s real estate, suggest REITs. Justify your picks in 1–2 lines each.
        """

        state["etf_suggestions"] = self.model.predict(prompt)
        return state

    # ==== 6. Fetch Live Prices using yfinance ====
    def fetch_etf_prices(self, state):
        text = state["etf_suggestions"]
        tickers = re.findall(r'\b[A-Z]{3,10}\.NS\b', text)
        etf_data = {}

        for ticker in tickers:
            try:
                ticker_obj = yf.Ticker(ticker)
                hist = ticker_obj.history(period="5d")

                if hist.empty:
                    etf_data[ticker] = "No historical data found."
                    continue

                prices = hist["Close"]
                # Sort and format prices
                formatted = {
                    date.strftime("%Y-%m-%d"): f"₹{round(price, 2)}"
                    for date, price in prices.items()
                }
                etf_data[ticker] = formatted
            except Exception as e:
                etf_data[ticker] = f"Error fetching: {e}"

        state["etf_prices"] = etf_data
        return state

    # ==== 7. Final Summary ====
    def final_summary(self,state):
        summary = f"""
        Profile Summary:
    {state['profile_summary']}

        Risk Profile:
    {state['risk_profile']}

        Allocation Plan:
    {state['allocation']}
    
        Recommended Indian ETFs:
    {state['etf_suggestions']}

        Live ETF Prices (Last 5 Days in ₹ INR):
    """
        # Format ETF prices as Markdown tables
        for ticker, prices in state["etf_prices"].items():
            summary += f"\n### {ticker} Prices\n"
            if isinstance(prices, dict):
                summary += "| Date | Price (₹) |\n|------|-----------|\n"
                for date, price in prices.items():
                    summary += f"| {date} | {price} |\n"
            else:
                summary += f"{prices}\n"

        state["summary"] = summary
        return state

    