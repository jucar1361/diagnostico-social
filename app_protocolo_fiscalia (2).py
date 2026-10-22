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
    .area-header-ts { background-color: #e8f5e9; color: #1b5e20; padding: 8px 12px; border-radius: 6px; border-left: 5px solid #2e7d32; font-weight: bold; margin-bottom: 8px;}
    .area-header-edu { background-color: #e3f2fd; color: #0d47a1; padding: 8px 12px; border-radius: 6px; border-left: 5px solid #1565c0; font-weight: bold; margin-bottom: 8px;}
    .area-header-psi { background-color: #f3e5f5; color: #4a148c; padding: 8px 12px; border-radius: 6px; border-left: 5px solid #6a1b9a; font-weight: bold; margin-bottom: 8px;}
    </style>
""", unsafe_allow_html=True)

# Helper para selecciones seguras
def safe_index(options, value, default_index=0):
    if value in options:
        return options.index(value)
    return default_index

# Inicialización de session_state para datos del expediente
if "expediente" not in st.session_state:
    st.session_state.expediente = {
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
        
        # Formulario Trabajo Social (TS)
        "val_ts_habitabilidad": "Adecuada",
        "val_ts_economia": "Estable",
        "val_ts_red_social": "Suficiente",
        "val_ts_riesgos": [],
        "val_ts_protectores": [],
        "val_ts_entorno": "",
        
        # Formulario Educación Social (EDU)
        "val_edu_escolarizacion": "Adecuada",
        "val_edu_absentismo": "Sin absentismo (<5%)",
        "val_edu_conducta": "Normotípica",
        "val_edu_riesgos": [],
        "val_edu_protectores": [],
        "val_edu_escolar": "",
        
        # Formulario Psicología (PSI)
        "val_psi_estilo_parental": "Democrático / Normativo",
        "val_psi_vinculo": "Afectivo seguro",
        "val_psi_estado_menor": "Estable emocionalmente",
        "val_psi_riesgos": [],
        "val_psi_protectores": [],
        "val_psi_emocional": "",
        
        # Deliberación de Equipo
        "conclusiones_equipo": "",
        "diagnostico_situacion": "",
        "pronostico_evolutivo": "",
        "medidas_propuestas": [],
        "nivel_riesgo": "Riesgo Moderado",
        "redactor_designado": "Trabajo Social (TS)",
        
        # Revisiones y VºBº
        "p7_revision_equipo": False,
        "p8_vobo_direccion": False,
        "p8_enviado_oficial": False
    }

# Cargar caso de prueba completo
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
    
    # TS
    st.session_state.expediente["val_ts_habitabilidad"] = "Adecuada"
    st.session_state.expediente["val_ts_economia"] = "Estable"
    st.session_state.expediente["val_ts_red_social"] = "Escasa / Limitada"
    st.session_state.expediente["val_ts_riesgos"] = ["Elevada conflictividad entre progenitores", "Aislamiento de red extensa"]
    st.session_state.expediente["val_ts_protectores"] = ["Vivienda en buenas condiciones de habitabilidad", "Ingresos económicos suficientes"]
    st.session_state.expediente["val_ts_entorno"] = "Vivienda en condiciones adecuadas de habitabilidad y equipamiento. Red social de apoyo limitada tras traslado reciente de domicilio. Ingresos estables pero elevada conflictividad interparental en proceso de separación no regulada."
    
    # EDU
    st.session_state.expediente["val_edu_escolarizacion"] = "Adecuada"
    st.session_state.expediente["val_edu_absentismo"] = "Absentismo incipiente (5-15%)"
    st.session_state.expediente["val_edu_conducta"] = "Normotípica"
    st.session_state.expediente["val_edu_riesgos"] = ["Bajada puntual en rendimiento académico", "Faltas injustificadas recientes"]
    st.session_state.expediente["val_edu_protectores"] = ["Buena integración con grupo de iguales", "Buena actitud de la menor hacia el centro"]
    st.session_state.expediente["val_edu_escolar"] = "Faltas injustificadas puntuales (12% en el último mes). Adecuada integración con su grupo de iguales, aunque se observa bajada en el rendimiento académico motivada por el clima de discusión en el hogar."
    
    # PSI
    st.session_state.expediente["val_psi_estilo_parental"] = "Inconsistente / Conflictivo"
    st.session_state.expediente["val_psi_vinculo"] = "Afectivo seguro"
    st.session_state.expediente["val_psi_estado_menor"] = "Sintomatología ansiosa"
    st.session_state.expediente["val_psi_riesgos"] = ["Exposición a conflicto interparental", "Ansiedad reactiva a la separación"]
    st.session_state.expediente["val_psi_protectores"] = ["Vínculo afectivo positivo con ambos progenitores", "Capacidad de expresión emocional"]
    st.session_state.expediente["val_psi_emocional"] = "La menor expresa sintomatología ansiosa directamente vinculada al clima de discusión en el hogar. Mantiene buen vínculo afectivo con ambos progenitores pero demanda neutralidad y cese del conflicto."
    
    # Deliberación
    st.session_state.expediente["conclusiones_equipo"] = "Situación de riesgo social moderado derivada de la alta conflictividad parental en contexto de separación no regulada. No se observan indicadores de desprotección grave ni maltrato activo."
    st.session_state.expediente["diagnostico_situacion"] = "Riesgo sociofamiliar moderado por exposición continua a conflicto interparental desestructurante y absentismo escolar incipiente."
    st.session_state.expediente["pronostico_evolutivo"] = "Favorable si se formaliza mediación familiar y seguimiento psicopedagógico intensivo. Reservado si se mantiene la tensión interparental sin intervención."
    st.session_state.expediente["medidas_propuestas"] = ["Derivación a Servicio de Mediación Familiar", "Acompañamiento psicopedagógico escolar", "Plan de apoyo a la parentalidad positiva"]
    st.session_state.expediente["nivel_riesgo"] = "Riesgo Moderado"
    st.session_state.expediente["redactor_designado"] = "Educación Social (EDU)"
    st.session_state.expediente["p7_revision_equipo"] = True
    st.session_state.expediente["p8_vobo_direccion"] = False
    st.session_state.expediente["p8_enviado_oficial"] = False

# Sidebar
with st.sidebar:
    st.title("⚖️ Control de Plazos")
    st.subheader("Procedimiento Urgente (10 Días)")
    
    fecha_rec = st.session_state.expediente.get("fecha_recepcion", datetime.date.today())
    if isinstance(fecha_rec, str):
        try:
            fecha_rec = datetime.datetime.strptime(fecha_rec, "%Y-%m-%d").date()
        except Exception:
            fecha_rec = datetime.date.today()
    if not isinstance(fecha_rec, datetime.date):
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
        for k in list(st.session_state.expediente.keys()):
            if isinstance(st.session_state.expediente[k], bool):
                st.session_state.expediente[k] = False
            elif isinstance(st.session_state.expediente[k], list):
                st.session_state.expediente[k] = []
            elif isinstance(st.session_state.expediente[k], str):
                st.session_state.expediente[k] = ""
        st.session_state.expediente["fecha_recepcion"] = datetime.date.today()
        st.session_state.expediente["organo"] = "Fiscalía de Menores"
        st.session_state.expediente["nivel_riesgo"] = "Riesgo Moderado"
        st.session_state.expediente["redactor_designado"] = "Trabajo Social (TS)"
        st.session_state.expediente["val_ts_habitabilidad"] = "Adecuada"
        st.session_state.expediente["val_ts_economia"] = "Estable"
        st.session_state.expediente["val_ts_red_social"] = "Suficiente"
        st.session_state.expediente["val_edu_escolarizacion"] = "Adecuada"
        st.session_state.expediente["val_edu_absentismo"] = "Sin absentismo (<5%)"
        st.session_state.expediente["val_edu_conducta"] = "Normotípica"
        st.session_state.expediente["val_psi_estilo_parental"] = "Democrático / Normativo"
        st.session_state.expediente["val_psi_vinculo"] = "Afectivo seguro"
        st.session_state.expediente["val_psi_estado_menor"] = "Estable emocionalmente"
        st.rerun()

# Encabezado Principal
st.title("⚖️ Protocolo de Actuación Rápida (10 Días)")
st.caption("Peticiones de la Fiscalía de Menores y Servicio de Protección de Menores — Formulario Interdisciplinar Optimizado (TS, EDU, PSI)")

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
    "2️⃣ Investigación y Formularios de Área (Días 2-4)",
    "3️⃣ Deliberación de Equipo y Diagnóstico (Días 5-6)",
    "4️⃣ Informe Final Unificado (Días 7-10)"
])

# ==================== TAB 1: RECEPCIÓN Y FILTRO ====================
with tab1:
    st.header("1. Datos del Oficio y Coordinación Inicial (Primeras 24-48 Horas)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.expediente["num_expediente"] = st.text_input("Nº de Expediente / Oficio:", st.session_state.expediente["num_expediente"])
        
        opts_org = ["Fiscalía de Menores", "Servicio de Protección de Menores", "Juzgado de Familia"]
        idx_org = safe_index(opts_org, st.session_state.expediente["organo"], 0)
        st.session_state.expediente["organo"] = st.selectbox("Órgano Solicitante:", opts_org, index=idx_org)
        
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
        st.markdown("<div class='area-header-ts'>📁 Trabajo Social (TS)</div>", unsafe_allow_html=True)
        st.session_state.expediente["p2_ts_previo"] = st.checkbox(
            "Recopilación de información previa / expediente histórico",
            value=st.session_state.expediente["p2_ts_previo"]
        )

    with c2:
        st.markdown("<div class='area-header-edu'>🎓 Educación Social (EDU)</div>", unsafe_allow_html=True)
        st.session_state.expediente["p2_edu_contacto_colegio"] = st.checkbox(
            "Contacto telefónico inicial con centro educativo",
            value=st.session_state.expediente["p2_edu_contacto_colegio"]
        )
        st.session_state.expediente["p2_edu_informe_legal"] = st.checkbox(
            "Solicitud formal de informe escolar por vía legal",
            value=st.session_state.expediente["p2_edu_informe_legal"]
        )

    with c3:
        st.markdown("<div class='area-header-psi'>🧠 Psicología (PSI)</div>", unsafe_allow_html=True)
        st.session_state.expediente["p2_psi_contacto_familia"] = st.checkbox(
            "Contacto telefónico con la familia",
            value=st.session_state.expediente["p2_psi_contacto_familia"]
        )
        fecha_cita_def = st.session_state.expediente["p2_psi_cita_fecha"] or (datetime.date.today() + datetime.timedelta(days=1))
        st.session_state.expediente["p2_psi_cita_fecha"] = st.date_input("Fecha cita entrevista (máx 24-48h):", fecha_cita_def)

# ==================== TAB 2: INVESTIGACIÓN Y FORMULARIOS DE ÁREA ====================
with tab2:
    st.header("2. Trabajo de Campo y Formularios de Valoración Sectorial")
    st.info("💡 **Ajuste de formularios:** Cada profesional dispone de indicadores rápidos y campo narrativo estructurado para acelerar la recogida de datos en el plazo de 10 días.")

    st.subheader("Paso 3: Verificación de Entrevistas y Visitas de Campo")
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

    st.divider()
    st.subheader("Paso 4: Formularios Específicos por Área Técnica")

    # --- FORMULARIO TRABAJO SOCIAL ---
    with st.expander("🟢 FORMULARIO 1: TRABAJO SOCIAL (Entorno Social, Economía y Vivienda)", expanded=True):
        st.markdown("<div class='area-header-ts'>📁 Área de Trabajo Social (TS)</div>", unsafe_allow_html=True)
        col_ts1, col_ts2, col_ts3 = st.columns(3)
        with col_ts1:
            opts_hab = ["Adecuada", "Deficiencias Menores", "Insalubridad / Inseguridad", "Hacinamiento"]
            idx_hab = safe_index(opts_hab, st.session_state.expediente["val_ts_habitabilidad"], 0)
            st.session_state.expediente["val_ts_habitabilidad"] = st.selectbox("Habitabilidad y Vivienda:", opts_hab, index=idx_hab)
        with col_ts2:
            opts_eco = ["Estable", "Precariedad Coyuntural", "Pobreza Severa / Sin Ingresos", "Dependencia de Subsidios"]
            idx_eco = safe_index(opts_eco, st.session_state.expediente["val_ts_economia"], 0)
            st.session_state.expediente["val_ts_economia"] = st.selectbox("Situación Socioeconómica:", opts_eco, index=idx_eco)
        with col_ts3:
            opts_red = ["Suficiente", "Escasa / Limitada", "Aislamiento Social", "Red Conflictiva / Entorno Deteriorado"]
            idx_red = safe_index(opts_red, st.session_state.expediente["val_ts_red_social"], 0)
            st.session_state.expediente["val_ts_red_social"] = st.selectbox("Red Social / Familiar Extensa:", opts_red, index=idx_red)

        col_ts_r, col_ts_p = st.columns(2)
        with col_ts_r:
            st.session_state.expediente["val_ts_riesgos"] = st.multiselect(
                "Factores de Riesgo Social detectados:",
                ["Elevada conflictividad entre progenitores", "Inestabilidad residencial / Riesgo desahucio", "Precariedad económica extrema", "Aislamiento de red extensa", "Consumo de sustancias en el entorno", "Incumplimiento de necesidades básicas"],
                default=st.session_state.expediente["val_ts_riesgos"]
            )
        with col_ts_p:
            st.session_state.expediente["val_ts_protectores"] = st.multiselect(
                "Factores de Protección Social detectados:",
                ["Vivienda en buenas condiciones de habitabilidad", "Ingresos económicos suficientes", "Apoyo activo de familia extensa", "Adecuado uso de recursos comunitarios", "Buena vinculación con Servicios Sociales"],
                default=st.session_state.expediente["val_ts_protectores"]
            )

        st.session_state.expediente["val_ts_entorno"] = st.text_area(
            "Síntesis Narrativa del Entorno Social y Domiciliario (TS):",
            value=st.session_state.expediente["val_ts_entorno"],
            height=90,
            help="Describir brevemente las condiciones del hogar, situación laboral/económica de los adultos y apoyo familiar."
        )

    # --- FORMULARIO EDUCACIÓN SOCIAL ---
    with st.expander("🔵 FORMULARIO 2: EDUCACIÓN SOCIAL (Ámbito Escolar y Conductual)", expanded=True):
        st.markdown("<div class='area-header-edu'>🎓 Área de Educación Social (EDU)</div>", unsafe_allow_html=True)
        col_ed1, col_ed2, col_ed3 = st.columns(3)
        with col_ed1:
            opts_esc = ["Adecuada", "Desfase Curricular", "Rendimiento Bajo", "Riesgo de Abandono"]
            idx_esc = safe_index(opts_esc, st.session_state.expediente["val_edu_escolarizacion"], 0)
            st.session_state.expediente["val_edu_escolarizacion"] = st.selectbox("Adaptación Escolar:", opts_esc, index=idx_esc)
        with col_ed2:
            opts_abs = ["Sin absentismo (<5%)", "Absentismo incipiente (5-15%)", "Absentismo grave (15-50%)", "Desescolarización / Absentismo crónico (>50%)"]
            idx_abs = safe_index(opts_abs, st.session_state.expediente["val_edu_absentismo"], 0)
            st.session_state.expediente["val_edu_absentismo"] = st.selectbox("Nivel de Absentismo:", opts_abs, index=idx_abs)
        with col_ed3:
            opts_cond = ["Normotípica", "Disruptiva en aula", "Aislamiento de iguales", "Problemas de conducta graves"]
            idx_cond = safe_index(opts_cond, st.session_state.expediente["val_edu_conducta"], 0)
            st.session_state.expediente["val_edu_conducta"] = st.selectbox("Conducta e Integración Social:", opts_cond, index=idx_cond)

        col_ed_r, col_ed_p = st.columns(2)
        with col_ed_r:
            st.session_state.expediente["val_edu_riesgos"] = st.multiselect(
                "Factores de Riesgo Educativo/Conductual:",
                ["Bajada puntual en rendimiento académico", "Faltas injustificadas recientes", "Dificultades de relación con iguales", "Uso inadecuado de TICs / Redes", "Ocio no estructurado / Callejero", "Conductas disociales incipientes"],
                default=st.session_state.expediente["val_edu_riesgos"]
            )
        with col_ed_p:
            st.session_state.expediente["val_edu_protectores"] = st.multiselect(
                "Factores de Protección Educativos:",
                ["Buena integración con grupo de iguales", "Buena actitud de la menor hacia el centro", "Participación en actividades extraescolares", "Tutoría/Profesorado implicado y protector", "Hábitos de estudio supervisados"],
                default=st.session_state.expediente["val_edu_protectores"]
            )

        st.session_state.expediente["val_edu_escolar"] = st.text_area(
            "Síntesis Narrativa del Ámbito Escolar y Socioeducativo (EDU):",
            value=st.session_state.expediente["val_edu_escolar"],
            height=90,
            help="Describir nivel de escolarización, informes del colegio, integración con iguales y hábitos de ocio."
        )

    # --- FORMULARIO PSICOLOGÍA ---
    with st.expander("🟣 FORMULARIO 3: PSICOLOGÍA (Salud Emocional y Dinámica Parental)", expanded=True):
        st.markdown("<div class='area-header-psi'>🧠 Área de Psicología (PSI)</div>", unsafe_allow_html=True)
        col_ps1, col_ps2, col_ps3 = st.columns(3)
        with col_ps1:
            opts_par = ["Democrático / Normativo", "Inconsistente / Conflictivo", "Autoritario / Rígido", "Permisivo / Negligente"]
            idx_par = safe_index(opts_par, st.session_state.expediente["val_psi_estilo_parental"], 0)
            st.session_state.expediente["val_psi_estilo_parental"] = st.selectbox("Estilo Educativo Parental:", opts_par, index=idx_par)
        with col_ps2:
            opts_vin = ["Afectivo seguro", "Ambivalente / Ansioso", "Evitativo", "Desorganizado / Inseguro"]
            idx_vin = safe_index(opts_vin, st.session_state.expediente["val_psi_vinculo"], 0)
            st.session_state.expediente["val_psi_vinculo"] = st.selectbox("Vínculo Afectivo Observado:", opts_vin, index=idx_vin)
        with col_ps3:
            opts_men = ["Estable emocionalmente", "Sintomatología ansiosa", "Labilidad emocional / Tristeza", "Labilidad / Impulsividad grave"]
            idx_men = safe_index(opts_men, st.session_state.expediente["val_psi_estado_menor"], 0)
            st.session_state.expediente["val_psi_estado_menor"] = st.selectbox("Estado Emocional del Menor:", opts_men, index=idx_men)

        col_ps_r, col_ps_p = st.columns(2)
        with col_ps_r:
            st.session_state.expediente["val_psi_riesgos"] = st.multiselect(
                "Factores de Riesgo Psicológico/Parental:",
                ["Exposición a conflicto interparental", "Ansiedad reactiva a la separación", "Instrumentalización del menor", "Falta de límites / Incoherencia pautas", "Incapacidad de contención emocional de adultos"],
                default=st.session_state.expediente["val_psi_riesgos"]
            )
        with col_ps_p:
            st.session_state.expediente["val_psi_protectores"] = st.multiselect(
                "Factores de Protección Psicológicos:",
                ["Vínculo afectivo positivo con ambos progenitores", "Capacidad de expresión emocional", "Buena introspección / Resiliencia del menor", "Progenitores receptivos al asesoramiento profesional"],
                default=st.session_state.expediente["val_psi_protectores"]
            )

        st.session_state.expediente["val_psi_emocional"] = st.text_area(
            "Síntesis Narrativa Psicológica y Familiar (PSI):",
            value=st.session_state.expediente["val_psi_emocional"],
            height=90,
            help="Describir vivencia emocional del menor, estilo de crianza, alianzas o tensiones internas en la familia."
        )

# ==================== TAB 3: DELIBERACIÓN DE EQUIPO Y DIAGNÓSTICO ====================
with tab3:
    st.header("3. Deliberación Interdisciplinar y Asignación de Redacción")
    st.caption("Síntesis unificada integrada por las valoraciones conjuntas de Trabajo Social, Educación Social y Psicología.")

    col_r1, col_r2 = st.columns([2, 1])
    with col_r1:
        st.session_state.expediente["conclusiones_equipo"] = st.text_area(
            "1. Conclusiones unificadas de la deliberación técnica del equipo:",
            value=st.session_state.expediente["conclusiones_equipo"],
            height=110
        )
        st.session_state.expediente["diagnostico_situacion"] = st.text_area(
            "2. Diagnóstico de la situación (Riesgo / Desprotección / Normalización):",
            value=st.session_state.expediente["diagnostico_situacion"],
            height=80
        )
        st.session_state.expediente["pronostico_evolutivo"] = st.text_area(
            "3. Pronóstico y propuesta de intervención recomendada:",
            value=st.session_state.expediente["pronostico_evolutivo"],
            height=80
        )
    
    with col_r2:
        opts_riesgo = ["Sin Riesgo Apreciable", "Riesgo Leve", "Riesgo Moderado", "Riesgo Grave / Desprotección"]
        idx_riesgo = safe_index(opts_riesgo, st.session_state.expediente["nivel_riesgo"], 2)
        st.session_state.expediente["nivel_riesgo"] = st.selectbox(
            "Nivel de Riesgo Evaluado:",
            opts_riesgo,
            index=idx_riesgo
        )

        st.session_state.expediente["medidas_propuestas"] = st.multiselect(
            "Propuestas de Medidas / Intervenciones recomendadas:",
            ["Derivación a Servicio de Mediación Familiar", "Acompañamiento psicopedagógico escolar", "Plan de apoyo a la parentalidad positiva", "Seguimiento desde Servicios Sociales Básicos", "Tratamiento en Salud Mental Infanto-Juvenil", "Propuesta de Medida de Protección de Menores"],
            default=st.session_state.expediente["medidas_propuestas"]
        )

        st.subheader("Paso 6: Asignación de Redacción")
        opts_red = ["Trabajo Social (TS)", "Educación Social (EDU)", "Psicología (PSI)"]
        idx_red = safe_index(opts_red, st.session_state.expediente["redactor_designado"], 0)
        st.session_state.expediente["redactor_designado"] = st.radio(
            "Profesional designado/a para ensamblar el informe unificado:",
            opts_red,
            index=idx_red
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
    
    # Resumen de factores
    r_ts = ", ".join(st.session_state.expediente["val_ts_riesgos"]) if st.session_state.expediente["val_ts_riesgos"] else "Ninguno reseñado"
    p_ts = ", ".join(st.session_state.expediente["val_ts_protectores"]) if st.session_state.expediente["val_ts_protectores"] else "Ninguno reseñado"
    
    r_edu = ", ".join(st.session_state.expediente["val_edu_riesgos"]) if st.session_state.expediente["val_edu_riesgos"] else "Ninguno reseñado"
    p_edu = ", ".join(st.session_state.expediente["val_edu_protectores"]) if st.session_state.expediente["val_edu_protectores"] else "Ninguno reseñado"

    r_psi = ", ".join(st.session_state.expediente["val_psi_riesgos"]) if st.session_state.expediente["val_psi_riesgos"] else "Ninguno reseñado"
    p_psi = ", ".join(st.session_state.expediente["val_psi_protectores"]) if st.session_state.expediente["val_psi_protectores"] else "Ninguno reseñado"

    meds = "\n- ".join(st.session_state.expediente["medidas_propuestas"]) if st.session_state.expediente["medidas_propuestas"] else "Sin medidas específicas seleccionadas."

    informe_texto = f"""================================================================================
INFORME SOCIAL Y PSICOEDUCATIVO UNIFICADO PARA {org.upper()}
================================================================================
EXPEDIENTE / OFICIO Nº: {exp_num}
ÓRGANO SOLICITANTE: {org}
FECHA DE SOLICITUD / ENTRADA: {st.session_state.expediente['fecha_recepcion']}
FECHA DE EMISIÓN: {datetime.date.today().strftime('%d/%m/%Y')}

1. DATOS DE IDENTIFICACIÓN Y MARCO LEGAL
--------------------------------------------------------------------------------
Nombre del/la Menor: {nombre_m}
Fecha de Nacimiento: {st.session_state.expediente['fecha_nacimiento'] or 'No consta'}
Tutores Legales: {st.session_state.expediente['tutores_legales'] or 'No consta'}
Domicilio: {st.session_state.expediente['domicilio'] or 'No consta'}

2. VALORACIÓN SECTORIAL INTERDISCIPLINAR DE EQUIPO
--------------------------------------------------------------------------------
A) ÁREA DE TRABAJO SOCIAL (Entorno Social, Economía y Vivienda):
• Habitabilidad: {st.session_state.expediente['val_ts_habitabilidad']} | Economía: {st.session_state.expediente['val_ts_economia']} | Red Social: {st.session_state.expediente['val_ts_red_social']}
• Factores de Riesgo Social: {r_ts}
• Factores de Protección Social: {p_ts}
• VALORACIÓN NARRATIVA:
{st.session_state.expediente['val_ts_entorno'] or 'Pendiente de cumplimentar.'}

B) ÁREA DE EDUCACIÓN SOCIAL (Ámbito Escolar y Conductual):
• Adaptación Escolar: {st.session_state.expediente['val_edu_escolarizacion']} | Absentismo: {st.session_state.expediente['val_edu_absentismo']} | Conducta: {st.session_state.expediente['val_edu_conducta']}
• Factores de Riesgo Educativo: {r_edu}
• Factores de Protección Educativos: {p_edu}
• VALORACIÓN NARRATIVA:
{st.session_state.expediente['val_edu_escolar'] or 'Pendiente de cumplimentar.'}

C) ÁREA DE PSICOLOGÍA (Salud Emocional y Crianza):
• Estilo Parental: {st.session_state.expediente['val_psi_estilo_parental']} | Vínculo: {st.session_state.expediente['val_psi_vinculo']} | Estado Emocional: {st.session_state.expediente['val_psi_estado_menor']}
• Factores de Riesgo Psicológico: {r_psi}
• Factores de Protección Psicológicos: {p_psi}
• VALORACIÓN NARRATIVA:
{st.session_state.expediente['val_psi_emocional'] or 'Pendiente de cumplimentar.'}

