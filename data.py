# Clinical knowledge base for the AI-Powered Healthcare Diagnosis Assistant

DISEASES_DB = [
    {
        "name": "Common Cold",
        "category": "Respiratory / Viral",
        "symptoms": ["runny nose", "sneezing", "sore throat", "mild cough", "congestion", "mild fatigue", "low fever"],
        "severity": "Low",
        "specialty": "General Practitioner / Family Medicine",
        "description": "A viral infection of the upper respiratory tract. Usually harmless, though it may not feel that way.",
        "tips": [
            "Get plenty of rest and stay well hydrated.",
            "Use warm saline gargles for sore throat relief.",
            "Over-the-counter decongestants or saline nasal sprays can help relieve congestion.",
            "Monitor symptoms; they should resolve in 7-10 days."
        ]
    },
    {
        "name": "Influenza (Flu)",
        "category": "Respiratory / Viral",
        "symptoms": ["high fever", "body aches", "chills", "dry cough", "severe fatigue", "headache", "sore throat", "sweating"],
        "severity": "Medium",
        "specialty": "General Practitioner / Family Medicine",
        "description": "A highly contagious viral infection of the respiratory passages causing fever, severe aching, and catarrh.",
        "tips": [
            "Prioritize strict bed rest and hydration.",
            "Use acetaminophen or ibuprofen to manage fever and body aches.",
            "Consider consulting a doctor within 48 hours of symptom onset for potential antiviral prescription (e.g., Tamiflu).",
            "Isolate to prevent spreading the virus to others."
        ]
    },
    {
        "name": "COVID-19",
        "category": "Respiratory / Viral",
        "symptoms": ["fever", "dry cough", "shortness of breath", "loss of taste", "loss of smell", "fatigue", "body aches", "sore throat", "headache"],
        "severity": "High",
        "specialty": "Pulmonologist / Infectious Disease",
        "description": "An infectious disease caused by the SARS-CoV-2 virus. Can range from mild respiratory symptoms to severe pneumonia.",
        "tips": [
            "Self-isolate immediately and wear a mask around others.",
            "Monitor blood oxygen levels with a pulse oximeter if available.",
            "Stay hydrated and use fever reducers if necessary.",
            "Seek immediate emergency care if you experience difficulty breathing, persistent chest pain, or bluish lips."
        ]
    },
    {
        "name": "Gastroenteritis (Stomach Flu)",
        "category": "Gastrointestinal",
        "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal cramps", "mild fever", "loss of appetite", "dehydration"],
        "severity": "Medium",
        "specialty": "Gastroenterologist / General Practitioner",
        "description": "Inflammation of the stomach and intestines, typically resulting from bacterial toxins or viral infection.",
        "tips": [
            "Focus on replacing lost fluids. Drink Oral Rehydration Salts (ORS), clear broths, or diluted sports drinks.",
            "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) when ready to eat.",
            "Avoid dairy, caffeine, alcohol, nicotine, and fatty or highly seasoned foods.",
            "Seek medical care if you cannot keep liquids down for 24 hours or show signs of severe dehydration."
        ]
    },
    {
        "name": "Migraine",
        "category": "Neurological",
        "symptoms": ["throbbing headache", "sensitivity to light", "sensitivity to sound", "nausea", "vomiting", "visual aura", "dizziness"],
        "severity": "Medium",
        "specialty": "Neurologist / Pain Specialist",
        "description": "A neurological condition characterized by intense, debilitating headaches, often accompanied by sensory disturbances.",
        "tips": [
            "Rest in a dark, quiet, cool room.",
            "Apply a cold compress or ice pack to your forehead or the back of your neck.",
            "Stay hydrated and avoid skipping meals, which can be a trigger.",
            "Keep a migraine diary to identify and avoid trigger factors."
        ]
    },
    {
        "name": "Allergic Rhinitis (Hay Fever)",
        "category": "Immunological / Allergy",
        "symptoms": ["sneezing", "itchy eyes", "runny nose", "nasal congestion", "watery eyes", "scratchy throat"],
        "severity": "Low",
        "specialty": "Allergist / Immunologist",
        "description": "An allergic response causing itchy, watery eyes, sneezing, and other similar symptoms, triggered by allergens like pollen or pet dander.",
        "tips": [
            "Identify and limit exposure to known environmental allergens.",
            "Over-the-counter antihistamines or nasal corticosteroid sprays can provide significant relief.",
            "Keep windows closed during high-pollen seasons and use air filters.",
            "Rinse nasal passages with saline solution to clear allergens."
        ]
    },
    {
        "name": "Pneumonia",
        "category": "Respiratory / Bacterial or Viral",
        "symptoms": ["productive cough", "coughing up mucus", "high fever", "shortness of breath", "chest pain", "chills", "fatigue", "sweating"],
        "severity": "High",
        "specialty": "Pulmonologist / Internal Medicine",
        "description": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus.",
        "tips": [
            "Consult a medical professional promptly for diagnostic chest X-rays or sputum tests.",
            "Take prescribed antibiotics or antivirals exactly as directed, finishing the entire course.",
            "Get plenty of rest and use a humidifier to help loosen chest congestion.",
            "Avoid coughing medicines unless recommended by a doctor, as coughing helps clear infection."
        ]
    },
    {
        "name": "Appendicitis",
        "category": "Gastrointestinal / Emergency",
        "symptoms": ["severe abdominal pain", "pain in lower right abdomen", "nausea", "vomiting", "loss of appetite", "fever", "abdominal swelling"],
        "severity": "High",
        "specialty": "General Surgeon / Emergency Medicine Specialist",
        "description": "A serious medical emergency where the appendix becomes inflamed and filled with pus. Requires urgent surgical removal.",
        "tips": [
            "Go to the nearest emergency room immediately.",
            "DO NOT eat, drink, or use laxatives/heating pads, as they can cause the appendix to rupture.",
            "Limit movement and keep still to minimize pain while seeking emergency care."
        ]
    },
    {
        "name": "Urinary Tract Infection (UTI)",
        "category": "Urological / Bacterial",
        "symptoms": ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "strong-smelling urine", "blood in urine"],
        "severity": "Medium",
        "specialty": "Urologist / General Practitioner",
        "description": "An infection in any part of the urinary system, most commonly the bladder or urethra. More common in women.",
        "tips": [
            "Drink plenty of water to help flush out the bacteria.",
            "Consult a doctor for a simple urine analysis and standard antibiotic course.",
            "Avoid bladder irritants like coffee, alcohol, and spicy foods until the infection clears.",
            "Do not delay urination when the urge arises."
        ]
    },
    {
        "name": "Asthma Exacerbation",
        "category": "Respiratory",
        "symptoms": ["shortness of breath", "wheezing", "chest tightness", "persistent cough", "difficulty speaking", "rapid breathing"],
        "severity": "High",
        "specialty": "Pulmonologist / Allergist",
        "description": "A sudden worsening of asthma symptoms caused by bronchospasm, swelling of airway linings, and increased mucus production.",
        "tips": [
            "Use your rescue inhaler (e.g., Albuterol) immediately according to your asthma action plan.",
            "Sit upright and try to remain calm; anxiety can worsen breathing difficulties.",
            "Remove yourself from any potential triggers (smoke, cold air, dust).",
            "Seek immediate emergency medical assistance if your rescue inhaler does not resolve symptoms or if you cannot speak in full sentences."
        ]
    },
    {
        "name": "Streptococcal Pharyngitis (Strep Throat)",
        "category": "Respiratory / Bacterial",
        "symptoms": ["severe sore throat", "painful swallowing", "fever", "swollen tonsils", "white patches on tonsils", "swollen lymph nodes", "headache"],
        "severity": "Medium",
        "specialty": "ENT Specialist / General Practitioner",
        "description": "A bacterial infection of the throat and tonsils caused by group A Streptococcus bacteria.",
        "tips": [
            "Consult a doctor for a rapid throat swab test.",
            "If bacterial strep is confirmed, complete the full course of prescribed antibiotics to prevent complications like rheumatic fever.",
            "Drink warm liquids, eat soft foods, and gargle with warm salt water.",
            "Replace your toothbrush after starting antibiotics to prevent reinfection."
        ]
    },
    {
        "name": "Gastroesophageal Reflux Disease (GERD)",
        "category": "Gastrointestinal",
        "symptoms": ["heartburn", "acid reflux", "chest pain", "difficulty swallowing", "regurgitation", "sour taste", "dry cough"],
        "severity": "Low",
        "specialty": "Gastroenterologist / Family Physician",
        "description": "A chronic digestive disease where stomach acid or bile flows back into the food pipe, irritating the lining.",
        "tips": [
            "Eat smaller, more frequent meals instead of large ones.",
            "Avoid lying down for at least 2-3 hours after eating.",
            "Identify and avoid trigger foods (fatty, fried, spicy foods, caffeine, chocolate, citrus).",
            "Elevate the head of your bed by 6 inches to prevent nighttime reflux."
        ]
    },
    {
        "name": "Hypertensive Crisis",
        "category": "Cardiovascular / Emergency",
        "symptoms": ["severe headache", "chest pain", "shortness of breath", "blurry vision", "dizziness", "anxiety", "nosebleeds"],
        "severity": "High",
        "specialty": "Cardiologist / Emergency Medicine Specialist",
        "description": "A severe increase in blood pressure that can lead to a stroke or organ damage. Blood pressure is typically 180/120 mmHg or higher.",
        "tips": [
            "If your blood pressure is 180/120 mmHg or higher and you experience these symptoms, call emergency services immediately.",
            "Sit quietly and avoid physical exertion or stress.",
            "Do not wait to see if your pressure drops on its own."
        ]
    },
    {
        "name": "Type 2 Diabetes (Hyperglycemia / New Onset)",
        "category": "Endocrine / Metabolic",
        "symptoms": ["excessive thirst", "frequent urination", "extreme hunger", "unexplained weight loss", "fatigue", "blurry vision", "slow-healing sores"],
        "severity": "Medium",
        "specialty": "Endocrinologist / Primary Care Physician",
        "description": "A chronic condition that affects the way the body processes blood sugar (glucose), resulting in high blood sugar levels.",
        "tips": [
            "Schedule a medical appointment for a blood glucose test and HbA1c screening.",
            "Adopt a balanced, low-glycemic diet rich in fiber, lean proteins, and vegetables.",
            "Engage in regular physical activity to help improve insulin sensitivity.",
            "Limit intake of sugary beverages and refined carbohydrates."
        ]
    },
    {
        "name": "Anemia",
        "category": "Hematological",
        "symptoms": ["chronic fatigue", "weakness", "pale skin", "cold hands", "cold feet", "dizziness", "shortness of breath", "chest pain"],
        "severity": "Low",
        "specialty": "Hematologist / Family Physician",
        "description": "A condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
        "tips": [
            "Request a complete blood count (CBC) from your doctor to confirm anemia type (e.g., iron-deficiency).",
            "Incorporate iron-rich foods (red meat, beans, lentils, dark leafy greens) into your diet.",
            "Consume vitamin C alongside iron-rich foods to enhance iron absorption.",
            "Discuss potential iron supplements with a physician, as excess iron can be harmful."
        ]
    }
]

ALL_SYMPTOMS = sorted(list(set(symptom for disease in DISEASES_DB for symptom in disease["symptoms"])))
