from guardrails import Guard
from models import DisasterData  # ✅ Corrected Import

# ✅ Use Guardrails for validation
guard = Guard.for_pydantic(DisasterData)