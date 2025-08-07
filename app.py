import streamlit as st
from graph import FinancialAdvisorGraph

st.title("AI-Powered Financial Advisor 🤖💰")


user_input = st.text_area(
    "Enter your financial goal (e.g., I want to save for my child's education in 25 years)"
)

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter your financial goal before submitting.")
    else:
        graph = FinancialAdvisorGraph()
        runnable = graph.compile()
        result = runnable.invoke({"user_input": user_input})
        st.markdown("### Advisor's Recommendation")
        st.write(result["summary"])
