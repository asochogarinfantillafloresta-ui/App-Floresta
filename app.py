import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import os
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="EIC La Floresta", layout="wide", page_icon="🎈")

# 2. CONEXIÓN A GOOGLE SHEETS
# Nota: La URL y credenciales se gestionan desde los Secrets de Streamlit Cloud
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

# --- LISTAS DE OPCIONES ---
lista_ucas = ["HUELLITAS DE ALEGRES", "HUELLITAS DE IGUALDAD", "HUELLITAS DE ESPERANZA", "HUELLITAS DE BONDAD", "HUELLITAS DE AMOR", "HUELLITAS DE AMISTAD", "HUELLITAS DE PAZ", "HUELLITAS DE COLORES", "HUELLITAS DE DIOS", "HUELLITAS DE PERDON", "HUELLITAS DE TENACIDAD", "HUELLITAS DE FELICIDAD", "ANGELITOS DE DIOS", "HUELLITAS DE FE", "HUELLITAS DE VALENTIA", "HUELLITAS DE ILUSION", "HUELLITAS DE FORTALEZA", "CARITAS ALEGRES", "HUELLITAS DE OPTIMISMO", "HUELLITAS DE SUPERACIÓN", "HUELLITAS DE LIBERTAD", "CARITAS FELICES", "HUELLITAS DE ESFUERZO"]
lista_docentes = ["YURLEIBY", "CLAUDIA MEDINA", "MARIA JOSE TRILLOS", "CLAUDIA DIAZ", "YENNY LOZANO", "MARIA JOSE BARBOSA", "VANNESA LOZANO", "ELIZABETH BOHORQUEZ", "ALVEIRO MEDINA", "YESSICA TRILLOS", "JUAN CAMILO", "MAYERLY DONADO", "AURELLY", "MONICA", "MARIA FERNANDA", "MARY LUZ", "MARLY TATIANA", "LEIDY BENAVIDEZ", "ANGELICA ROJAS", "ELAINE QUINTERO", "AIDA QUINTERO", "NANCY VERGEL", "YERLY PRADA"]
lista_tipo_doc = ["RC", "CC", "CE", "TI", "PPT", "SIN DOCUMENTO"]

# --- FUNCIONES ---
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

# --- NAVEGACIÓN ---
if 'menu_opcion' not in st.session_state:
    st.session_state.menu_opcion = "Inicio"

with st.sidebar:
    st.markdown("## 🎈 MI FLORESTA")
    if st.button("🏠 Inicio", use_container_width=True): st.session_state.menu_opcion = "Inicio"
    if st.button("👶 Nuevo Ingreso", use_container_width=True): st.session_state.menu_opcion = "Ingreso"
    if st.button("👋 Retiro", use_container_width=True): st.session_state.menu_opcion = "Retiro"
    if st.button("📚 Base de Datos", use_container_width=True): st.session_state.menu_opcion = "Listado"
    st.markdown("---")
    st.info("**Desarrollado por:**\n\nIng. Oscar Sánchez Pérez")
    if st.button("🚪 Salir"):
        st.session_state.autenticado = False
        st.rerun()

# --- ENCABEZADO ---
col_logo, col_titulo = st.columns([1, 4])
with col_logo: 
    if os.path.exists("EIC.jpg"): st.image("EIC.jpg", width=120)
with col_titulo: 
    st.title("Hogar Infantil La Floresta")
    st.subheader("Asociación de Padres de Familia")

# --- MÓDULO: INICIO ---
if st.session_state.menu_opcion == "Inicio":
    st.header("📊 Resumen de Control")
    try:
        df_ing = conn.read(worksheet="INGRESOS", ttl=0)
        st.metric("Total Participantes en Base", len(df_ing))
        st.subheader("Distribución por UCA")
        st.bar_chart(df_ing["UCA"].value_counts())
    except:
        st.info("Iniciando sistema... No hay datos registrados.")

