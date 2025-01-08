from dataclasses import dataclass


@dataclass
class Model:
    provider: str
    name: str

    @classmethod
    def tric(cls, model_name: str = ""):
        """Quick creator for Tric models"""
        return cls(provider="", name=model_name)

    @classmethod
    def anthropic(cls, model_name: str = ""):
        """Quick creator for Anthropic models"""
        return cls(provider="", name=model_name)
