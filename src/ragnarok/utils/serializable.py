import json
from typing import Any, Dict


class JSONSerializable:
    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=self._json_default)

    @staticmethod
    def _json_default(obj: Any) -> Any:
        if isinstance(obj, JSONSerializable):
            return obj.to_dict()
        elif hasattr(obj, "__dict__"):
            return obj.__dict__
        else:
            return str(obj)
