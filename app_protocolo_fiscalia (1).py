import streamlit as st
import datetime
import json

# Configuración de la página
st.set_page_config(
    page_title="Protocolo 10 Días - Fiscalía / Protección de Menores",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual adaptado a móviles
st.markdown("""
    <style>
    .stApp {
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #0d6efd;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .alert-green { background-color: #d1e7dd; color: #0f5132; padding: 10px; border-radius: 6px; }
    .alert-yellow { background-color: #fff3cd; color: #664d03; padding: 10px; border-radius: 6px; }
    .alert-red { background-color: #f8d7da; color: #842029; padding: 10px; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

# Valores por defecto del expediente
DEFAULT_EXPEDIENTE = {
    "num_expediente": "FIS-2026/0489",
    "organo": "Fiscalía de Menores",
    "fecha_recepcion": datetime.date.today(),
    "nombre_menor": "",
    "fecha_nacimiento": None,
    "tutores_legales": "",
    "domicilio": "",
    # Pasos del protocolo
    "p1_coord_24h": False,
    "p2_ts_previo": False,
    "p2_edu_contacto_colegio": False,
    "p2_edu_informe_legal": False,
    "p2_psi_contacto_familia": False,
    "p2_psi_cita_fecha": None,
    "p3_entrevista_familiar": False,
    "p3_visita_domiciliaria": False,
    "val_ts_entorno": "",
    "val_edu_escolar": "",
    "val_psi_emocional": "",
    "conclusiones_equipo": "",
    "diagnostico_situacion": "",
    "pronostico_evolutivo": "",
    "nivel_riesgo": "Riesgo Moderado",
    "redactor_designado": "Trabajo Social (TS)",
    "p7_revision_equipo": False,
    "p8_vobo_direccion": False,
    "p8_enviado_oficial": False
}

# Inicialización de session_state para datos del expediente
if "expediente" not in st.session_state:
    st.session_state.expediente = DEFAULT_EXPEDIENTE.copy()

# Función para cargar caso de prueba
def cargar_datos_prueba():
    st.session_state.expediente["num_expediente"] = "FIS-2026/0892"
    st.session_state.expediente["organo"] = "Fiscalía de Menores"
    st.session_state.expediente["fecha_recepcion"] = datetime.date.today() - datetime.timedelta(days=2)
    st.session_state.expediente["nombre_menor"] = "Lucía M. R."
    st.session_state.expediente["fecha_nacimiento"] = datetime.date(2012, 5, 14)
    st.session_state.expediente["tutores_legales"] = "Carmen R. G. (Madre) y Pedro M. V. (Padre)"
    st.session_state.expediente["domicilio"] = "Calle Mayor 14, 2ºB"
    st.session_state.expediente["p1_coord_24h"] = True
    st.session_state.expediente["p2_ts_previo"] = True
    st.session_state.expediente["p2_edu_contacto_colegio"] = True
    st.session_state.expediente["p2_edu_informe_legal"] = True
    st.session_state.expediente["p2_psi_contacto_familia"] = True
    st.session_state.expediente["p2_psi_cita_fecha"] = datetime.date.today() + datetime.timedelta(days=1)
    st.session_state.expediente["p3_entrevista_familiar"] = True
    st.session_state.expediente["p3_visita_domiciliaria"] = True
    st.session_state.expediente["val_ts_entorno"] = "Vivienda en condiciones adecuadas de habitabilidad. Red social de apoyo limitada tras traslado reciente de domicilio. Ingresos estables pero elevada conflictividad entre progenitores."
    st.session_state.expediente["val_edu_escolar"] = "Faltas injustificadas puntuales (12% en el último mes). Adecuada integración con su grupo de iguales, aunque se observa bajada en el rendimiento académico."
    st.session_state.expediente["val_psi_emocional"] = "La menor expresa sintomatología ansiosa vinculada al clima de discusión en el hogar. Mantiene buen vínculo afectivo con ambos progenitores pero demanda neutralidad."
    st.session_state.expediente["conclusiones_equipo"] = "Situación de riesgo social moderado ligada a la alta conflictividad parental en contexto de separación no regulada. La menor no presenta indicadores de desprotección grave."
    st.session_state.expediente["diagnostico_situacion"] = "Riesgo sociofamiliar moderado por exposición a conflicto interparental desestructurante y ausentismo escolar incipiente."
    st.session_state.expediente["pronostico_evolutivo"] = "Favorable si se formaliza mediación familiar y seguimiento psicopedagógico. Reservado si se mantiene la tensión sin intervención."
    st.session_state.expediente["nivel_riesgo"] = "Riesgo Moderado"
    st.session_state.expediente["redactor_designado"] = "Educación Social (EDU)"
    st.session_state.expediente["p7_revision_equipo"] = True
    st.session_state.expediente["p8_vobo_direccion"] = False
    st.session_state.expediente["p8_enviado_oficial"] = False

# Sidebar: Control y Estado del Expediente
with st.sidebar:
    st.title("⚖️ Control de Plazos")
    st.subheader("Procedimiento Urgente (10 Días)")
    
    fecha_rec = st.session_state.expediente["fecha_recepcion"]
    if isinstance(fecha_rec, str):
        try:
            fecha_rec = datetime.datetime.strptime(fecha_rec, "%Y-%m-%d").date()
        except ValueError:
            fecha_rec = datetime.date.today()

    fecha_limite = fecha_rec + datetime.timedelta(days=10)
    dias_transcurridos = (datetime.date.today() - fecha_rec).days
    dias_restantes = 10 - dias_transcurridos

    st.metric("Fecha de Recepción", fecha_rec.strftime("%d/%m/%Y"))
    st.metric("Fecha Límite Remisión", fecha_limite.strftime("%d/%m/%Y"))

    if dias_restantes > 5:
        st.markdown(f'<div class="alert-green"><b>🟢 Plazo Holgado:</b> Quedan {dias_restantes} días.</div>', unsafe_allow_html=True)
    elif 2 <= dias_restantes <= 5:
        st.markdown(f'<div class="alert-yellow"><b>🟡 Plazo Medio:</b> Quedan {dias_restantes} días (Fase de Valoración/Redacción).</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-red"><b>🔴 Urgencia Extrema:</b> Quedan {dias_restantes} días. Se requiere envío inminente.</div>', unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Cargar Caso de Prueba", use_container_width=True):
        cargar_datos_prueba()
        st.rerun()

    if st.button("🗑️ Limpiar / Nuevo Expediente", use_container_width=True):
        st.session_state.expediente = DEFAULT_EXPEDIENTE.copy()
        st.session_state.expediente["fecha_recepcion"] = datetime.date.today()
        st.rerun()

# Encabezado Principal
st.title("⚖️ Protocolo de Actuación Rápida (10 Días)")
st.caption("Peticiones de la Fiscalía de Menores y Servicio de Protección de Menores — Gestión Interdisciplinar (TS, EDU, PSI)")

# Barra de Progreso del Protocolo (8 Pasos)
pasos_completados = sum([
    st.session_state.expediente["p1_coord_24h"],
    st.session_state.expediente["p2_ts_previo"] and st.session_state.expediente["p2_edu_contacto_colegio"] and st.session_state.expediente["p2_psi_contacto_familia"],
    st.session_state.expediente["p3_entrevista_familiar"] and st.session_state.expediente["p3_visita_domiciliaria"],
    bool(st.session_state.expediente["val_ts_entorno"] and st.session_state.expediente["val_edu_escolar"] and st.session_state.expediente["val_psi_emocional"]),
    bool(st.session_state.expediente["conclusiones_equipo"]),
    bool(st.session_state.expediente["redactor_designado"]),
    st.session_state.expediente["p7_revision_equipo"],
    st.session_state.expediente["p8_vobo_direccion"] and st.session_state.expediente["p8_enviado_oficial"]
])

porcentaje = int((pasos_completados / 8) * 100)
st.progress(porcentaje / 100, text=f"Progreso del Expediente: {pasos_completados}/8 Pasos Completados ({porcentaje}%)")

# Estructura en Pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "1️⃣ Recepción y Filtro (Días 1-2)",
    "2️⃣ Investigación y Campo (Días 2-4)",
    "3️⃣ Sesión de Equipo y Diagnóstico (Días 5-6)",
    "4️⃣ Informe Final y Registro (Días 7-10)"
])

# ==================== TAB 1: RECEPCIÓN Y FILTRO ====================
with tab1:
    st.header("1. Datos del Oficio y Coordinación Inicial (Primeras 24-48 Horas)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.expediente["num_expediente"] = st.text_input("Nº de Expediente / Oficio:", st.session_state.expediente["num_expediente"])
        
        opciones_organo = ["Fiscalía de Menores", "Servicio de Protección de Menores", "Juzgado de Familia"]
        val_organo = st.session_state.expediente.get("organo", "Fiscalía de Menores")
        idx_organo = opciones_organo.index(val_organo) if val_organo in opciones_organo else 0
        
        st.session_state.expediente["organo"] = st.selectbox("Órgano Solicitante:", opciones_organo, index=idx_organo)
        st.session_state.expediente["nombre_menor"] = st.text_input("Nombre y Apellidos del Menor:", st.session_state.expediente["nombre_menor"])
    with col2:
        st.session_state.expediente["fecha_recepcion"] = st.date_input("Fecha de Entrada/Recepción:", st.session_state.expediente["fecha_recepcion"])
        st.session_state.expediente["tutores_legales"] = st.text_input("Padres / Tutores Legales:", st.session_state.expediente["tutores_legales"])
        st.session_state.expediente["domicilio"] = st.text_input("Domicilio de Residencia:", st.session_state.expediente["domicilio"])

    st.subheader("Paso 1: Coordinación Informativa de Entrada (Primeras 24 Horas)")
    st.session_state.expediente["p1_coord_24h"] = st.checkbox(
        "✅ **Reunión/Puesta en común inicial de 24h realizada** (Trabajo Social, Educación Social y Psicología)",
        value=st.session_state.expediente["p1_coord_24h"]
    )

    st.subheader("Paso 2: Actuaciones Preparatorias Sectoriales")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("##### 📁 Trabajo Social (TS)")
        st.session_state.expediente["p2_ts_previo"] = st.checkbox(
            "Recopilación de información previa / expediente histórico",
            value=st.session_state.expediente["p2_ts_previo"]
        )

    with c2:
        st.markdown("##### 🎓 Educación Social (EDU)")
        st.session_state.expediente["p2_edu_contacto_colegio"] = st.checkbox(
            "Contacto telefónico inicial con centro educativo",
            value=st.session_state.expediente["p2_edu_contacto_colegio"]
        )
        st.session_state.expediente["p2_edu_informe_legal"] = st.checkbox(
            "Solicitud formal de informe escolar por vía legal",
            value=st.session_state.expediente["p2_edu_informe_legal"]
        )

    with c3:
        st.markdown("##### 🧠 Psicología (PSI)")
        st.session_state.expediente["p2_psi_contacto_familia"] = st.checkbox(
            "Contacto telefónico con la familia",
            value=st.session_state.expediente["p2_psi_contacto_familia"]
        )
        fecha_cita_def = st.session_state.expediente["p2_psi_cita_fecha"] or (datetime.date.today() + datetime.timedelta(days=1))
        st.session_state.expediente["p2_psi_cita_fecha"] = st.date_input("Fecha cita entrevista (máx 24-48h):", fecha_cita_def)

# ==================== TAB 2: INVESTIGACIÓN Y CAMPO ====================
with tab2:
    st.header("2. Trabajo de Campo y Valoraciones Rápidas Urgentes")
    st.info("💡 **Nota metodológica:** Las valoraciones para Fiscalía en plazo de 10 días deben ser concisas, objetivas y centradas en la situación actual sin sobrecargar de diagnósticos profundos innecesarios.")

    st.subheader("Paso 3: Ejecución de Entrevistas y Visitas")
    col_a, col_b = st.columns(2)
    with col_a:
        st.session_state.expediente["p3_entrevista_familiar"] = st.checkbox(
            "✅ **Entrevista familiar conjunta realizada** (EDU + PSI)",
            value=st.session_state.expediente["p3_entrevista_familiar"]
        )
    with col_b:
        st.session_state.expediente["p3_visita_domiciliaria"] = st.checkbox(
            "✅ **Visita domiciliaria realizada** (TS)",
            value=st.session_state.expediente["p3_visita_domiciliaria"]
        )

    st.subheader("Paso 4: Valoraciones Urgentes por Áreas Profesionales")
    
    st.markdown("#### 🟢 Valoración de Entorno Social y Habitabilidad (Trabajo Social)")
    st.session_state.expediente["val_ts_entorno"] = st.text_area(
        "Indicar condiciones del domicilio, dinámica socioeconómica y red de apoyo informal:",
        value=st.session_state.expediente["val_ts_entorno"],
        height=100
    )

    st.markdown("#### 🔵 Valoración del Ámbito Escolar y Adaptativo (Educación Social)")
    st.session_state.expediente["val_edu_escolar"] = st.text_area(
        "Indicar nivel de escolarización, asistencia, integración con iguales y conducta:",
        value=st.session_state.expediente["val_edu_escolar"],
        height=100
    )

    st.markdown("#### 🟣 Valoración Emocional y Dinámica Familiar (Psicología)")
    st.session_state.expediente["val_psi_emocional"] = st.text_area(
        "Indicar estado emocional del menor, estilo parental y pautas de crianza observadas:",
        value=st.session_state.expediente["val_psi_emocional"],
        height=100
    )

# ==================== TAB 3: SESIÓN DE EQUIPO Y DIAGNÓSTICO ====================
with tab3:
    st.header("3. Deliberación Interdisciplinar y Asignación de Redacción")

    st.subheader("Paso 5: Reunión Técnica del Equipo (TS + EDU + PSI)")
    
    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        st.session_state.expediente["conclusiones_equipo"] = st.text_area(
            "Conclusiones unificadas de la deliberación técnica:",
            value=st.session_state.expediente["conclusiones_equipo"],
            height=110
        )
        st.session_state.expediente["diagnostico_situacion"] = st.text_area(
            "Diagnóstico de la situación (Riesgo / Desprotección / Normalización):",
            value=st.session_state.expediente["diagnostico_situacion"],
            height=80
        )
        st.session_state.expediente["pronostico_evolutivo"] = st.text_area(
            "Pronóstico y propuesta de medidas/intervención recomendadas:",
            value=st.session_state.expediente["pronostico_evolutivo"],
            height=80
        )
    
    with col_r2:
        opciones_riesgo = ["Sin Riesgo Apreciable", "Riesgo Leve", "Riesgo Moderado", "Riesgo Grave / Desprotección"]
        val_riesgo = st.session_state.expediente.get("nivel_riesgo", "Riesgo Moderado")
        idx_riesgo = opciones_riesgo.index(val_riesgo) if val_riesgo in opciones_riesgo else 2

        st.session_state.expediente["nivel_riesgo"] = st.selectbox(
            "Nivel de Riesgo Evaluado:",
            opciones_riesgo,
            index=idx_riesgo
        )

        st.subheader("Paso 6: Asignación de Redacción")
        
        opciones_redactor = ["Trabajo Social (TS)", "Educación Social (EDU)", "Psicología (PSI)"]
        val_redactor = st.session_state.expediente.get("redactor_designado", "Trabajo Social (TS)")
        idx_redactor = opciones_redactor.index(val_redactor) if val_redactor in opciones_redactor else 0

        st.session_state.expediente["redactor_designado"] = st.radio(
            "Profesional designado/a para ensamblar el informe unificado:",
            opciones_redactor,
            index=idx_redactor
        )

# ==================== TAB 4: INFORME FINAL Y REGISTRO ====================
with tab4:
    st.header("4. Revisión Técnica, VºBº y Remisión Oficial")

    st.subheader("Paso 7 y 8: Control de Calidad y Registro de Salida")
    c_rev1, c_rev2, c_rev3 = st.columns(3)
    
    with c_rev1:
        st.session_state.expediente["p7_revision_equipo"] = st.checkbox(
            "✅ **Paso 7:** Revisión técnica por el equipo (TS, EDU, PSI) realizada y aprobada",
            value=st.session_state.expediente["p7_revision_equipo"]
        )

    with c_rev2:
        st.session_state.expediente["p8_vobo_direccion"] = st.checkbox(
            "✅ **Paso 8:** VºBº final de Dirección concedido",
            value=st.session_state.expediente["p8_vobo_direccion"]
        )

    with c_rev3:
        st.session_state.expediente["p8_enviado_oficial"] = st.checkbox(
            "📨 **Paso 8:** Registro de Salida y remisión efectuada a Fiscalía/Protección",
            value=st.session_state.expediente["p8_enviado_oficial"]
        )

    st.divider()

    # Generación del Texto del Informe Unificado
    nombre_m = st.session_state.expediente["nombre_menor"] or "[Nombre del Menor]"
    exp_num = st.session_state.expediente["num_expediente"] or "[Nº Expediente]"
    org = st.session_state.expediente["organo"]
    
    informe_texto = f"""
================================================================================
INFORME SOCIAL Y PSICOEDUCATIVO PARA {org.upper()}
================================================================================
EXPEDIENTE / OFICIO Nº: {exp_num}
ÓRGANO SOLICITANTE: {org}
FECHA DE SOLICITUD / ENTRADA: {st.session_state.expediente['fecha_recepcion']}
FECHA DE EMISIÓN: {datetime.date.today().strftime('%d/%m/%Y')}

1. DATOS DE IDENTIFICACIÓN
--------------------------------------------------------------------------------
Nombre del/la Menor: {nombre_m}
Fecha de Nacimiento: {st.session_state.expediente['fecha_nacimiento'] or 'No consta'}
Tutores Legales: {st.session_state.expediente['tutores_legales'] or 'No consta'}
Domicilio: {st.session_state.expediente['domicilio'] or 'No consta'}

2. VALORACIÓN SECTORIAL INTERDISCIPLINAR
--------------------------------------------------------------------------------
A) VALORACIÓN DEL ENTORNO SOCIOFAMILIAR (Trabajo Social):
{st.session_state.expediente['val_ts_entorno'] or 'Pendiente de cumplimentar.'}

B) VALORACIÓN ESCOLAR Y ADAPTATIVA (Educación Social):
{st.session_state.expediente['val_edu_escolar'] or 'Pendiente de cumplimentar.'}

