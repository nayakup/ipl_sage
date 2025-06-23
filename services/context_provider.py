from atomic_agents.lib.components.system_prompt_generator import SystemPromptContextProviderBase

from services.preprocess import PreprocessIPLData


class IPLContextProvider(SystemPromptContextProviderBase):
    """Provide IPL Data Schema as context"""

    def __init__(self, title: str):
        super().__init__(title=title)

    def get_info(self) -> str:
        return PreprocessIPLData().generate_schema_description_duckdb()
