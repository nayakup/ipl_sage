import logging
import os
from dataclasses import dataclass

from pydantic import BaseModel, Field
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


class APIKeyNotFoundError(Exception):
    """API Key Not Found Exception"""

    def __init__(self):
        super().__init__("API key not found. Please set the OPENAI_API_KEY environment variable.")


def get_api_key() -> str:
    """Retrieve API key from environment or raise error"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise APIKeyNotFoundError

    return api_key


@dataclass
class ChatConfig:
    """Configuration for the chat application"""

    api_key: str = get_api_key()  # This becomes a class variable
    model: str = "gpt-4.1-nano"
    exit_commands: set[str] = frozenset({"/exit", "exit", "quit", "/quit"})

    def __init__(self):
        # Prevent instantiation
        error_msg: str = "ChatConfig is not meant to be instantiated"
        raise TypeError(error_msg)


class MatchData(BaseModel):
    """Schema of the input CSV Files"""

    season: str = Field(..., description="The season in which the match is played represented by the year")
    match_id: str = Field(..., description="Unique identifier for the match.")
    phase: str = Field(..., description="The phase of the tournament")
    match_no: int = Field(..., description="The match number in the tournament.")
    date: str = Field(..., description="The date of the match")
    venue: str = Field(..., description="The venue where the match is held. Format: Stadium, City")
    batting_team: str = Field(..., description="The team that is batting.")
    bowling_team: str = Field(..., description="The team that is bowling.")
    innings: int = Field(..., description="The innings number (1 or 2).")
    over: float = Field(
        ...,
        description="The delivery/ball of the innings. In regex pattern ^(20(\.([0-5]))?|[1-9]?\d(\.([0-5]))?)$",  # noqa: W605
    )
    striker: str = Field(..., description="The player who is currently batting.")
    bowler: str = Field(..., description="The player who is currently bowling.")
    runs_of_bat: int = Field(..., description="The runs scored by the batsman in that delivery.")
    extras: int = Field(..., description="The total number of extras in that delivery.")
    wide: int = Field(..., description="The number of wide balls in that delivery.")
    legbyes: int = Field(..., description="The number of leg-byes in that delivery.")
    byes: int = Field(..., description="The number of byes in that delivery.")
    noballs: int = Field(..., description="The number of no-balls in that delivery.")
    wicket_type: int = Field(..., description="The way the player was dismissed (e.g., bowled, caught), if applicable.")
    player_dismissed: str = Field(..., description="The name of the player who got dismissed, if applicable.")
    fielder: str = Field(..., description="The name of the fielder involved in the dismissal, if applicable.")
    # over_ceil: float = Field(
    #     ..., description="The actual over number, rounded up to the next integer. possible values: 1, 2, ..., 20"
    # )


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger with a RichHandler using a custom theme.

    Args:
        name (str): The name of the logger (typically __name__).

    Returns:
        logging.Logger: Configured logger instance.

    """
    custom_theme = Theme(
        {
            "logging.level.debug": "orange1",
            "logging.level.info": "bold green",
            "logging.level.warning": "orange1",
            "logging.level.error": "bold red",
            "logging.level.critical": "bold red",
        }
    )
    console = Console(theme=custom_theme)

    # Configure logging with RichHandler
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(console=console)],
    )
    logger = logging.getLogger(name)
    return logger


DATABASE_NAME = "ipldatabase.db"
DATABASE_TABLE = "ipl"
LLM_TEMPERATURE = 0  # Lower temperature for more deterministic output
