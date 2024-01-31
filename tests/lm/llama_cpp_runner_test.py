import pytest

from lm import LlamaCppRunner, LlamaCppOption
from lumi import Message

def tes1t_complete_text():
	runner = LlamaCppRunner(
		name="llama7b",
		model_path="../../models/llama-7b.q4_0.gguf")
	res = runner.complete_text("hello", LlamaCppOption())
	assert res


def test_complete_chat():
	runner = LlamaCppRunner(
		name="llama7b",
		model_path="../../models/llama-7b.q4_0.gguf",
		chat_format="llama-2")
	query = [
		Message(
			author="system",
			content="You are an assistant who perfectly describes images."),
		Message(
			author="user",
			content="Describe this image in detail please."),
	]
	res = runner.complete_chat(query, LlamaCppOption())
	assert res
