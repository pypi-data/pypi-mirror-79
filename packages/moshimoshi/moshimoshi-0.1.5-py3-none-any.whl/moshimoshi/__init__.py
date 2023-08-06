import importlib
import json
from inspect import iscoroutine
from json import JSONDecodeError
from typing import Callable

from parse import parse


class moshi:
    def __new__(cls, to: str, *args, fallback: Callable = None, **kwargs):
        function_path = a_json = to

        # test hypothesis if to is a json
        try:
            call_detail = json.loads(a_json)

            function_path = call_detail["call"]

            # prioritize args and kwargs
            args = [*call_detail.get("args", tuple()), *args]
            kwargs = {**call_detail.get("kwargs", dict()), **kwargs}

        except JSONDecodeError:
            pass

        parsed = parse(r"{import_path}:{function_name:w}", function_path)
        if parsed is None:
            if fallback:
                return fallback(*args, **kwargs)
            else:
                raise Exception("argument `to` is invalid.")

        import_path = parsed["import_path"]
        function_name = parsed["function_name"]

        try:
            module = importlib.import_module(f"{import_path}")
            function = getattr(module, function_name)
            return function(*args, **kwargs)

        except ModuleNotFoundError as e:
            if fallback:
                return fallback(*args, **kwargs)

            else:
                raise e

    @classmethod
    async def moshi(cls, to: str, *args, fallback: Callable = None, **kwargs):
        ret = cls(to, *args, fallback=fallback, **kwargs)
        if iscoroutine(ret):
            return await ret
        else:
            return ret
