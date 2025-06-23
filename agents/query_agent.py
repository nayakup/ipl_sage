import instructor
import openai
from atomic_agents.agents.base_agent import (
    BaseAgent,
    BaseAgentConfig,
    BaseIOSchema,
)
from atomic_agents.lib.components.system_prompt_generator import SystemPromptGenerator
from pydantic import Field

from config import LLM_TEMPERATURE, ChatConfig, get_logger
from services.context_provider import IPLContextProvider

logger = get_logger(__name__)


class IPLAgentInputSchema(BaseIOSchema):
    """Schema for input to the RAG query agent."""

    user_query: str = Field(
        ..., description="The user's inquiry regarding IPL data, including the relevant input data schema"
    )


class IPLAgentOutputSchema(BaseIOSchema):
    """Schema for output from the RAG query agent."""

    # reasoning: str = Field(..., description="reasoning for the generated duckdb query, if requested by the user")
    duckdb_query: str = Field(
        ..., description="The duckdb that retrieves the results corresponding to the user's inquiry"
    )


logger.info("Creating Query Agent")
ipl_query_agent = BaseAgent(
    BaseAgentConfig(
        client=instructor.from_openai(openai.OpenAI(api_key=ChatConfig.api_key)),
        model=ChatConfig.model,
        system_prompt_generator=SystemPromptGenerator(
            background=[
                "You are an expert IPL (Indian Premier League) data analyst.",
                "You help users analyze IPL cricket data by generating duckdb query.",
                "You have access to a duckdb table called 'ipl' containing ball-by-ball IPL match data.",
                "For formulae on cricket statistics, refer to the official IPL website or cricket statistics resources.",
            ],
            steps=[
                "Understand the user's query about IPL data",
                "Generate appropriate duckdb query to answer the user's query",
                "Ensure the duckdb query is syntactically correct and efficient",
                "Return only the duckdb query without explanations unless asked",
            ],
            output_instructions=[
                "Generate duckdb query that works with the provided table 'ipl'",
                "Use proper duckdb query syntax and functions",
                "Handle edge cases and potential errors",
                "Do not include any comments or additional text in the query",
                "Return executable duckdb query",
                "Provide reasoning for the query if asked",
            ],
            context_providers={"CSV Schema Context": IPLContextProvider(title="CSV Schema Context")},
        ),
        input_schema=IPLAgentInputSchema,
        output_schema=IPLAgentOutputSchema,
        temperature=LLM_TEMPERATURE,
    )
)

if __name__ == "__main__":
    pass
