import streamlit as st
import json

# Configuración de página
st.set_page_config(
    page_title="Aplicativo de Diagnóstico Social",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Aplicativo de Diagnóstico Social, Pronóstico y Propuesta PAI/PPI")
st.markdown("""
Este aplicativo metodológico aplica los algoritmos de valoración del Trabajo Social para clasificar la situación social,
generar la narrativa diagnóstica por fases y estructurar un borrador de **Programa de Atención Individualizada (PAI/PPI)**.
""")

st.sidebar.header("👤 Datos de la Persona Atendida")
nombre = st.sidebar.text_input("Nombre / Iniciales", "Manuel G. P.")
edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, value=52)
motivo = st.sidebar.text_area("Motivo de consulta / Demanda inicial", "Solicitud de ayuda de emergencia y riesgo residencial por desahucio inminente.")
profesional = st.sidebar.text_input("Profesional de Referencia", "Trabajador/a Social de Atención Primaria")

st.header("1. Valoración de Necesidades Básicas e Indicadores")
st.caption("Selecciona el estado de cobertura para cada una de las 11 Necesidades Básicas:")

col1, col2 = st.columns(2)

necesidades_estado = {}

opciones = ["Adecuada", "Deficitaria", "Muy Deficitaria"]

with col1:
    st.subheader("Bloque Desarrollo Personal, Autonomía y Convivencia")
    necesidades_estado["Información"] = st.selectbox("1. Información", opciones, index=0)
    necesidades_estado["Habilidades Sociales"] = st.selectbox("2. Habilidades Sociales", opciones, index=1)
    necesidades_estado["Autonomía Física/Psíquica"] = st.selectbox("3. Autonomía Física/Psíquica", opciones, index=0)
    necesidades_estado["Relación Convivencial"] = st.selectbox("4. Relación Convivencial", opciones, index=1)
    necesidades_estado["Organización Unidad Convivencial"] = st.selectbox("5. Organización Unidad Convivencial", opciones, index=0)

with col2:
    st.subheader("Bloque Socio-Estructural y Entorno")
    necesidades_estado["Recursos Económicos"] = st.selectbox("6. Recursos Económicos", opciones, index=2)
    necesidades_estado["Trabajo/Ocupación"] = st.selectbox("7. Trabajo/Ocupación", opciones, index=2)
    necesidades_estado["Formación/Educación"] = st.selectbox("8. Formación/Educación", opciones, index=0)
    necesidades_estado["Vivienda"] = st.selectbox("9. Vivienda", opciones, index=2)
    necesidades_estado["Participación Social"] = st.selectbox("10. Participación Social", opciones, index=1)
    necesidades_estado["Aceptación Social"] = st.selectbox("11. Aceptación Social", opciones, index=0)

st.header("2. Evidencias, Factores de Riesgo y Protecciones")
col_e1, col_e2 = st.columns(2)

with col_e1:
    evidencias_obj = st.text_area(
        "Datos Objetivos y Evidencias (Documentos, observaciones)",
        "- Desahucio programado por impago de alquiler en 60 días.\n- Desempleo de larga duración (3 años).\n- Informe médico acreditativo de hipertensión no controlada."
    )
    info_referida = st.text_area(
        "Información Referida por el usuario (Percepción, vivencias)",
        "- Refiere elevada ansiedad y angustia por la pérdida de la vivienda.\n- Expresa sentimiento de soledad tras el reciente fallecimiento de sus progenitores."
    )

with col_e2:
    factores_proteccion = st.text_area(
        "Factores Protectores y Capacidades (Fortalezas, red, motivación)",
        "- Cualificación previa en oficio técnico (electricista).\n- Alta motivación para la inserción laboral.\n- Autonomía física e intelectual conservada para las AVD."
    )
    hipotesis_iniciales = st.text_area(
        "Hipótesis e Incertidumbres a contrastar",
        "- La pérdida de empleo actuó como desencadenante del aislamiento.\n- La contención residencial permitirá reactivar la búsqueda de empleo."
    )

def evaluar_tipologia(necesidades):
    deficitaria_count = sum(1 for v in necesidades.values() if v == "Deficitaria")
    muy_deficitaria_count = sum(1 for v in necesidades.values() if v == "Muy Deficitaria")
    
    bloque_personal = ["Habilidades Sociales", "Autonomía Física/Psíquica", "Relación Convivencial", "Organización Unidad Convivencial"]
    muy_def_personal = sum(1 for k in bloque_personal if necesidades[k] == "Muy Deficitaria")
    
    bloque_estructural = ["Recursos Económicos", "Trabajo/Ocupación", "Formación/Educación"]
    muy_def_estructural = sum(1 for k in bloque_estructural if necesidades[k] == "Muy Deficitaria")
    
    if muy_deficitaria_count >= 7:
        return "Marginación", "Afectación muy deficitaria grave y extendida (7 a 11 necesidades)."
    elif necesidades["Aceptación Social"] == "Muy Deficitaria":
        return "Desventaja Social", "Afectación muy deficitaria prioritaria en Aceptación Social (discriminación o exclusión de derechos)."
    elif muy_def_estructural >= 2:
        return "Exclusión Social", "Afectación muy deficitaria en el bloque socio-estructural (Ingresos, Empleo, Formación)."
    elif muy_def_personal >= 1 and muy_def_personal <= 4:
        return "Déficit de Larga Duración", "Afectación muy deficitaria en necesidades de desarrollo personal, autonomía o convivencia."
    elif (deficitaria_count + muy_deficitaria_count) <= 5:
        return "Déficit Coyuntural", "Afectación deficitaria moderada (1 a 5 necesidades) con conservación de capacidades y apoyos relacionales."
    else:
        return "Déficit Multidimensional Complejo", "Afectación mixta que requiere abordaje prioritario intensivo."