# --- MÓDULO: INGRESO ---
elif st.session_state.menu_opcion == "Ingreso":
    st.header("📝 Formulario de Registro")
    with st.form("registro_final"):
        col1, col2, col3 = st.columns(3)
        with col1:
            t_persona = st.selectbox("Tipo de Participante", ["NIÑO", "NIÑA", "MADRE GESTANTE"])
            nombre = st.text_input("Nombre Completo").upper()
            t_doc = st.selectbox("Tipo de Documento", options=lista_tipo_doc)
            n_doc = st.text_input("Número de Documento")
        with col2:
            f_nac = st.date_input("Fecha de Nacimiento", value=datetime(2020, 1, 1))
            l_nac = st.text_input("Lugar de Nacimiento").upper()
            f_ing = st.date_input("Fecha de Ingreso")
            uca = st.selectbox("UCA", options=lista_ucas)
        with col3:
            docente = st.selectbox("Docente Encargado", options=lista_docentes)
            telefono = st.text_input("Número de Teléfono")
            discapacidad = st.radio("¿Tiene Discapacidad?", ["NO", "SI"], horizontal=True)

        direccion = st.text_input("Dirección de Residencia", value="KDX ").upper()

        st.subheader("👨‍👩‍👧 Información Familiar")
        f_col1, f_col2 = st.columns(2)
        nombre_m = f_col1.text_input("Nombre de la Madre").upper()
        id_m = f_col1.text_input("Cédula de la Madre")
        nombre_p = f_col2.text_input("Nombre del Padre").upper()
        id_p = f_col2.text_input("Cédula del Padre")
        
        acudiente = st.text_input("Nombre del Acudiente / Responsable").upper()
        parentesco = st.selectbox("Parentesco del Acudiente", ["MADRE", "PADRE", "ABUELOS", "TIOS", "OTRO"])

        if st.form_submit_button("💾 Guardar Registro"):
            if not nombre or not n_doc:
                st.error("⚠️ Nombre y Documento son obligatorios.")
            else:
                datos = {
                    "FECHA INGRESO": str(f_ing), "TIPO_PERSONA": t_persona, "NOMBRE PARTICIPANTE": nombre,
                    "TIPO_DOC": t_doc, "ID PARTICIPANTE": n_doc, "LUGAR NACIMIENTO": l_nac,
                    "FECHA NACIMIENTO": str(f_nac), "EDAD AL INGRESAR": calcular_edad_detallada(f_nac),
                    "DIRECCION": direccion, "TELEFONO": telefono, "DISCAPACIDAD": discapacidad,
                    "DOCENTE": docente, "UCA": uca, "NOMBRE MADRE": nombre_m, "ID MADRE": id_m,
                    "NOMBRE PADRE": nombre_p, "ID PADRE": id_p, "ACUDIENTE": acudiente, "PARENTESCO": parentesco
                }
                if guardar_datos(datos, "INGRESOS"):
                    st.success(f"✅ ¡{nombre} registrado con éxito!")
                    st.balloons()

# --- MÓDULO: RETIRO ---
elif st.session_state.menu_opcion == "Retiro":
    st.header("👋 Registro de Retiros")
    try:
        df_ing = conn.read(worksheet="INGRESOS", ttl=0)
        seleccion = st.selectbox("Seleccione al participante a retirar:", df_ing["NOMBRE PARTICIPANTE"].tolist(), index=None)
        if seleccion:
            fila = df_ing[df_ing["NOMBRE PARTICIPANTE"] == seleccion].iloc[0]
            with st.form("form_retiro"):
                f_ret = st.date_input("Fecha de Retiro")
                motivo = st.selectbox("Motivo del Retiro", ["CAMBIO DE DOMICILIO", "INGRESO A COLEGIO", "VOLUNTARIO", "OTRO"])
                obs = st.text_area("Observaciones")
                if st.form_submit_button("Confirmar Retiro"):
                    datos_r = {
                        "FECHA RETIRO": str(f_ret), 
                        "ID": str(fila["ID PARTICIPANTE"]), 
                        "NOMBRE": seleccion, 
                        "MOTIVO": motivo,
                        "OBS": obs
                    }
                    if guardar_datos(datos_r, "RETIROS"):
                        st.success("Retiro registrado en la base de datos.")
    except: st.warning("No hay datos disponibles para procesar retiros.")

# --- MÓDULO: LISTADO ---
elif st.session_state.menu_opcion == "Listado":
    st.header("📋 Base de Datos de Participantes")
    try:
        df_i = conn.read(worksheet="INGRESOS", ttl=0)
        try:
            df_r = conn.read(worksheet="RETIROS", ttl=0)
            ids_r = df_r["ID"].astype(str).tolist()
        except: ids_r = []
        
        busq = st.text_input("🔍 Buscar por Nombre o Cédula")
        if busq:
            df_i = df_i[df_i.astype(str).apply(lambda x: busq.upper() in x.str.upper().values, axis=1)]

        def color_retiro(row):
            return ['background-color: #f8d7da' if str(row["ID PARTICIPANTE"]) in ids_r else '' for _ in row]

        st.write("💡 *Las filas en rojo representan participantes ya retirados.*")
        st.dataframe(df_i.style.apply(color_retiro, axis=1), use_container_width=True)
        
        csv = df_i.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Base Completa (CSV)", csv, "base_la_floresta.csv", "text/csv")
    except: st.error("No se pudo conectar con la base de datos de Google Sheets.")
