import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="EIC La Floresta", layout="wide")

# 2. CONEXIÓN A GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1iC5HihmFohbGf00SUC4Sdsyn9f66DwUSup5Ba5NNMyA/edit?gid=149634862#gid=149634862"


# --- SISTEMA DE ACCESO SIMPLE ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔑 Acceso Docentes - La Floresta")
    password = st.text_input("Introduce la clave de acceso:", type="password")
    if st.button("Entrar"):
        if password == "Floresta2026":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Clave incorrecta") 
    st.stop()

# --- LISTAS DE OPCIONES ---
lista_ucas = [
    "HUELLITAS DE ALEGRES", "HUELLITAS DE IGUALDAD", "HUELLITAS DE ESPERANZA", 
    "HUELLITAS DE BONDAD", "HUELLITAS DE AMOR", "HUELLITAS DE AMISTAD", 
    "HUELLITAS DE PAZ", "HUELLITAS DE COLORES", "HUELLITAS DE DIOS", 
    "HUELLITAS DE PERDON", "HUELLITAS DE TENACIDAD", "HUELLITAS DE FELICIDAD", 
    "ANGELITOS DE DIOS", "HUELLITAS DE FE", "HUELLITAS DE VALENTIA", 
    "HUELLITAS DE ILUSION", "HUELLITAS DE FORTALEZA", "CARITAS ALEGRES", 
    "HUELLITAS DE OPTIMISMO", "HUELLITAS DE SUPERACIÓN", "HUELLITAS DE LIBERTAD", 
    "CARITAS FELICES", "HUELLITAS DE ESFUERZO"
]

lista_docentes = [
    "YURLEIBY", "CLAUDIA MEDINA", "MARIA JOSE TRILLOS", "CLAUDIA DIAZ", 
    "YENNY LOZANO", "MARIA JOSE BARBOSA", "VANNESA LOZANO", "ELIZABETH BOHORQUEZ", 
    "ALVEIRO MEDINA", "YESSICA TRILLOS", "JUAN CAMILO", "MAYERLY DONADO", 
    "AURELLY", "MONICA", "MARIA FERNANDA", "MARY LUZ", "MARLY TATIANA", 
    "LEIDY BENAVIDEZ", "ANGELICA ROJAS", "ELAINE QUINTERO", "AIDA QUINTERO", 
    "NANCY VERGEL", "YERLY PRADA"
]

lista_tipo_doc = ["RC", "CC", "CE", "TI", "PPT", "SIN DOCUMENTO"]

# --- FUNCIONES DE APOYO ---
def calcular_edad_detallada(fecha_nac):
    if not fecha_nac: return "N/A"
    if isinstance(fecha_nac, str):
        try:
            fecha_nac = datetime.strptime(fecha_nac, '%Y-%m-%d').date()
        except: return "N/A"
    hoy = datetime.now().date()
    anios = hoy.year - fecha_nac.year
    meses = hoy.month - fecha_nac.month
    dias = hoy.day - fecha_nac.day
    if dias < 0:
        meses -= 1
        dias += 30 
    if meses < 0:
        anios -= 1
        meses += 12
    return f"{anios} AÑOS, {meses} MESES, {dias} DÍAS"

