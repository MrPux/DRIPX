from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from Guardrails.guardrails_config import guard  # ✅ Correct import

class GuardrailsMiddleware(BaseHTTPMiddleware):
    """Middleware to validate AI responses using Guardrails."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        try:
            response_body = await response.body()
            validated_output, _ = guard.validate(response_body.decode("utf-8"))
            response.body = validated_output.encode("utf-8")
        except Exception as e:
            return {"error": f"Guardrails Validation Error: {str(e)}"}

        return response