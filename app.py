import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import os
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="EIC La Floresta", layout="wide", page_icon="🎈")

# ==========================================
# 2. CONEXIÓN (Usa Secrets de Streamlit Cloud)
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

# --- SISTEMA DE ACCESO ---
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

# ==========================================
# 3. LISTAS DE REFERENCIA
# ==========================================
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
# ==========================================
# 4. FUNCIONES DE LÓGICA
# ==========================================
def calcular_edad_detallada(fecha_nac):
    if not fecha_nac: return "N/A"
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
    try:
        nuevo_df = pd.DataFrame([nuevo_dict])
        try:
            df_actual = conn.read(worksheet=nombre_hoja, ttl=0)
        except:
            df_actual = pd.DataFrame()

        if df_actual is None or df_actual.empty:
            nuevo_df.insert(0, "N°", 1)
            df_final = nuevo_df
        else:
            consecutivo = len(df_actual) + 1
            nuevo_df.insert(0, "N°", consecutivo)
            df_final = pd.concat([df_actual, nuevo_df], ignore_index=True)

        conn.update(worksheet=nombre_hoja, data=df_final)
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# ==========================================
# 5. MENÚ LATERAL Y CRÉDITOS
# ==========================================
if 'menu_opcion' not in st.session_state:
    st.session_state.menu_opcion = "Inicio"

with st.sidebar:
    st.markdown("## 🎈 MI FLORESTA")
    if st.button("🏠 Inicio Feliz", use_container_width=True): st.session_state.menu_opcion = "Inicio"
    if st.button("👶 Nuevo Registro", use_container_width=True): st.session_state.menu_opcion = "Ingreso"
    if st.button("👋 Retirar Participante", use_container_width=True): st.session_state.menu_opcion = "Retiro"
    if st.button("📚 Ver Base de Datos", use_container_width=True): st.session_state.menu_opcion = "Listado"
    
    st.markdown("---")
    st.markdown("### 🛠️ Soporte Técnico")
    st.info("**Desarrollado por:**\n\nIng. Oscar Sánchez Pérez")
    st.caption("© 2026 LA FLORESTA - Versión Cloud Full")
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo: 
    if os.path.exists("EIC.jpg"): st.image("EIC.jpg", width=120)
with col_titulo: 
    st.title("Hogar Infantil La Floresta")
    st.subheader("Asociación de Padres de Familia")

# ==========================================
# 7. MÓDULOS DE LA APLICACIÓN
# ==========================================

# --- MÓDULO: INICIO ---
if st.session_state.menu_opcion == "Inicio":
    st.header("📊 Tablero de Control")
    try:
        df_ing = conn.read(worksheet="INGRESOS", ttl=0)
        try:
            df_ret = conn.read(worksheet="RETIROS", ttl=0)
            count_ret = len(df_ret)
        except:
            count_ret = 0
            
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Histórico", len(df_ing))
        c2.metric("Retiros Registrados", count_ret)
        c3.metric("Estado", "Conectado 🟢")
        
        if not df_ing.empty:
            st.subheader("Población Activa por UCA")
            st.bar_chart(df_ing["UCA"].value_counts())
    except:
        st.info("No hay datos disponibles para estadísticas.")