3. DIAGNÓSTICO Y CONCLUSIONES DEL EQUIPO INTERDISCIPLINAR
--------------------------------------------------------------------------------
NIVEL DE RIESGO EVALUADO: {st.session_state.expediente['nivel_riesgo'].upper()}

DIAGNÓSTICO DE LA SITUACIÓN:
{st.session_state.expediente['diagnostico_situacion'] or 'Sin especificar.'}

CONCLUSIONES DE LA DELIBERACIÓN TÉCNICA (TS + EDU + PSI):
{st.session_state.expediente['conclusiones_equipo'] or 'Sin especificar.'}

4. PRONÓSTICO Y PROPUESTA DE MEDIDAS DE INTERVENCIÓN
--------------------------------------------------------------------------------
PRONÓSTICO EVOLUTIVO:
{st.session_state.expediente['pronostico_evolutivo'] or 'Sin especificar.'}

PROPUESTA DE MEDIDAS Y RECOMENDACIONES TÉCNICAS:
- {meds}

--------------------------------------------------------------------------------
REDACTOR/A DESIGNADO/A: {st.session_state.expediente['redactor_designado']}
REVISIÓN TÉCNICA DE EQUIPO: {'✅ Aprobada' if st.session_state.expediente['p7_revision_equipo'] else '⏳ Pendiente'}
VºBº DE DIRECCIÓN: {'✅ Concedido' if st.session_state.expediente['p8_vobo_direccion'] else '⏳ Pendiente'}
REGISTRO DE SALIDA: {'📨 Enviado' if st.session_state.expediente['p8_enviado_oficial'] else '⏳ Pendiente de envío'}
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
