from flask import Blueprint, g, jsonify, request
from config import Config
from middleware.auth_middleware import token_required
from models import db
from services.llm_service import LLMError, analyze_code

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.post("/analyze")
@token_required
def analyze():
    data = request.get_json(silent=True) or {}
    code = data.get("code") or ""
    hint = (data.get("language") or "").strip() or None

    if not code.strip():
        return jsonify(error="Paste or upload some code first."), 400
    if len(code) > Config.MAX_CODE_CHARS:
        return jsonify(error=f"Code is too long. The limit is {Config.MAX_CODE_CHARS} characters."), 413

    try:
        report = analyze_code(code, hint)
    except LLMError as e:
        return jsonify(error=str(e)), 502

    report["id"] = db.save_report(g.user_id, report["language"], code, report)
    report["code"] = code
    return jsonify(report)