C) VALORACIÓN EMOCIONAL Y DE DINÁMICA FAMILIAR (Psicología):
{st.session_state.expediente['val_psi_emocional'] or 'Pendiente de cumplimentar.'}

3. DIAGNÓSTICO Y CONCLUSIONES DE EQUIPO
--------------------------------------------------------------------------------
NIVEL DE RIESGO ESTIMADO: {st.session_state.expediente['nivel_riesgo'].upper()}

SÍNTESIS DIAGNÓSTICA:
{st.session_state.expediente['diagnostico_situacion'] or 'Sin especificar.'}

CONCLUSIONES DEL EQUIPO INTERDISCIPLINAR:
{st.session_state.expediente['conclusiones_equipo'] or 'Sin especificar.'}

4. PRONÓSTICO Y PROPUESTA DE INTERVENCIÓN
--------------------------------------------------------------------------------
{st.session_state.expediente['pronostico_evolutivo'] or 'Sin especificar.'}

--------------------------------------------------------------------------------
REDACTOR/A DESIGNADO/A: {st.session_state.expediente['redactor_designado']}
REVISIÓN TÉCNICA DE EQUIPO: {'Aprobada' if st.session_state.expediente['p7_revision_equipo'] else 'Pendiente'}
VºBº DE DIRECCIÓN: {'Concedido' if st.session_state.expediente['p8_vobo_direccion'] else 'Pendiente'}
================================================================================
"""

    st.subheader("📄 Vista Previa del Informe Unificado Listo para Copiar/Enviar")
    st.code(informe_texto, language="markdown")

    st.download_button(
        label="📥 Descargar Informe en Texto (.txt)",
        data=informe_texto,
        file_name=f"Informe_{exp_num.replace('/', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
