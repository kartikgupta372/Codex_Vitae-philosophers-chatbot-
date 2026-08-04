import json

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse

from app.adapters.guardrail.base import GuardrailClient
from app.api.deps import get_chat_service, get_guardrail_client
from app.core.config import Settings, get_settings
from app.core.rate_limit import check_rate_limit
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
async def chat(
    request: Request,
    body: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    guardrail: GuardrailClient = Depends(get_guardrail_client),
    settings: Settings = Depends(get_settings),
    _rate_limit: None = Depends(check_rate_limit),
):
    """
    SSE stream, per TECH-STACK-AND-WORKFLOW.md \u00a72 ("POST /chat streaming (SSE)").

    Guardrail (PRD R3 / TASKS 2.9) runs BEFORE the persona is ever called, not
    as a post-filter -- if it trips, the persona adapter is never invoked at
    all. Runs sequentially rather than concurrently with retrieval for now,
    since there's no retrieval step yet to run it alongside (see chat_service.py
    for why -- figure data comes straight from disk, not pgvector). Revisit
    once real RAG retrieval exists, per TECH-STACK-AND-WORKFLOW.md \u00a77's
    latency budget.

    The first SSE event is always {"guardrail_tripped": bool} before any
    content, so the frontend can relabel the reply away from the philosopher's
    name BEFORE any text arrives, not after.
    """
    agent = service.get_agent(body.slug)
    if agent is None:
        raise HTTPException(
            status_code=404,
            detail=f"No agent available yet for '{body.slug}' -- this figure hasn't been extracted.",
        )

    guardrail_result = await guardrail.check(body.message)
    history = [{"role": m.role, "content": m.content} for m in body.history]

    async def event_stream():
        yield f"data: {json.dumps({'guardrail_tripped': guardrail_result.tripped})}\n\n"

        if guardrail_result.tripped:
            yield f"data: {json.dumps({'chunk': settings.crisis_response_message})}\n\n"
        else:
            async for chunk in agent.stream(body.message, history=history):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
