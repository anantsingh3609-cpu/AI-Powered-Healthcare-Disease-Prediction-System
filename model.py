import re
import os
from google import genai
from google.genai import types
from data import DISEASES_DB, ALL_SYMPTOMS

def extract_symptoms_from_text(text: str) -> list:
    """
    Extracts symptoms from a free-text description by checking for keyword overlaps.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    extracted = []
    
    for symptom in ALL_SYMPTOMS:
        # Simple substring matching
        if symptom in text_lower:
            extracted.append(symptom)
        else:
            # Let's check for word-by-word presence for multi-word symptoms
            words = symptom.split()
            if len(words) > 1:
                # If all words of the symptom are in the text
                if all(word in text_lower for word in words):
                    extracted.append(symptom)
                    
    return list(set(extracted))

def diagnose_symptoms(selected_symptoms: list, user_text: str = "") -> list:
    """
    Diagnoses potential conditions based on selected symptoms and free text.
    Returns a sorted list of matched conditions with metadata and match scores.
    """
    # Combine selected symptoms with extracted symptoms
    extracted = extract_symptoms_from_text(user_text)
    combined_symptoms = list(set(selected_symptoms + extracted))
    
    if not combined_symptoms:
        return []
        
    results = []
    
    for disease in DISEASES_DB:
        disease_symptoms = disease["symptoms"]
        
        # Calculate overlap
        intersection = set(combined_symptoms) & set(disease_symptoms)
        if not intersection:
            continue
            
        # Recall: What proportion of the disease's symptoms are present?
        recall = len(intersection) / len(disease_symptoms)
        
        # Precision: What proportion of the user's symptoms match this disease?
        precision = len(intersection) / len(combined_symptoms)
        
        # Weighted score (favouring recall for healthcare since we want to capture diseases
        # even if the patient has additional unrelated symptoms)
        score = (0.7 * recall) + (0.3 * precision)
        
        results.append({
            "name": disease["name"],
            "category": disease["category"],
            "score": round(score * 100, 1),
            "matched_symptoms": list(intersection),
            "missing_symptoms": list(set(disease_symptoms) - intersection),
            "severity": disease["severity"],
            "specialty": disease["specialty"],
            "description": disease["description"],
            "tips": disease["tips"]
        })
        
    # Sort results by score in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

def get_gemini_client(api_key: str = None) -> genai.Client:
    """
    Initializes and returns a Gemini client.
    First checks the argument, then checks environment variables.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        return None

def generate_ai_summary(patient_profile: dict, symptoms: list, diagnosis_results: list, api_key: str = None) -> str:
    """
    Generates a professional AI summary explaining the diagnosis using Gemini.
    If no client/key is available, falls back to a locally generated report.
    """
    client = get_gemini_client(api_key)
    
    # Format local diagnosis info for context
    top_matches_text = ""
    for idx, match in enumerate(diagnosis_results[:3]):
        top_matches_text += f"{idx+1}. {match['name']} (Match Score: {match['score']}%, Severity: {match['severity']}, Specialist: {match['specialty']})\n"
        top_matches_text += f"   Reason: Matches symptoms: {', '.join(match['matched_symptoms'])}\n\n"
        
    if not client:
        # Fallback local report
        if not diagnosis_results:
            return "No matching conditions found based on current symptoms. Please try adjusting your symptoms or input."
            
        primary = diagnosis_results[0]
        fallback_msg = f"### [Local AI Model] Primary Diagnostic Match: **{primary['name']}**\n\n"
        fallback_msg += f"**Category**: {primary['category']} | **Urgency Level**: {primary['severity']}\n\n"
        fallback_msg += f"**Description**: {primary['description']}\n\n"
        fallback_msg += f"**Symptom Breakdown**:\n"
        fallback_msg += f"- Matched: {', '.join(primary['matched_symptoms'])}\n"
        if primary['missing_symptoms']:
            fallback_msg += f"- Other Common Symptoms: {', '.join(primary['missing_symptoms'])}\n"
        fallback_msg += f"\n**Clinical Guidance**:\n"
        fallback_msg += f"- Recommended Department: **{primary['specialty']}**\n"
        fallback_msg += f"- Initial Care Measures:\n"
        for tip in primary['tips']:
            fallback_msg += f"  - {tip}\n"
        fallback_msg += "\n\n> *Note: Gemini API key was not detected. Set your GEMINI_API_KEY in the sidebar to enable advanced, conversational clinical summaries and patient history analysis.*"
        return fallback_msg

    # Prepare prompt for Gemini
    prompt = f"""
    You are a professional clinical assistant. Review the following patient case and local algorithm results:
    
    [PATIENT PROFILE]
    - Age: {patient_profile.get('age', 'N/A')}
    - Biological Sex: {patient_profile.get('gender', 'N/A')}
    - Chronic / Existing Conditions: {patient_profile.get('conditions', 'None reported')}
    
    [SYMPTOMS REPORTED]
    {', '.join(symptoms)}
    
    [TOP ALGORITHMIC MATCHES]
    {top_matches_text}
    
    Please write a comprehensive, professional, and empathetic clinical assessment.
    Your output should be formatted in Markdown and include the following sections:
    1. **Overview & Rationale**: Analyze the reported symptoms in relation to the top matches. Explain how the patient's profile influences this.
    2. **Clinical Urgency / Triage**: Explicitly state the urgency level (Low, Medium, High, or Immediate Care).
    3. **Actionable Next Steps**: What tests or doctor specialties they should seek.
    4. **Wellness & Supportive Care**: Practical, safe home-care tips (nutrition, rest, hydration, what to avoid).
    5. **Red Flags**: Specific warning signs that mean the patient must go to the emergency room immediately.
    
    IMPORTANT: Start the assessment with a brief, clear disclaimer in an italicized quote block that this is an AI assistant, not a doctor, and they should seek professional medical advice.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a clinical decision support system. Maintain a professional, empathetic, and objective tone. Always highlight safety and provide medical disclaimers.",
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        return f"Error generating Gemini summary: {str(e)}\n\n(Fallback to local matches above)"

def generate_chat_response(user_message: str, chat_history: list, api_key: str = None) -> str:
    """
    Generates a conversational response for the health assistant chatbot.
    """
    client = get_gemini_client(api_key)
    
    if not client:
        return "I'm a local health chatbot. To talk with me, please enter a valid Gemini API key in the settings tab of the sidebar. In the meantime, I can tell you that for any medical concerns, it's best to consult a licensed healthcare practitioner."

    # Convert standard list history to Gemini's chat format
    contents = []
    for msg in chat_history:
        contents.append(
            types.Content(
                role="user" if msg["role"] == "user" else "model",
                parts=[types.Part.from_text(text=msg["content"])]
            )
        )
    # Add the final user message
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        )
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a helpful, professional, and empathetic AI Health Assistant. "
                    "You provide general wellness advice, clarify medical definitions, explain common symptoms, and offer lifestyle tips. "
                    "CRITICAL RULES:\n"
                    "1. Never diagnose specific conditions in chat unless analyzing symptoms explicitly passed from the checker.\n"
                    "2. Always emphasize that your advice is for informational purposes and cannot replace professional medical consult.\n"
                    "3. If symptoms sound severe (e.g. chest pain, breathing difficulty, severe bleeding, sudden numbness), instruct the user to seek emergency care immediately.\n"
                    "4. Keep your responses concise, structured, and easy to read."
                ),
                temperature=0.5
            )
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"