# --- MÓDULO: INGRESO (COMPLETO) ---
elif st.session_state.menu_opcion == "Ingreso":
    st.header("📝 Nuevo Registro de Participante")
    with st.form("form_ingreso", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            t_persona = st.selectbox("Tipo", ["NIÑO", "NIÑA", "MADRE GESTANTE"])
            nombre = st.text_input("Nombre Completo").upper()
            t_doc = st.selectbox("Documento", ["RC", "CC", "TI", "PPT"])
        with col2:
            n_doc = st.text_input("N° Identificación")
            f_nac = st.date_input("Fecha Nacimiento", value=datetime(2020, 1, 1))
            l_nac = st.text_input("Lugar Nacimiento").upper()
        with col3:
            uca = st.selectbox("UCA", options=lista_ucas)
            docente = st.selectbox("Docente", options=lista_docentes)
            f_ing = st.date_input("Fecha Ingreso")
            
        st.markdown("---")
        col4, col5 = st.columns(2)
        direccion = col4.text_input("Dirección", value="KDX ").upper()
        telefono = col5.text_input("Teléfono")
        
        st.subheader("👨‍👩‍👧 Datos del Acudiente")
        acudiente = st.text_input("Nombre del Responsable").upper()
        id_acu = st.text_input("Cédula Responsable")
        
        if st.form_submit_button("💾 Guardar Ingreso"):
            if not nombre or not n_doc:
                st.error("Nombre y Documento son obligatorios")
            else:
                datos = {
                    "FECHA INGRESO": str(f_ing), "TIPO_PERSONA": t_persona, "NOMBRE PARTICIPANTE": nombre,
                    "TIPO_DOC": t_doc, "ID PARTICIPANTE": n_doc, "LUGAR NACIMIENTO": l_nac,
                    "FECHA NACIMIENTO": str(f_nac), "EDAD AL INGRESAR": calcular_edad_detallada(f_nac),
                    "DIRECCION": direccion, "TELEFONO": telefono, "DOCENTE": docente, "UCA": uca,
                    "ACUDIENTE": acudiente, "ID ACUDIENTE": id_acu
                }
                if guardar_datos(datos, "INGRESOS"):
                    st.success(f"✅ {nombre} guardado correctamente.")

# --- MÓDULO: RETIRO (NUEVO Y COMPLETO) ---
elif st.session_state.menu_opcion == "Retiro":
    st.header("👋 Registro de Retiros")
    try:
        df_ingresos = conn.read(worksheet="INGRESOS", ttl=0)
        if not df_ingresos.empty:
            # Seleccionar participante de la lista existente
            opciones = df_ingresos["NOMBRE PARTICIPANTE"].tolist()
            seleccion = st.selectbox("Seleccione el participante a retirar:", opciones, index=None)
            
            if seleccion:
                fila = df_ingresos[df_ingresos["NOMBRE PARTICIPANTE"] == seleccion].iloc[0]
                st.warning(f"Va a retirar a: {seleccion} (ID: {fila['ID PARTICIPANTE']})")
                
                with st.form("form_retiro"):
                    f_ret = st.date_input("Fecha de Retiro")
                    motivo = st.selectbox("Motivo del Retiro", ["CAMBIO DE DOMICILIO", "TRANSICIÓN A COLEGIO", "VOLUNTARIO", "OTRO"])
                    obs = st.text_area("Observaciones adicionales")
                    
                    if st.form_submit_button("❌ Confirmar Retiro"):
                        datos_ret = {
                            "FECHA RETIRO": str(f_ret),
                            "ID": str(fila["ID PARTICIPANTE"]),
                            "NOMBRE": seleccion,
                            "MOTIVO": motivo,
                            "OBSERVACIONES": obs
                        }
                        if guardar_datos(datos_ret, "RETIROS"):
                            st.success("Retiro registrado correctamente.")
        else:
            st.info("No hay participantes registrados para retirar.")
    except:
        st.error("Error al cargar datos para retiros.")

# --- MÓDULO: LISTADO (CON CRUCE DE RETIRADOS) ---
elif st.session_state.menu_opcion == "Listado":
    st.header("📋 Base de Datos General")
    try:
        df_mostrar = conn.read(worksheet="INGRESOS", ttl=0)
        try:
            df_ret = conn.read(worksheet="RETIROS", ttl=0)
            ids_retirados = df_ret["ID"].astype(str).tolist()
        except:
            ids_retirados = []

        if not df_mostrar.empty:
            # Buscador
            busq = st.text_input("🔍 Buscar por Nombre o ID")
            if busq:
                df_mostrar = df_mostrar[df_mostrar.astype(str).apply(lambda x: busq.upper() in x.str.upper().values, axis=1)]
            
            # Función para resaltar retirados en rojo suave
            def color_retiro(row):
                return ['background-color: #f8d7da' if str(row["ID PARTICIPANTE"]) in ids_retirados else '' for _ in row]

            st.write("Nota: Las filas en **rojo** son participantes ya retirados.")
            st.dataframe(df_mostrar.style.apply(color_retiro, axis=1), use_container_width=True)
            
            csv = df_mostrar.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", csv, "base_datos_floresta.csv", "text/csv")
    except:
        st.error("No se pudo cargar la base de datos.")















