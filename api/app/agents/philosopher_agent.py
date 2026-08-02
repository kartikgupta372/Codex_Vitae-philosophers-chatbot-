"""
The core agentic piece: one PhilosopherAgent embodies ONE figure, grounded in
that figure's own data (figure.schema.json shape), speaking through the same
PersonaLLMClient port already built and proven working (adapters/llm/).

Deliberately simple, on purpose: no repository, no ports ceremony for this
piece specifically -- it just needs a figure's data dict and an LLM client.
Loading figures from Postgres instead of a JSON file, and retrieval-augmenting
from figure_chunks, are real later work (see the RAG-vs-expanded-prompt note
below for why that isn't built yet); this class is the reusable core those
will eventually call into.
"""
import json
from pathlib import Path

from app.adapters.llm.base import PersonaLLMClient


class PhilosopherAgent:
    def __init__(self, figure_data: dict, llm: PersonaLLMClient):
        self._figure = figure_data
        self._llm = llm
        self._system_prompt = self._build_system_prompt(figure_data)

    @classmethod
    def from_json_file(cls, path: str | Path, llm: PersonaLLMClient) -> "PhilosopherAgent":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data, llm)

    @property
    def name(self) -> str:
        return self._figure["name"]

    def stream(self, user_message: str, history: list[dict[str, str]] | None = None):
        """Returns an async iterator of text chunks -- same shape as the
        underlying PersonaLLMClient.stream(), just pre-loaded with this
        figure's system prompt."""
        return self._llm.stream(
            system_prompt=self._system_prompt,
            user_message=user_message,
            history=history,
        )

    @staticmethod
    def _build_system_prompt(figure: dict) -> str:
        """
        Uses most of the figure's JSON, not a compressed summary. Earlier
        version only included central_frame/register/cadence/never_does/
        failure_modes -- meaning a direct question like "what did they think
        about status" had no real material to draw on beyond what happened to
        be inferable from that summary. This version gives the model the
        actual positions, the operating manual, the applied examples, and the
        confidence notes, so it can answer specifically rather than generically.

        This is the "expand the prompt" choice over building RAG retrieval:
        at 12-44 figures, a full figure.json (~2.5-3K words) fits easily in
        Gemini's context window, so there's no real need for figure_chunks /
        pgvector / embeddings yet. Revisit if the roster grows enough that
        cramming the whole file in stops being cheap, or if retrieval quality
        genuinely needs narrowing to the most relevant section per question
        rather than handing over everything every turn.
        """
        voice = figure["voice"]
        beliefs = figure["core_beliefs"]
        who = figure["who_they_really_were"]
        limits = figure["limits_and_dangers"]
        manual = figure.get("operating_manual", {})
        powerful = figure.get("what_makes_them_powerful", {})
        confidence = figure.get("confidence_notes", {})

        never_does = "; ".join(voice["never_does"])
        failure_modes = "\n".join(
            f"  - {fm['distortion']} (looks like: {fm['looks_like']})"
            for fm in limits["failure_modes"]
        )
        positions = "\n".join(
            f"  - {key.replace('_', ' ').title()}: {pos['stance']}"
            + (f" Nuance: {pos['nuance']}" if pos.get("nuance") else "")
            + (f" NOT this: {pos['not_this']}" if pos.get("not_this") else "")
            for key, pos in beliefs["positions"].items()
        )
        flaws = "; ".join(who.get("flaws", []))
        contradictions = "; ".join(who.get("contradictions", []))
        behaviors = "; ".join(manual.get("behaviors", []))
        rules = "; ".join(manual.get("rules", []))
        decision_principles = "; ".join(manual.get("decision_principles", []))
        core_strengths = "; ".join(powerful.get("core_strengths", []))
        applied = "\n".join(
            f"  - When: {ex['situation']} -> {ex['how_it_lands']}"
            for ex in powerful.get("applied_examples", [])
        )
        contested = "; ".join(confidence.get("contested", []))
        attribution_warnings = "; ".join(confidence.get("attribution_warnings", []))
        who_careful = "; ".join(limits.get("who_should_be_careful", []))
        is_living = bool(figure.get("is_living"))

        if is_living:
            # PRD R1: living figures get a "scholar of" register, not first-person --
            # publicity-rights exposure is real, not a style preference. This branch
            # did not exist until now because every figure extracted so far happened
            # to be historical; Naval Ravikant is the first to actually exercise it.
            framing = (
                f"You are a knowledgeable scholar of {figure['name']} ({figure['lifespan']}), "
                f"speaking ANALYTICALLY ABOUT their documented public positions -- not "
                f"impersonating them, not claiming to BE them, and not generating opinions "
                f"or quotes in their voice as if they personally said them to this user. "
                f"{figure['name']} is a living person with their own voice and publicity "
                f"rights; speak in third person ('{figure['name']} has argued...', 'their "
                f"position is...'), grounded in what they have actually said and written "
                f"publicly. If asked what they 'would say' about something specific and "
                f"undocumented, be explicit that you are extrapolating from their known "
                f"positions, not quoting them."
            )
        else:
            framing = (
                f"You are having a conversation AS {figure['name']} ({figure['lifespan']}), "
                f"not a modern assistant describing them from the outside. This is a study "
                f"companion, not a claim to be the real person -- if the user seems genuinely "
                f"confused about that, clarify plainly without breaking voice more than needed."
            )

        return (
            f"{framing}\n\n"

            f"CENTRAL FRAME: {beliefs['central_frame']}\n"
            + (f"THE FLATTENED INTERNET VERSION (correct this if it comes up): {beliefs['internet_version']}\n\n" if beliefs.get("internet_version") else "\n")

            + f"REGISTER: {voice['register']}\n"
            f"CADENCE: {voice['cadence']}\n"
            + (f"VOCABULARY YOU ACTUALLY REACH FOR: {', '.join(voice['vocabulary'])}\n" if voice.get("vocabulary") else "")
            + (f"METAPHOR DOMAINS: {', '.join(voice['metaphor_domains'])}\n" if voice.get("metaphor_domains") else "")
            + f"NEVER DO (out of character): {never_does}\n\n"

            + "CONVERSATIONAL DEPTH: This should feel like an actual, unhurried "
            "conversation with you, not a quick answer to a question. Give full, "
            "developed responses that work through the user's specific situation "
            "in your real voice, cadence and metaphor domains -- not a summary of "
            "your position, a demonstration of it. Take the space a real exchange "
            "with you would take. Draw on your actual positions, operating manual "
            "and applied examples above concretely rather than staying abstract.\n\n"

            f"WHO YOU REALLY WERE: {who['context']}\n"
            f"Your actual flaws, own them if relevant, don't hide behind the flattering version: {flaws}\n"
            f"Contradictions in your own thought/life, acknowledge these if pressed rather than smoothing them over: {contradictions}\n\n"

            f"YOUR ACTUAL POSITIONS on the things people ask about -- use these to answer "
            f"specifically rather than generically. Each includes the common misreading to "
            f"correct if the user brings it up:\n{positions}\n\n"

            + (f"WHAT MAKES YOUR THINKING USEFUL: {core_strengths}\n" if core_strengths else "")
            + (f"WORKED EXAMPLES of how you reframe ordinary problems:\n{applied}\n\n" if applied else "\n")

            + (f"YOUR OPERATING MANUAL, offer pieces of this when relevant, don't dump it all at once:\n"
               f"  Behaviors you'd recommend: {behaviors}\n"
               f"  Rules -- things you'd say never to do: {rules}\n"
               f"  Decision principles: {decision_principles}\n\n" if manual else "")

            + f"WHERE YOUR OWN PHILOSOPHY GOES WRONG in a real person's hands -- name this "
            f"honestly if it's relevant, don't only defend the idea:\n{failure_modes}\n"
            + (f"Who should be especially careful with this way of thinking: {who_careful}\n\n" if who_careful else "\n")

            + (f"WHAT'S GENUINELY CONTESTED OR UNCERTAIN about your own record -- don't "
               f"overclaim certainty here if it comes up: {contested}\n" if contested else "")
            + (f"LINES FALSELY ATTRIBUTED TO YOU that people may bring up as quotes -- correct "
               f"these if asked, don't validate them: {attribution_warnings}\n\n" if attribution_warnings else "\n")

            + f"Safety stopgap (the real guardrail layer runs before you're even called now, "
            f"but stay alert regardless): if the user's message reads as crisis-adjacent -- "
            f"self-harm, wanting to disappear, acute despair -- drop the persona entirely and "
            f"respond as a direct, caring modern voice pointing them to real support. Character "
            f"consistency matters far less than this."
        )
