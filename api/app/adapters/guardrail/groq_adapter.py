"""
Real implementation. This is PRD R3 / TASKS 2.9 -- non-negotiable per your own
docs, so this wasn't treated as optional to skip while everything else got
built. What it deliberately does NOT try to be: a comprehensive clinical
classifier. It's a fast, cheap first pass that fails closed.

Calibration matters more than it looks like it would. This app WILL get a lot
of messages about death, suffering, and struggle -- that's the actual subject
matter of half the roster. A classifier tuned too broadly trips on ordinary
Stoic-philosophy conversation constantly, which trains users to ignore it
right when it matters. Tuned too narrowly, it misses real signal. The prompt
below tries to hold that line explicitly with contrasting examples rather
than leaving it to the model's untuned judgment.

IMPORTANT, found via live testing, not theory: openai/gpt-oss-20b is a
reasoning model -- it spends tokens on internal chain-of-thought before
emitting the final SAFE/CRISIS token. An earlier version of this file used
max_tokens=8 and checked `"CRISIS" in verdict`; the model was silently
getting cut off mid-reasoning (finish_reason="length", content=""), returning
successfully with empty content, and that empty string evaluated to
NOT tripped -- a false SAFE on a live test of "I don't want to be here
anymore," which is literally one of this file's own CRISIS examples below.
No exception was ever raised, so the fail-closed exception handler never
fired either. Fixed two ways: enough max_tokens for the model to actually
finish reasoning, AND inverted parse logic so anything that ISN'T an
explicit SAFE verdict -- empty, truncated, garbled, genuinely ambiguous --
defaults to tripped. Both matter; don't remove either one to "simplify."
"""
from groq import AsyncGroq

from app.adapters.guardrail.base import GuardrailClient, GuardrailResult

_CLASSIFIER_PROMPT = """You are a safety classifier for a philosophy study app. Users discuss philosophers who wrote extensively about death, suffering, and struggle -- philosophical discussion of these themes is NORMAL and must NOT trip this classifier.

Trip ONLY if the message itself suggests the person may be in genuine personal crisis right now: suicidal ideation, wanting to disappear or not exist, active self-harm, or acute personal despair directed at themselves -- not an abstract or academic question.

Respond with exactly one word, and nothing else: SAFE or CRISIS.

SAFE examples (do not trip):
- "What did Marcus Aurelius think about death?"
- "How do I deal with the fact that everything ends?"
- "I'm really struggling with a hard situation at work"
- "Camus says suicide is the one serious philosophical question -- what does he mean?"

CRISIS examples (trip):
- "I don't want to be here anymore"
- "what would you say about wanting to disappear" (asked in a personal, not academic, register)
- Any explicit statement of self-harm intent or method
"""


class GroqGuardrailAdapter(GuardrailClient):
    def __init__(self, api_key: str, model: str):
        self._client = AsyncGroq(api_key=api_key)
        self._model = model

    async def check(self, message: str) -> GuardrailResult:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": _CLASSIFIER_PROMPT},
                    {"role": "user", "content": message},
                ],
                # gpt-oss-20b reasons before answering -- see module docstring.
                # Verified empirically: 8 was not enough and failed silently.
                max_tokens=300,
                temperature=0,
            )
            verdict = (response.choices[0].message.content or "").strip().upper()
            # Fail closed at the PARSING level, not just on exceptions: only
            # skip tripping if the model explicitly and clearly said SAFE.
            # Anything else -- empty, truncated, garbled, a genuinely unclear
            # answer -- defaults to tripped. This is the fix for the false
            # negative found in live testing; do not invert this back to
            # checking for "CRISIS" instead.
            tripped = "SAFE" not in verdict
            return GuardrailResult(tripped=tripped, reason="crisis_adjacent" if tripped else None)
        except Exception:
            # Fail CLOSED on the exception path too -- see base.py's docstring.
            return GuardrailResult(tripped=True, reason="guardrail_check_failed")
