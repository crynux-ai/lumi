from dataclasses import dataclass, field

from llama_cpp import Llama

from lumi import LM, LMInferenceOption


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
        self.runner = Llama(**args)


    def generate(self, query: str, option: LlamaCppOption) -> str:
        result = self.runner(
            query,
            max_tokens=option.max_tokens,
            stop=option.stop,
            echo=option.echo)
        return result["choices"][0]["text"]
        