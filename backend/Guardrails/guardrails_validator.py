from guardrails_config import guard

def validate_ai_response(response_text: str) -> str:
    """Validates AI-generated text using Guardrails before sending to frontend."""
    try:
        validated_output, _ = guard.validate(response_text)
        return validated_output
    except Exception as e:
        return f"Guardrails Validation Error: {str(e)}"