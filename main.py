import json

from agents.query_agent import IPLAgentInputSchema, ipl_query_agent
from config import get_logger
from services.run_query import run_duckdb_query

logger = get_logger(__name__)


def example_run(message: str):
    query_output = ipl_query_agent.run(IPLAgentInputSchema(user_query=message))
    return query_output


if __name__ == "__main__":
    user_query = "Who won the IPL 2025 final match? A team is considered to have won if they score more runs than the opposition team in a single match."
    logger.info("User Query: %s\n", user_query)
    llm_response = example_run(user_query)
    llm_response = json.loads(llm_response.model_dump_json())
    query = llm_response["duckdb_query"]
    # reasoning = llm_response["reasoning"] if "reasoning" in llm_response["reasoning"] else "No reasoning provided"
    logger.info("Generated DuckDB Query: %s\n", query)
    # logger.info("Reasoning: %s\n", reasoning)
    query_result = run_duckdb_query(query)
    logger.info("Generated DuckDB Query Result: %s\n", query_result)
