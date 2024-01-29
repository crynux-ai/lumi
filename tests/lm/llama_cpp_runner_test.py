import pytest

from lm import LlamaCppRunner, LlamaCppOption

def test_llamacpp_inference():
	runner = LlamaCppRunner(model_path="../../models/llama-7b.q4_0.gguf")
	res = runner.generate("hello", LlamaCppOption())
	assert res