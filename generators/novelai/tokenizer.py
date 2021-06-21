from transformers import GPT2Tokenizer
import struct, base64

tokenizer = GPT2Tokenizer("encoder.json", "vocab.bpe")

def encode(txt: str) -> list:
    return tokenizer.encode(txt)

def decode(data: list) -> str:
    return tokenizer.decode(data)

def ids_to_b64_uint16_buf(tokenized_ids: list) -> str:
    encoded_ids = b"".join([struct.pack("H", token) for token in tokenized_ids])
    final_output = base64.b64encode(encoded_ids).decode("utf-8")
    return final_output

def b64_uint16_buf_to_ids(txt: str) -> str:
    encoded_ids = base64.b64decode(txt)
    tokenized_ids_native = memoryview(encoded_ids).cast("H")
    return tokenized_ids_native

test_encoded = ids_to_b64_uint16_buf(encode("test"))
assert test_encoded == "SCQ=", "Incorrect encoding"

test_decoded = decode(b64_uint16_buf_to_ids(test_encoded))
assert test_decoded == "test", "Incorrect decoding"