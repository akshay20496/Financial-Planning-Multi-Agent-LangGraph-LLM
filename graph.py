from langgraph.graph import StateGraph, END
from agents import MultiAgent

class FinancialAdvisorGraph(StateGraph):
    def __init__(self):
        super().__init__(dict)
        self.multi_agent = MultiAgent()

        # Define thenodes
        self.add_node("start", self.multi_agent.parse_user_query)
        self.add_node("analyzer", self.multi_agent.profile_analyzer)
        self.add_node("risk", self.multi_agent.risk_model)
        self.add_node("allocate", self.multi_agent.asset_allocator)
        self.add_node("suggest", self.multi_agent.investment_suggestion)
        self.add_node("prices", self.multi_agent.fetch_etf_prices)
        self.add_node("summary", self.multi_agent.final_summary)
        
        # Define the flow of the graph
        self.set_entry_point("start")
        self.add_edge("start", "analyzer")
        self.add_edge("analyzer", "risk")
        self.add_edge("risk", "allocate")
        self.add_edge("allocate", "suggest")
        self.add_edge("suggest", "prices")
        self.add_edge("prices", "summary")
        self.set_finish_point("summary")
