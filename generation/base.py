from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        topic: str
    ) -> str:
        """
        Generate an essay for the given topic.
        """
        raise NotImplementedError