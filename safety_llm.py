"""
SiteVision AI - LLM & NLP Safety Audit Generator
Converts detection telemetry and worker identity into concise, professional 2-3 sentence
construction safety reports. Supports Google Gemini LLM API and an offline local NLP engine.
"""

import os
import random

# Try importing Google Gemini client
try:
    from google import genai
    from google.genai import types
    GEMINI_CLIENT_AVAILABLE = True
except Exception:
    try:
        import google.generativeai as legacy_genai
        GEMINI_CLIENT_AVAILABLE = True
    except Exception:
        GEMINI_CLIENT_AVAILABLE = False


def generate_local_nlp_report(telemetry: dict, worker_profile: dict = None) -> str:
    """
    Zero-latency, offline rule-based NLP engine that generates realistic
    natural language safety officer audits from detection telemetry and worker profile.
    """
    helmet = telemetry.get("helmet", False)
    vest = telemetry.get("vest", False)
    smoking = telemetry.get("smoking", False)
    
    worker_name = worker_profile.get("name", "Personnel") if worker_profile else "Personnel"
    worker_id = worker_profile.get("id", "WRK-8901") if worker_profile else "WRK-8901"
    worker_role = worker_profile.get("role", "Worker") if worker_profile else "Worker"
    
    if smoking:
        templates = [
            f"🚨 CRITICAL DLP BREACH: Worker {worker_name} ({worker_id}, {worker_role}) observed smoking / using open flame on active job site. Per OSHA 1926.151 fire prevention protocol, badge clearance is immediately BLOCKED and site turnstiles locked.",
            f"🚨 SECURITY VIOLATION (DLP): Combustible hazard detected for {worker_name} ({worker_id}). Site access credentials have been revoked instantly and a mandatory safety supervisor dispatch debrief has been logged.",
            f"🚨 IMMEDIATE WORKSTOP TRIGGER: Active smoking identified for {worker_name} on site camera. Automated safety policy has locked Worker ID {worker_id}; turnstile 01 held until safety clearance."
        ]
        return random.choice(templates)

    if not helmet and not vest:
        return f"⚠️ SEVERE PPE INFRACTION: {worker_name} ({worker_id}, {worker_role}) detected without required hardhat and high-visibility safety vest. Immediate site entry is denied until full Class-2 protective equipment is equipped and re-scanned."

    if not helmet:
        return f"⚠️ PPE WARNING: High-visibility vest verified for {worker_name} ({worker_id}), but mandatory hardhat is missing. Head injury risk exceeds OSHA tolerance; personnel must equip approved head protection before proceeding past staging."

    if not vest:
        return f"⚠️ PPE WARNING: Hardhat verified for {worker_name} ({worker_id}), but required high-visibility safety apparel is missing. Low-visibility hazard flagged; personnel must wear an approved reflective vest prior to entering active transit lanes."

    # All Safe
    safe_templates = [
        f"✅ SAFETY VERIFIED: {worker_name} ({worker_id}, {worker_role}) successfully cleared with approved hardhat and Class-2 high-visibility vest. Site access is granted under standard operational protocol with zero DLP infractions.",
        f"✅ FULL PPE CLEARANCE: Both cranial protection and reflective apparel confirmed for {worker_name}. Worker clearance token authenticated for active construction zone entry.",
        f"✅ ACCESS APPROVED: Complete safety equipment verified for {worker_name} ({worker_id}) with zero open-flame hazards. Personnel is cleared for shift operations at Turnstile 01."
    ]
    return random.choice(safe_templates)


def generate_safety_report(telemetry: dict, api_key: str = None, worker_profile: dict = None) -> dict:
    """
    Generates a natural language safety assessment using Gemini API if key is provided,
    otherwise gracefully falls back to the local NLP safety engine.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    worker_name = worker_profile.get("name", "Personnel") if worker_profile else "Personnel"
    worker_id = worker_profile.get("id", "WRK-8901") if worker_profile else "WRK-8901"
    worker_role = worker_profile.get("role", "Worker") if worker_profile else "Worker"

    # If no key is configured, use local NLP engine
    if not key:
        report_text = generate_local_nlp_report(telemetry, worker_profile=worker_profile)
        return {
            "source": "Local Safety Engine (Offline)",
            "report": report_text,
            "status": telemetry.get("status", "SAFE"),
            "dlp_blocked": telemetry.get("dlp_blocked", False)
        }

    # Use Google Gemini LLM
    try:
        prompt = f"""
You are SiteVision AI, an autonomous construction site safety compliance officer.
Analyze the following real-time visual detection telemetry:
- Worker Name: {worker_name}
- Worker ID: {worker_id}
- Role / Designation: {worker_role}
- Hardhat / Helmet Detected: {"YES (Compliant)" if telemetry.get("helmet") else "NO (Missing)"}
- High-Visibility Safety Vest Detected: {"YES (Compliant)" if telemetry.get("vest") else "NO (Missing)"}
- Smoking / Open Flame Detected: {"CRITICAL DETECTED (DLP VIOLATION)" if telemetry.get("smoking") else "None (Clear)"}
- Current Clearance Status: {telemetry.get("status", "SAFE")}

Instruction:
Write a concise, professional 2-3 sentence safety evaluation report mentioning the worker by name and ID.
- If smoking is detected, explicitly state that {worker_name}'s ID clearance ({worker_id}) is immediately BLOCKED due to DLP fire/safety violation.
- If PPE is missing, state the specific hazard and required remedial action.
- If all PPE is compliant and no smoking is present, issue an access granted clearance.
Keep the tone authoritative, clear, and actionable. Do not use markdown bullet points in the short summary.
"""

        try:
            from google import genai
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            report_text = response.text.strip()
            return {
                "source": "Gemini 2.5 Flash",
                "report": report_text,
                "status": telemetry.get("status", "SAFE"),
                "dlp_blocked": telemetry.get("dlp_blocked", False)
            }
        except Exception:
            import google.generativeai as legacy_genai
            legacy_genai.configure(api_key=key)
            model = legacy_genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            report_text = response.text.strip()
            return {
                "source": "Gemini 1.5 Flash",
                "report": report_text,
                "status": telemetry.get("status", "SAFE"),
                "dlp_blocked": telemetry.get("dlp_blocked", False)
            }

    except Exception as e:
        report_text = generate_local_nlp_report(telemetry, worker_profile=worker_profile)
        return {
            "source": f"Local NLP Engine (API fallback: {str(e)[:40]}...)",
            "report": report_text,
            "status": telemetry.get("status", "SAFE"),
            "dlp_blocked": telemetry.get("dlp_blocked", False)
        }
