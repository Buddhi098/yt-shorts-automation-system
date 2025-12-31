import random
from langchain_openai import ChatOpenAI
from .prompts import PROMPT_TEMPLATE, parser, THEMES
from app.utils.save_json import save_json
from app.config.settings import settings

class ContentGenerator:
    def __init__(self , logger):
        self.llm = ChatOpenAI(model=settings.ai.model,
                            temperature=settings.ai.temperature)
        self.logger = logger

    def generate(self, theme: str):
        try:
            chain = PROMPT_TEMPLATE | self.llm | parser
            result = chain.invoke({
                "theme": theme,
                "format_instructions": parser.get_format_instructions()
            })
            return result.model_dump()
        except Exception as e:
            self.logger.error(f"Failed to generate content for theme '{theme}': {e}")
            return None

    def generate_batch(self, n: int = settings.ai.num_responses):
        if(n <= 0):
            self.logger.warning("Requested number of responses is non-positive. Returning empty list.")
            return []
        if(settings.files.motivational_output.exists()):
            self.logger.info(f"Output file {settings.files.motivational_output} already exists. Skipping generation.")
            return []
        
        results = []
        for idx in range(n):
            theme = random.choice(THEMES)
            data = self.generate(theme)
            if data:
                data["id"] = idx + 1
                results.append(data)
            self.logger.info(f"Generated content {idx + 1}/{n} for theme '{theme}'")

        try:
            save_json(results, settings.files.motivational_output)
            self.logger.info(f"Generated and saved {len(results)} motivational content pieces.")
        except RuntimeError as e:
            self.logger.error(f"Failed to save motivational content: {e}")

        return results