def guardar_datos(nuevo_dict, nombre_hoja):
    conn = st.connection("gsheets", type=GSheetsConnection)

    # 🔹 convertir dict → DataFrame de UNA fila
    nuevo_df = pd.DataFrame([nuevo_dict])

    try:
        df_actual = conn.read(
            spreadsheet=SPREADSHEET_URL,
            worksheet=nombre_hoja
        )
    except:
        df_actual = pd.DataFrame()

    if df_actual.empty:
        nuevo_df.insert(0, "N°", 1)
        df_final = nuevo_df
    else:
        consecutivo = len(df_actual) + 1
        nuevo_df.insert(0, "N°", consecutivo)
        df_final = pd.concat([df_actual, nuevo_df], ignore_index=True)

    conn.update(
        spreadsheet=SPREADSHEET_URL,
        worksheet=nombre_hoja,
        data=df_final
    )
    st.cache_data.clear()

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp {
        background-color: #FDFCF0; /* Un crema muy suave para no cansar la vista */
    }

    /* Personalización del Menú Lateral */
    [data-testid="stSidebar"] {
        background-color: #E3F2FD; /* Azul pastel muy claro */
        border-right: 2px solid #BBDEFB;
    }

    /* Botones del Menú Lateral */
    .stButton>button {
        width: 100%;
        border-radius: 20px; /* Más redondeados */
        height: 3.5em;
        background-color: #4CAF50; /* Verde juguetón */
        color: white;
        font-weight: bold;
        border: 2px solid #388E3C;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #81C784; /* Verde más claro al pasar el mouse */
        border: 2px solid #4CAF50;
        transform: scale(1.02); /* Efecto de crecimiento suave */
    }

    /* Títulos y Subtítulos */
    h1 {
        color: #1976D2; /* Azul vibrante */
        font-family: 'Comic Sans MS', cursive, sans-serif; /* Opcional, da toque infantil */
    }
    
    h2, h3 {
        color: #F57C00; /* Naranja amigable */
    }

    /* Estilo para las métricas del Dashboard */
    [data-testid="stMetricValue"] {
        color: #D32F2F; /* Rojo para los números */
        font-weight: bold;
    }
    
    /* Estilo para el texto de sugerencia (placeholder) en los selectores */
    div[data-baseweb="select"] div[aria-selected="false"] {
        color: #9E9E9E !important;
        font-style: italic;
    }

    /* Mejorar las entradas de texto */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #90CAF9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'menu_opcion' not in st.session_state:
    st.session_state.menu_opcion = "Inicio"

with st.sidebar:
    st.markdown("## 🎈 MI FLORESTA")
    if st.button("🏠 Inicio Feliz"): st.session_state.menu_opcion = "Inicio"
    if st.button("👶 Nuevo Pequeñín / Gestante"): st.session_state.menu_opcion = "Ingreso" 
    if st.button("👋 Retirar Participante"): st.session_state.menu_opcion = "Retiro"
    if st.button("📚 Ver listado"): st.session_state.menu_opcion = "Listado"
    st.markdown("---")
    if st.button("🚪 Salir de la Aplicación"):
        st.session_state.autenticado = False
        st.rerun()
    st.sidebar.markdown("<div style='text-align: center; font-size: 0.8rem;'><p>© 2026 LA FLORESTA<br>Ing. Oscar Sánchez Pérez</p></div>", unsafe_allow_html=True)

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo: st.image("EIC.jpg", width=150)
with col_titulo: st.title("Asociación de Padres de Familia - Hogar Infantil La Floresta")

# --- SECCIÓN: INICIO ---
if st.session_state.menu_opcion == "Inicio":
    st.header("📊 Cuadro de Control")
    try:
        df_ing = conn.read(worksheet="INGRESOS", ttl=0) # ttl=0 evita que use datos viejos guardados
        try:
            df_ing = conn.read(worksheet="RETIROS", ttl=0) # ttl=0 evita que use datos viejos guardados
            ids_ret = df_ret["ID"].astype(str).tolist()
        except:
            ids_ret = []
        
        df_activos = df_ing[~df_ing["ID PARTICIPANTE"].astype(str).isin(ids_ret)]
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Histórico", len(df_ing))
        m2.metric("Participantes Activos", len(df_activos))
        m3.metric("Total Retiros", len(ids_ret))

        if not df_activos.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🌈 Población por Tipo")
                torta = df_activos["TIPO_PERSONA"].value_counts()
                import plotly.graph_objects as go
                fig = go.Figure(data=[go.Pie(labels=torta.index, values=torta.values, hole=.3)])
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.subheader("📍 Cobertura por UCA")
                st.bar_chart(df_activos["UCA"].value_counts())
    except:
        st.info("No hay base de datos aún. Registre su primer participante.")

