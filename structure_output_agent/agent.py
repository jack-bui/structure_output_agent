from pydantic import BaseModel, Field
from google.adk.agents import Agent

class financial(BaseModel):
    revenue:str = Field(description="The revenue in the financial statement, in million of USD, round to 2 decimals")
    cogs:str = Field(description="The cost of good sold in the financial statement, in million of USD, in million of USD, round to 2 decimals")
    net_income:str = Field(description="The net income in the financial statement, in million of USD, in million of USD, round to 2 decimals")
    note:str = Field(description="To inform the user if the currency is not in USD or if the financial information is unavailable")
root_agent = Agent (
    name="financial_structured_output_agent",
    model="gemini-2.0-flash",
    description=('''
        You are a helpful agent who read financial report and extract the required data.
        IMPORTANT:
        Your reply must be in a standard JSON with the following format
                {"revenue":"revenue amount in million USD,in million of USD, round to 2 decimals"}
                {"cogs":"cost of goods sold in million USD,in million of USD, round to 2 decimals"}
                {"net income":"net income in million USD,in million of USD, round to 2 decimals"}
                {"note":"to inform the user oif the currency is not in USD or if the information is not found"}
        If the information does not exist or the currency  is not in USD, inform the user and return all 0 value for the financial data
                 '''),
    output_schema=financial,
    output_key="statement"

)

