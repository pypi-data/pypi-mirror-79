from typing import Optional, Dict, Any

from loguru import logger

import ciphey
from ciphey.iface import registry, Translation, ParamSpec


@registry.register
class Leet(ciphey.iface.Decoder[str, str]):
    @staticmethod
    def getTarget() -> str:
        return "leet"

    def decode(self, text: str) -> Optional[str]:
        for src, dst in self.translate.items():
            text = text.replace(src, dst)
        return text

    @staticmethod
    def getParams() -> Optional[Dict[str, Dict[str, Any]]]:
        pass

    @staticmethod
    def priority() -> float:
        return 0.05

    def __init__(self, config: ciphey.iface.Config):
        super().__init__(config)
        self.translate = config.get_resource(self._params()["dict"], Translation)

    @staticmethod
    def getParams() -> Optional[Dict[str, ParamSpec]]:
        return {
            "dict": ParamSpec(
                desc="The leetspeak dictionary to use",
                req=False,
                default="cipheydists::translate::leet",
            )
        }