# --- SECCIÓN: INGRESO ---
elif st.session_state.menu_opcion == "Ingreso":
    st.header("📝 Formulario de Registro")
    tipo_persona = st.selectbox("Tipo de Participante", ["NIÑO", "NIÑA", "MADRE GESTANTE"], index=None, placeholder="Seleccione...")
    
    col1, col2, col3 = st.columns(3)
    nombre = col1.text_input("Nombre Completo").upper()
    tipo_doc = col1.selectbox("Tipo de Documento", options=lista_tipo_doc, index=None)
    id_niño = col1.text_input("N° de Identificación")
    discapacidad = col1.radio("¿Discapacidad?", ["NO", "SI"], horizontal=True)
    
    lugar_nac = col2.text_input("Lugar de Nacimiento").upper()
    fecha_nac = col2.date_input("Fecha de Nacimiento", min_value=datetime(1940, 1, 1))
    telefono = col2.text_input("Número Telefónico")
    
    fecha_ingreso = col3.date_input("Fecha de Ingreso")
    docente = col3.selectbox("Docente Encargado", options=lista_docentes, index=None)
    uca = col3.selectbox("Unidad UCA", options=lista_ucas, index=None)

    direccion = st.text_input("DIRECCIÓN COMPLETA", value="KDX ").upper()

    # LÓGICA DE FAMILIA
    es_menor_gestante = (tipo_persona == "MADRE GESTANTE" and tipo_doc == "TI")
    necesita_acudiente = (tipo_persona in ["NIÑO", "NIÑA"]) or es_menor_gestante
    necesita_padres = (tipo_persona in ["NIÑO", "NIÑA"]) 
    if necesita_acudiente:
        st.subheader("👨‍👩‍👧 Información del Responsable")
        with st.expander("Datos del Responsable", expanded=True):
            a_c1, a_c2, a_c3 = st.columns(3)
            nombre_acu = a_c1.text_input("Nombre Responsable").upper()
            tp_doc_acu = a_c1.selectbox("Tipo Doc Acu.", ["CC", "TI", "CE", "PPT"])
            id_acu = a_c2.text_input("N° Documento Acu.")
            parentesco = a_c2.selectbox("Parentesco", ["MADRE", "PADRE", "ABUELOS", "TIOS", "OTRO"])
            f_nac_acu = a_c3.date_input("Fecha Nac Acu.", value=datetime(1990, 1, 1))
            l_nac_acu = a_c3.text_input("Lugar Nac Acu.").upper()

        if necesita_padres:
            with st.expander("Datos de los Padres"):
                t1, t2 = st.tabs(["Padre", "Madre"])
                val_p_nom = nombre_acu if parentesco == "PADRE" else "" 
                val_p_id = id_acu if parentesco == "PADRE" else "" 
                val_p_doc = ["CC", "TI", "CE", "PPT"].index(tp_doc_acu) if parentesco == "PADRE" else 0
                
                with t1:
                    p_c1, p_c2 = st.columns(2)
                    nombre_p = p_c1.text_input("Nombre del Padre", value=val_p_nom).upper()
                    id_p = p_c1.text_input("ID Padre", value=val_p_id)
                    tp_doc_p = p_c2.selectbox("Tipo Doc Padre", ["CC", "TI", "CE", "PPT"], index=val_p_doc)
                    f_nac_p = p_c2.date_input("Fecha Padre", value=f_nac_acu if parentesco == "PADRE" else datetime(1990, 1, 1))
                    l_nac_p = st.text_input("Lugar Nacimiento Padre", value=l_nac_acu if parentesco == "PADRE" else "").upper()
                
                val_m_nom = nombre_acu if parentesco == "MADRE" else "" 
                val_m_id = id_acu if parentesco == "MADRE" else "" 
                val_m_doc = ["CC", "TI", "CE", "PPT"].index(tp_doc_acu) if parentesco == "MADRE" else 0

                with t2:
                    m_c1, m_c2 = st.columns(2)
                    nombre_m = m_c1.text_input("Nombre de la Madre", value=val_m_nom).upper()
                    id_m = m_c1.text_input("ID Madre", value=val_m_id)
                    tp_doc_m = m_c2.selectbox("Tipo Doc Madre", ["CC", "TI", "CE", "PPT"], index=val_m_doc)
                    f_nac_m = m_c2.date_input("Fecha Madre", value=f_nac_acu if parentesco == "MADRE" else datetime(1990, 1, 1))
                    l_nac_m = st.text_input("Lugar Madre", value=l_nac_acu if parentesco == "MADRE" else "").upper()
        else:
            nombre_p = id_p = tp_doc_p = f_nac_p = l_nac_p = "NO APLICA"
            nombre_m = id_m = tp_doc_m = f_nac_m = l_nac_m = "NO APLICA"
    else:
        nombre_acu = id_acu = tp_doc_acu = parentesco = f_nac_acu = l_nac_acu = "NO APLICA"
        nombre_p = id_p = tp_doc_p = f_nac_p = l_nac_p = nombre_m = id_m = tp_doc_m = f_nac_m = l_nac_m = "NO APLICA"

    # BOTÓN DE ADJUNTO (Novedad solicitada)
    st.markdown("---")
    st.subheader("📁 Documentos")
    archivo_adjunto = st.file_uploader("Subir documento del beneficiario", type=["pdf", "jpg", "png"])

    if st.button("💾 Guardar Registro Completo"):
        if not tipo_persona or not uca or not docente:
            st.error("⚠️ Faltan campos obligatorios.")
        else:
            nuevo = {
                "FECHA INGRESO": fecha_ingreso, "TIPO_PERSONA": tipo_persona, "NOMBRE PARTICIPANTE": nombre,
                "TIPO_DOC": tipo_doc, "ID PARTICIPANTE": id_niño, "LUGAR NACIMIENTO": lugar_nac,
                "FECHA NACIMIENTO": fecha_nac, "EDAD AL INGRESAR": calcular_edad_detallada(fecha_nac),
                "DIRECCION": direccion, "TELEFONO": telefono, "DISCAPACIDAD": discapacidad,
                "DOCENTE": docente, "UCA": uca, "ACUDIENTE": nombre_acu, "ID ACUDIENTE": id_acu,
                "TP_DOC_ACU": tp_doc_acu, "PARENTESCO": parentesco, "FECHA_NAC_ACU": f_nac_acu,
                "L_NAC_ACU": l_nac_acu, "NOMBRE PADRE": nombre_p, "ID PADRE": id_p, "TP_DOC_P": tp_doc_p,
                "F_NAC_P": f_nac_p, "L_NAC_P": l_nac_p, "NOMBRE MADRE": nombre_m, "ID MADRE": id_m,
                "TP_DOC_M": tp_doc_m, "F_NAC_M": f_nac_m, "L_NAC_M": l_nac_m,
                "ADJUNTO": archivo_adjunto.name if archivo_adjunto else "SIN ARCHIVO"
            }
            guardar_datos(nuevo, "INGRESOS")
            st.success("¡Registro guardado!")
            st.balloons()

