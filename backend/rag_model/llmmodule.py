"""LLM wrapper with automatic task selection and safe error handling.

Attempts to load an appropriate transformers pipeline task for the provided model.
Tries tasks in priority order: text2text-generation, text-generation.
Logs detailed errors to the server log but never exposes them to API users.
"""
from transformers import pipeline
import logging
import os

logging.basicConfig()
logger = logging.getLogger(__name__)

# Prefer a small default instruction-tuned model. Change via quembedding if desired.
DEFAULT_MODEL = os.getenv('RAG_LLM_MODEL', 'google/flan-t5-base')

class LLM:
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.pipe = None
        self.task = None

        # Try candidate tasks in order. Some models support text2text, others require text-generation.
        candidate_tasks = [
            'text2text-generation',
            'text-generation'
        ]

        for t in candidate_tasks:
            try:
                # device_map="auto" may fail on CPU-only environments; let transformers decide.
                self.pipe = pipeline(t, model=self.model_name)
                self.task = t
                logger.info(f"Loaded model {self.model_name} with task {t}")
                break
            except Exception as e:
                logger.debug(f"Model {self.model_name} not usable with task {t}: {e}")
                self.pipe = None
                self.task = None

        if self.pipe is None:
            logger.error(f"Failed to initialize pipeline for model {self.model_name}; no supported task found.")
            # Do not raise; generation will fail gracefully returning None

    def generate(self, prompt: str, max_length: int = 512) -> str | None:
        """Generate text for prompt. On failure, log the exception and return None.
        Calling code must convert None to a user-friendly message.
        """
        if self.pipe is None:
            logger.error(f"No pipeline available for model {self.model_name}")
            return None

        try:
            # Adjust call signature for text-generation vs text2text-generation
            if self.task == 'text-generation':
                # text-generation expects a prompt string
                outputs = self.pipe(prompt, max_length=max_length, do_sample=False)
            else:
                # text2text-generation (T5-like) also supports same kwargs
                outputs = self.pipe(prompt, max_length=max_length, do_sample=False)

            # Normalize outputs into a string
            if isinstance(outputs, list) and outputs:
                out = outputs[0]
                if isinstance(out, dict):
                    return out.get('generated_text') or out.get('text') or str(out)
                return str(out)

            return str(outputs)

        except Exception as e:
            # Log full traceback to server log (safe), return None to caller
            logger.exception("LLM generation failed")
            return None
