import json
import codecs
from yt_shared.schemas.success import SuccessDownloadPayload
from yt_shared.schemas.error import ErrorDownloadPayload

with open("error.json", "r") as f:
    data = f.read()

# Fix python string escapes \x \n \t in the raw text
def decode_escapes(s):
    return codecs.decode(s, 'unicode_escape')

try:
    data = decode_escapes(data)
    # now encode to utf-8 string, because unicode_escape might produce latin-1
    data = data.encode('latin1').decode('utf-8')
    payload_dict = json.loads(data)
    SuccessDownloadPayload.model_validate(payload_dict)
    print("SuccessPayload validated!")
except Exception as e:
    print("ValidationError:", e)