# --- SECCIÓN: RETIRO ---
elif st.session_state.menu_opcion == "Retiro":
    st.header("🚶 Gestión de Retiros")
    try:
        df_ingresos = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="INGRESOS")
        try:
            df_ret_existentes = conn.read(spreadsheet=SPREADSHEET_URL, worksheet="RETIROS")
            ids_retirados = df_ret_existentes["ID"].astype(str).tolist()
        except:
            ids_retirados = []

        df_activos = df_ingresos[~df_ingresos["ID PARTICIPANTE"].astype(str).isin(ids_retirados)]

        if df_activos.empty:
            st.info("🎉 ¡No hay participantes activos!")
        else:
            seleccionado = st.selectbox("Escriba el nombre:", options=df_activos["NOMBRE PARTICIPANTE"].tolist(), index=None)
            if seleccionado:
                datos_niño = df_activos[df_activos["NOMBRE PARTICIPANTE"] == seleccionado].iloc[0]
                st.success(f"**Seleccionado:** {seleccionado}")
                motivo = st.selectbox("Motivo", ["Traslado", "Cumplimiento de Edad", "Retiro Voluntario", "Otro"], index=None)
                obs = st.text_area("Observaciones")
                if st.button("Confirmar Retiro", type="primary"):
                    if motivo:
                        datos_retiro = {
                            "FECHA RETIRO": datetime.now().strftime("%Y-%m-%d"),
                            "NOMBRE": seleccionado, "ID": datos_niño['ID PARTICIPANTE'],
                            "UCA": datos_niño['UCA'], "DOCENTE": datos_niño['DOCENTE'],
                            "MOTIVO": motivo, "OBSERVACIONES": obs
                        }
                        guardar_datos(datos_retiro, "RETIROS")
                        st.success("Retiro procesado.")
                        st.rerun()
    except:
        st.error("No se pudo cargar la base de datos.")

