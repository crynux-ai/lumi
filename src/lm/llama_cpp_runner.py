from dataclasses import dataclass, field

from llama_cpp import Llama

from lumi import LM, LMInferenceOption, Message


@dataclass
class LlamaCppOption(LMInferenceOption):
    max_tokens: int = 32
    stop: list[str] = field(default_factory=lambda: ["Q:", "\n"])
    echo: bool = False


@dataclass
class LlamaCppRunner(LM):

    model_path: str = ""
    use_gpu: bool = True
    seed: int = -1
    context_len: int = -1
    chat_format: str = ""


    def __post_init__(self):
        super().__post_init__()
        args = {
            "model_path": self.model_path,
        }
        if self.use_gpu:
            args["n_gpu_layers"] = -1
        if self.seed > 0:
            args["seed"] = self.seed
        if self.context_len > 0:
            args["n_ctx"] = self.context_len
        if self.chat_format:
            args["chat_format"] = self.chat_format
        self.runner = Llama(**args)
        self.validate()


    def complete_text(self, query: str, option: LlamaCppOption) -> str:
        result = self.runner.create_completion(
            query,
            max_tokens=option.max_tokens,
            stop=option.stop,
            echo=option.echo)
        return result["choices"][0]["text"]

    def complete_chat(self, query: list[Message], option: LlamaCppOption) -> Message:
        result = self.runner.create_chat_completion(
            messages=[{"role": m.author, "content": m.content} for m in query]
        )
        return Message(
            author=result["choices"][0]["message"]["role"],
            content=result["choices"][0]["message"]["content"],
        )

