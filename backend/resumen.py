# ← Copia aquí las 
import pandas as pd
import re

def extract_situation(text):
    situations = re.findall(r'SITUACIÓN:\s*([^\n]+)', text, re.IGNORECASE)
    if not situations:
        situations = re.findall(r'(?:CASO|SITUACIÓN REPORTADA):\s*([^\n]+)', text, re.IGNORECASE)
    if not situations:
        paragraphs = text.split('\n')
        for p in paragraphs:
            if len(p.strip()) > 20:
                return p.strip()
    return situations[0].strip() if situations else "Por completar"

def extract_authorities(text):
    patterns = [
        r'AUTORIDADES:\s*([^\n]+)',
        r'COMPETENCIA POLICIAL:\s*([^\n]+)',
        r'COORDINACIÓN INSTITUCIONAL:\s*([^\n]+)',
        r'(?:ENTIDADES|INSTITUCIONES)(?:\s+COMPETENTES)?:\s*([^\n]+)'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].strip()
    return "Por completar"

def extract_legal_basis(text):
    patterns = [
        r'BASE LEGAL:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        r'NORMATIVA:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
        r'REFERENCIAS NORMATIVAS:\s*([^\n]+(?:\n(?!\n)[^\n]+)*)'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].strip()
    legal_refs = re.findall(r'(?:Ley|Decreto|Resolución|Artículo)\s+\d+[^.\n]+', text)
    if legal_refs:
        return '; '.join(legal_refs)
    return "Por completar"

def extract_procedure(text):
    section_patterns = [
        r'📋\s*PROCEDIMIENTO OPERATIVO:[\s\S]*?(?=(?:⚖️|🚨|🔍|📄|👮|🤝|$))',
        r'📋\s*PROCEDIMIENTO:[\s\S]*?(?=(?:⚖️|🚨|🔍|📄|👮|🤝|$))',
        r'PROCEDIMIENTO OPERATIVO:[\s\S]*?(?=(?:BASE LEGAL|PUNTOS CRÍTICOS|VERIFICACIÓN|DOCUMENTACIÓN|COMPETENCIA|COORDINACIÓN|$))',
        r'ACCIONES PASO A PASO:[\s\S]*?(?=(?:BASE LEGAL|PUNTOS CRÍTICOS|VERIFICACIÓN|DOCUMENTACIÓN|COMPETENCIA|COORDINACIÓN|$))',
    ]
    for pattern in section_patterns:
        section_match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if section_match:
            section_text = section_match.group(0)
            steps = re.findall(r'•\s*([^\n]+)', section_text)
            if not steps:
                steps = re.findall(r'\d+\.\s*([^\n]+)', section_text)
            if not steps:
                lines = [line.strip() for line in section_text.split('\n') if line.strip()]
                if lines and any(header in lines[0].lower() for header in ['procedimiento', 'acciones', 'pasos']):
                    lines = lines[1:]
                steps = [line for line in lines if not line.startswith(('⚖️', '🚨', '🔍', '📄', '👮', '🤝'))]
            if steps:
                summary_steps = []
                for i, step in enumerate(steps, 1):
                    clean_step = re.sub(r'^[•\-\d\.\s]+', '', step.strip())
                    parts = re.split(r'(?:[,:]|\sy\s)', clean_step, 1)
                    main_action = parts[0].strip()
                    details = parts[1].strip() if len(parts) > 1 else ""
                    formatted_step = f"{i}. {main_action} - {details}" if details else f"{i}. {main_action}"
                    if len(formatted_step) > 5:
                        summary_steps.append(formatted_step)
                if summary_steps:
                    return "\n".join(summary_steps[:5])
    full_text_steps = re.findall(r'(?:•|\d+\.)\s*([^\n]+)', text)
    if full_text_steps:
        summary_steps = []
        for i, step in enumerate(full_text_steps, 1):
            if any(word in step.lower() for word in ['verificar', 'documentar', 'coordinar', 'informar', 'inspeccionar']):
                parts = re.split(r'(?:[,:]|\sy\s)', step, 1)
                main_action = parts[0].strip()
                details = parts[1].strip() if len(parts) > 1 else ""
                formatted_step = f"{i}. {main_action} - {details}" if details else f"{i}. {main_action}"
                summary_steps.append(formatted_step)
                if len(summary_steps) == 5:
                    break
        if summary_steps:
            return "\n".join(summary_steps)
    return (
        "1. Verificar la situación - Documentar evidencia inicial\n"
        "2. Documentar hallazgos - Tomar fotografías y notas detalladas\n"
        "3. Coordinar con autoridades - Contactar entidades competentes"
    )

def create_executive_summary(response_text):
    situacion = extract_situation(response_text)
    procedimiento = extract_procedure(response_text)
    autoridades = extract_authorities(response_text)
    base_legal = extract_legal_basis(response_text)

    summary_data = {
        'Campo': [
            'Situación del Reporte',
            'Procedimiento',
            'Autoridades Competentes',
            'Base Legal'
        ],
        'Descripción': [
            situacion,
            procedimiento,
            autoridades,
            base_legal
        ]
    }

    df = pd.DataFrame(summary_data)
    return df

def get_legal_context(vector_store, query, k=5):
    """
    Obtiene el contexto legal relevante del vector store basado en la consulta.
    
    Args:
        vector_store: El almacén de vectores FAISS
        query: La consulta del usuario
        k: Número de documentos relevantes a recuperar
    
    Returns:
        Lista de documentos relevantes
    """
    docs = vector_store.similarity_search(query, k=k)
    return docs

def format_legal_context(context_docs):
    """
    Formatea los documentos de contexto legal en un formato legible.
    
    Args:
        context_docs: Lista de documentos relevantes
    
    Returns:
        String formateado con el contexto legal
    """
    formatted_context = []
    for i, doc in enumerate(context_docs, 1):
        formatted_context.append(f"Documento {i}:\n{doc.page_content}\n")
    return "\n".join(formatted_context)