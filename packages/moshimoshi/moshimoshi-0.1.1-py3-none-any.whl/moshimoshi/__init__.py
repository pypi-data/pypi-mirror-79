import importlib
import json
from inspect import iscoroutine
from json import JSONDecodeError

from parse import parse


class moshi:
    def __new__(cls, *args, **kwargs):
        function_path = aJson = args[0]

        # isolate fallback from kwargs
        fallback = kwargs.get("fallback")
        if fallback:
            del kwargs["fallback"]

        try:
            call_detail = json.loads(aJson)

            function_path = call_detail["call"]
            # prioritize args and kwargs
            args = [*call_detail["args"], *args]
            kwargs = {**call_detail["kwargs"], **kwargs}

        except JSONDecodeError as e:
            raise e

        parsed = parse(r"{import_path}:{function_name:w}", function_path)
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

    @staticmethod
    async def moshi(*args, **kwargs):
        function_path = aJson = args[0]

        # isolate fallback from kwargs
        fallback = kwargs.get("fallback")
        if fallback:
            del kwargs["fallback"]

        try:
            call_detail = json.loads(aJson)

            function_path = call_detail["call"]
            # prioritize args and kwargs
            args = [*call_detail["args"], *args]
            kwargs = {**call_detail["kwargs"], **kwargs}

        except JSONDecodeError as e:
            raise e

        parsed = parse(r"{import_path}:{function_name:w}", function_path)
        import_path = parsed["import_path"]
        function_name = parsed["function_name"]

        try:
            module = importlib.import_module(f"{import_path}")
            function = getattr(module, function_name)
            ret = function(*args, **kwargs)
            if iscoroutine(ret):
                await ret

        except ModuleNotFoundError as e:
            if fallback:
                ret = fallback(*args, **kwargs)
                if iscoroutine(ret):
                    await ret

            else:
                raise e