# --- SECCIÓN: LISTADO ---
elif st.session_state.menu_opcion == "Listado":
    st.header("📋 Base de Datos Completa")

    try:
        # 1. Leer INGRESOS
        df_ingresos = conn.read(
            spreadsheet=SPREADSHEET_URL,
            worksheet="INGRESOS"
        )

        if df_ingresos is None or df_ingresos.empty:
            st.warning("No hay registros aún.")
            st.stop()

        # 2. Leer RETIROS (si existe)
        try:
            df_retirados = conn.read(
                spreadsheet=SPREADSHEET_URL,
                worksheet="RETIROS"
            )

            ids_retirados = (
                df_retirados["ID"]
                .astype(str)
                .str.strip()
                .str.replace(".0", "", regex=False)
                .tolist()
            )

        except:
            ids_retirados = []

        # 3. Copia de trabajo
        df_mostrar = df_ingresos.copy()

        # --- LIMPIEZAS IMPORTANTES ---

        # ID PARTICIPANTE sin .000000
        df_mostrar["ID PARTICIPANTE"] = (
            df_mostrar["ID PARTICIPANTE"]
            .astype(str)
            .str.strip()
            .str.replace(".0", "", regex=False)
        )
        
        # TELEFONO sin .000000
        df_mostrar["TELEFONO"] = (
            df_mostrar["TELEFONO"]
            .astype(str)
            .str.replace(".0", "", regex=False)
        )

        # Recalcular consecutivo
        df_mostrar = df_mostrar.reset_index(drop=True)
        df_mostrar["N°"] = df_mostrar.index + 1

        # Edad actual
        df_mostrar["EDAD ACTUAL"] = pd.to_datetime(
            df_mostrar["FECHA NACIMIENTO"]
        ).apply(lambda x: calcular_edad_detallada(x.date()))

        # 4. Filtros
        f1, f2 = st.columns(2)
        busq = f1.text_input("🔍 Buscar Nombre o ID")
        uca_f = f2.multiselect(
            "Filtrar por UCA",
            sorted(df_mostrar["UCA"].dropna().unique())
        )

        if busq:
            df_mostrar = df_mostrar[
                df_mostrar["NOMBRE PARTICIPANTE"].str.contains(busq.upper(), na=False) |
                df_mostrar["ID PARTICIPANTE"].str.contains(busq)
            ]

        if uca_f:
            df_mostrar = df_mostrar[df_mostrar["UCA"].isin(uca_f)]

        # 5. Estilo de retirados
        def color_retiro(row):
            if row["ID PARTICIPANTE"] in ids_retirados:
                return ["background-color: #FFEBEE"] * len(row)
            return [""] * len(row)

        st.write("💡 *Las filas en rojo representan participantes retirados.*")

        st.dataframe(
            df_mostrar.style.apply(color_retiro, axis=1),
            use_container_width=True,
            height=600
        )

    except Exception as e:
        st.error(f"Error al cargar el listado: {e}")

        # Botón de descarga
        st.download_button(
            "📥 Descargar Base de Datos (CSV)", 
            df_mostrar.to_csv(index=False).encode('utf-8'), 
            "Base_Floresta.csv", 
            "text/csv"
        )

    except Exception as e:
        st.error(f"Error al cargar el listado: {e}")
        st.warning("Asegúrate de que la hoja 'INGRESOS' no esté vacía.")