if st.button("⚙️ Generar Diagnóstico Social, Pronóstico y PAI", type="primary"):
    tipologia, explicacion = evaluar_tipologia(necesidades_estado)
    
    st.success(f"**Tipología Diagnóstica Evaluada:** {tipologia}")
    st.info(f"**Criterio Metodológico:** {explicacion}")
    
    st.markdown("---")
    st.header("📝 Informe Diagnóstico Narrado")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Fase 1: Síntesis Descriptiva", "Fase 2: Análisis Causal", "Fase 3: Conceptualización e Hipótesis", "Fase 4: Pronóstico y PAI"])
    
    with tab1:
        st.markdown(f"**SÍNTESIS DESCRIPTIVA DE LA SITUACIÓN:**")
        st.write(f"Se evalúa la situación social de **{nombre}** ({edad} años), atendido/a por {profesional} debido a: *{motivo}*.")
        st.write(f"Tras el análisis sistemático del sistema de necesidades básicas, la situación se clasifica técnicamente como **{tipologia}** ({explicacion}).")
        st.markdown("**Evidencias y Datos Objetivos Constatados:**")
        for ev in evidencias_obj.split("\n"):
            if ev.strip():
                st.write(f"- En la documentación/observación consta que {ev.strip().lstrip('-')}")
                
    with tab2:
        st.markdown("**ANÁLISIS CAUSAL Y MULTIDIMENSIONAL:**")
        st.write("Al analizar la interacción entre las distintas dimensiones, se identifica una clara interdependencia entre los factores de vulnerabilidad detectados:")
        for inf in info_referida.split("\n"):
            if inf.strip():
                st.write(f"- Durante las entrevistas, la persona refiere que {inf.strip().lstrip('-')}")
        st.write("Se observa cómo el compromiso en el área socio-estructural e inestabilidad residencial impacta negativamente en el estado emocional y convivencial.")

    with tab3:
        st.markdown("**CONCEPTUALIZACIÓN E HIPÓTESIS DE TRABAJO:**")
        st.write(f"Las principales áreas afectadas comprometen los ejes de Integridad, Inclusión y Autonomía personal.")
        st.markdown("**Hipótesis a contrastar en seguimiento técnico:**")
        for hip in hipotesis_iniciales.split("\n"):
            if hip.strip():
                st.write(f"- Se plantea como hipótesis que {hip.strip().lstrip('-')}")

    with tab4:
        st.markdown("**EVALUACIÓN PRONÓSTICA Y PROPUESTA PAI / PPI:**")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.error("**Evolución sin intervención:** De no intervenir, se prevé un agravamiento de la exclusión y riesgo inminente de marginación/desalojo.")
        with col_p2:
            st.success("**Potencial de cambio:** Existen capacidades de recuperación basadas en:")
            for prot in factores_proteccion.split("\n"):
                if prot.strip():
                    st.write(f"  * {prot.strip().lstrip('-')}")
        
        st.subheader("Propuesta de Plan Personalizado de Intervención (PAI/PPI) para Equipo Interdisciplinar")
        
        pai = {
            "Área Social (Trabajo Social)": [
                "Tramitación de ayuda de emergencia y solicitud de prestación económica de garantía.",
                "Gestión de alternativa residencial temporal y contención de desahucio.",
                "Acompañamiento en itinerario de inclusión social."
            ],
            "Área Sanitaria / Clínica (Medicina y Enfermería)": [
                "Derivación a Atención Primaria de Salud para control estricto de hipertensión.",
                "Revisión de hábitos saludables y adherencia al tratamiento farmacológico."
            ],
            "Área Psicológica (Psicología / Salud Mental)": [
                "Acompañamiento psicológico individual para la gestión del estrés y ansiedad.",
                "Afrontamiento del duelo familiar y fortalecimiento emocional."
            ],
            "Área Funcional / Ocupacional (Terapia Ocupacional / Empleo)": [
                "Estructuración de rutina diaria activa.",
                "Derivación al Servicio de Orientación Laboral (SOL) para actualización de perfil profesional."
            ]
        }
        
        for area, acciones in pai.items():
            with st.expander(f"📌 {area}", expanded=True):
                for acc in acciones:
                    st.write(f"• {acc}")

    # Exportar datos
    informe_json = json.dumps({
        "persona": nombre,
        "edad": edad,
        "tipologia": tipologia,
        "necesidades": necesidades_estado,
        "evidencias": evidencias_obj,
        "info_referida": info_referida,
        "factores_proteccion": factores_proteccion,
        "hipotesis": hipotesis_iniciales
    }, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="📥 Descargar Diagnóstico en JSON",
        data=informe_json,
        file_name=f"diagnostico_social_{nombre.replace(' ', '_')}.json",
        mime="application/json"
    )
