from odmantic import Model, Field
from pydantic import root_validator
from functools import reduce
import base64


class RequestBody(Model):
    key: str = Field(primary_field=True)  # body keys+values encoded to base64
    body: dict
    duplicates: int = 1

    @root_validator(pre=True)
    def get_key(cls, values) -> dict:
        body_dict = dict(sorted(values["body"].items()))
        key = base64.b64encode(''.join(str(s) + str(body_dict[s]) for s in body_dict).encode('utf-8'))
        values["key"] = key.decode("utf-8")
        return values

# d1 = {"d": "2", "a": "4"}
# d2 = {"a": "4", "d": "2"}
# d1 = dict(sorted(d1.items()))
# d2 = dict(sorted(d2.items()))
# print(''.join(str(s) + str(d1[s]) for s in d1))
# print(''.join(str(s) + str(d1[s]) for s in d2))
# print(base64.b64encode(''.join(str(s) + str(d1[s]) for s in d1).encode('utf-8')))
# print(base64.b64encode(''.join(str(s) + str(d1[s]) for s in d2).encode('utf-8')))
