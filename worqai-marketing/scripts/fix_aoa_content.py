import re
from pathlib import Path

base = Path('production/Carousels to remake/priority 1/batch 3/reframed/Approved/Approved of approved')
files = list(base.glob('*.html'))

fixes_log = []

for f in files:
    content = f.read_text(encoding='utf-8')
    original = content
    file_fixes = []
    
    # Extract topic from title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else 'CV'
    topic = re.sub(r'worqai\s*[·\-]\s*', '', title).strip()
    if not topic or topic == 'worqai':
        topic = 'CV'
    
    # Fix 1: Generic consequence -> topic-specific
    old_conseq = 'Lo que vos ves ordenado puede llegar desordenado cuando el ATS extrae texto.'
    
    if old_conseq in content:
        topic_lower = topic.lower()
        if 'cv' in topic_lower or 'resumen' in topic_lower or 'plantilla' in topic_lower:
            new_conseq = 'Si el formato no es compatible, el ATS extrae texto desordenado y tu CV pierde sentido.'
        elif 'linkedin' in topic_lower or 'perfil' in topic_lower:
            new_conseq = 'Si tu perfil no tiene las keywords que el ATS busca, no aparecés en las búsquedas de reclutadores.'
        elif 'foto' in topic_lower or 'imagen' in topic_lower:
            new_conseq = 'Una foto mal posicionada puede romper el formato y hacer que el ATS no lea tu CV correctamente.'
        elif 'educaci' in topic_lower or 'grado' in topic_lower or 'estudio' in topic_lower:
            new_conseq = 'Si tu educación está en formato que el ATS no lee, los filtros de grado la ignoran por completo.'
        elif 'idioma' in topic_lower or 'inglés' in topic_lower or 'español' in topic_lower:
            new_conseq = 'Si tus idiomas no están en el formato que el ATS busca, los filtros los ignoran.'
        elif 'venta' in topic_lower or 'sales' in topic_lower:
            new_conseq = 'Si tus números de ventas quedan en gráficos, el ATS no los cuenta como experiencia.'
        elif 'admin' in topic_lower or 'oficina' in topic_lower:
            new_conseq = 'Si tus tareas administrativas quedan en tablas, el ATS las salta y no cuenta tu experiencia.'
        elif 'tech' in topic_lower or 'tecnología' in topic_lower or 'desarrollo' in topic_lower:
            new_conseq = 'Si tus skills técnicos quedan en iconos o badges, el ATS no los registra como habilidades.'
        elif 'marketing' in topic_lower:
            new_conseq = 'Si tus métricas de marketing quedan en gráficos, el ATS no las cuenta como logros.'
        elif 'bootcamp' in topic_lower or 'certificado' in topic_lower:
            new_conseq = 'Si el ATS no reconoce el formato de tu formación, descarta tu experiencia como irrelevante.'
        elif 'pdf' in topic_lower or 'archivo' in topic_lower:
            new_conseq = 'Si el PDF tiene formato incompatible, el ATS no lee el contenido y tu CV queda vacío.'
        elif 'portafolio' in topic_lower or 'portfolio' in topic_lower:
            new_conseq = 'Si el portafolio no tiene contexto, el ATS no entiende qué habilidades demuestra.'
        elif 'cambio' in topic_lower or 'carrera' in topic_lower:
            new_conseq = 'Si el ATS no ve experiencia directa, descarta tu CV sin leer tus habilidades transferibles.'
        elif 'rechazo' in topic_lower:
            new_conseq = 'Después de un rechazo, si no ajustás el CV, el ATS te descarta de nuevo por las mismas razones.'
        elif 'remoto' in topic_lower or 'remote' in topic_lower:
            new_conseq = 'Si tu experiencia remota queda escondida en tablas, el ATS no la encuentra como experiencia.'
        elif 'data' in topic_lower or 'datos' in topic_lower:
            new_conseq = 'Si tus proyectos de data quedan en gráficos, el ATS no los cuenta como experiencia técnica.'
        elif 'junior' in topic_lower or 'primer' in topic_lower:
            new_conseq = 'Si tu CV no muestra las skills que el aviso pide, el ATS te descarta antes de que un humano te vea.'
        elif 'senior' in topic_lower:
            new_conseq = 'Si tu CV tiene demasiado contenido, el ATS no encuentra tu experiencia senior relevante.'
        elif 'aplicaci' in topic_lower or 'postul' in topic_lower:
            new_conseq = 'Si tu aplicación no pasa el filtro del ATS, nunca llega a un reclutador humano.'
        elif 'keyword' in topic_lower or 'palabra' in topic_lower:
            new_conseq = 'Si tu CV no usa las palabras que el aviso pide, el ATS te descarta automáticamente.'
        elif 'nombre' in topic_lower or 'archivo' in topic_lower:
            new_conseq = 'Si el nombre del archivo no tiene sentido, el ATS puede descartarlo antes de abrirlo.'
        elif 'header' in topic_lower or 'encabezado' in topic_lower:
            new_conseq = 'Si el header no tiene las keywords correctas, el ATS no identifica tu perfil adecuadamente.'
        elif 'skills' in topic_lower or 'habilidad' in topic_lower:
            new_conseq = 'Si tus skills quedan en iconos o gráficos, el ATS no los registra como habilidades válidas.'
        elif 'extracción' in topic_lower or 'extrae' in topic_lower:
            new_conseq = 'Si el ATS no puede extraer el texto correctamente, tu CV queda vacío en el sistema.'
        elif 'filtro' in topic_lower:
            new_conseq = 'Si tu CV no pasa el filtro automático, nunca llega a un reclutador humano.'
        elif 'página' in topic_lower:
            new_conseq = 'Si el CV tiene demasiadas páginas, el ATS no escanea todo el contenido correctamente.'
        elif 'biling' in topic_lower:
            new_conseq = 'Si el ATS no detecta ambos idiomas correctamente, los filtros de idioma te descartan.'
        else:
            new_conseq = 'Si el formato no es compatible, el ATS extrae texto desordenado y tu CV pierde sentido.'
        
        content = content.replace(old_conseq, new_conseq)
        file_fixes.append('generic consequence -> topic-specific (' + topic + ')')
    
    # Fix 2: Check for any remaining 'ajustar' issues
    matches = re.findall(r'Despu[eé]s de ajustar (.+?) con WorqAI', content)
    for topic_ajustar in matches:
        topic_clean = topic_ajustar.strip()
        if 'CV' not in topic_clean and 'página' not in topic_clean and 'formato' not in topic_clean:
            new_phrase = 'Después de optimizar el CV de ' + topic_clean + ' con WorqAI'
            old_phrase = 'Después de ajustar ' + topic_clean + ' con WorqAI'
            if old_phrase in content:
                content = content.replace(old_phrase, new_phrase)
                file_fixes.append('ajustar "' + topic_clean + '" -> optimizar el CV de "' + topic_clean + '"')
        else:
            new_phrase = 'Después de optimizar ' + topic_clean + ' con WorqAI'
            old_phrase = 'Después de ajustar ' + topic_clean + ' con WorqAI'
            if old_phrase in content:
                content = content.replace(old_phrase, new_phrase)
                file_fixes.append('ajustar "' + topic_clean + '" -> optimizar "' + topic_clean + '"')
    
    # Fix 3: Backwards logic
    old_conseq2 = 'El aviso ya trae las palabras que el sistema quiere encontrar.'
    new_conseq2 = 'Si tu CV no usa esas palabras, el ATS te descarta antes de que un humano te vea.'
    if old_conseq2 in content:
        content = content.replace(old_conseq2, new_conseq2)
        file_fixes.append('consecuencia: positive -> negative (backwards logic)')
    
    if content != original:
        f.write_text(content, encoding='utf-8')
    
    if file_fixes:
        fixes_log.append(f.name + ': ' + topic)
        for fix in file_fixes:
            fixes_log.append('  - ' + fix)

print('=== APPROVED OF APPROVED: CONTENT FIXES ===')
print('Files scanned: ' + str(len(files)))
files_changed = len([x for x in fixes_log if not x.startswith('  -')])
print('Files with fixes: ' + str(files_changed))
print()
for line in fixes_log:
    print(line)

# Save log
log_path = base / 'CONTENT_FIX_LOG_AOA.txt'
log_path.write_text('\n'.join(fixes_log), encoding='utf-8')
print('\nLog saved to: ' + str(log_path))
