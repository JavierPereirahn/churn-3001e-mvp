from pathlib import Path
from html import escape
from textwrap import dedent
import re
import subprocess
import sys

from PIL import Image
import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
st.set_page_config(
    page_title="Panel de Riesgo de Churn (MVP)",
    page_icon="N",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');

/* ================================
   PALETA NOVANET
================================ */
:root {
    --azul-principal: #101B4D;
    --azul-secundario: #16245F;
    --naranja: #F5A623;
    --naranja-oscuro: #E69500;
    --blanco: #FFFFFF;
    --gris-fondo: #F5F7FB;
    --gris-borde: #DCE3EE;
    --texto: #1F2A44;
    --texto-secundario: #5F6B7A;
    --verde-ok: #16A34A;
    --rojo-error: #DC2626;
}

/* Fondo general */
.stApp {
    background: linear-gradient(180deg, #F5F7FB 0%, #EEF2F9 100%);
    color: var(--texto);
}

/* Contenedor principal */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
    max-width: 1450px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101B4D 0%, #16245F 100%);
    border-right: 2px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stCheckbox label {
    color: white !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
}

/* Títulos */
h1 {
    color: var(--azul-principal) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

h2, h3 {
    color: var(--azul-principal) !important;
    font-weight: 700 !important;
}

.small-note {
    color: var(--texto-secundario);
    font-size: 0.92rem;
}

/* Badge superior */
.badge-brand {
    display: inline-block;
    padding: 0.40rem 0.85rem;
    border-radius: 999px;
    background: linear-gradient(90deg, #101B4D 0%, #16245F 100%);
    color: white;
    font-weight: 700;
    font-size: 0.86rem;
    margin-bottom: 0.8rem;
}

/* Hero */
.hero-box {
    background: linear-gradient(90deg, #101B4D 0%, #16245F 100%);
    color: white;
    padding: 1.2rem 1.4rem;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(16, 27, 77, 0.18);
    margin-bottom: 1rem;
}

.hero-box h2 {
    color: white !important;
    margin-bottom: 0.2rem;
}

.hero-box p {
    color: rgba(255,255,255,0.88) !important;
    margin-bottom: 0;
}

/* Tarjetas */
.metric-card,
.section-card {
    background: var(--blanco);
    padding: 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid var(--gris-borde);
    box-shadow: 0 6px 18px rgba(16, 27, 77, 0.08);
}

/* Métricas */
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #DCE3EE;
    padding: 16px 18px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(16, 27, 77, 0.06);
}

div[data-testid="metric-container"] label {
    color: #5F6B7A !important;
    font-weight: 600;
}

div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #101B4D !important;
    font-weight: 800;
}

/* Botones */
.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #F5A623 0%, #E69500 100%);
    color: #101B4D !important;
    font-weight: 700;
    border: none;
    border-radius: 999px;
    padding: 0.55rem 1.15rem;
    box-shadow: 0 4px 14px rgba(245, 166, 35, 0.30);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(90deg, #FFB433 0%, #F5A623 100%);
    color: #101B4D !important;
    transform: translateY(-1px);
}

/* Expander */
details {
    background: #FFFFFF;
    border: 1px solid #DCE3EE;
    border-radius: 16px;
    padding: 0.4rem 0.7rem;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #DCE3EE;
    box-shadow: 0 4px 12px rgba(16, 27, 77, 0.05);
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Selectbox general */
div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid #DCE3EE !important;
}

/* Separadores */
hr {
    border: none;
    border-top: 1px solid #DCE3EE;
    margin: 1.2rem 0;
}

/* Caja del detalle */
.client-box {
    background: #FFFFFF;
    border: 1px solid #DCE3EE;
    border-left: 6px solid #F5A623;
    border-radius: 18px;
    padding: 1rem 1rem 0.85rem 1rem;
    box-shadow: 0 6px 18px rgba(16, 27, 77, 0.06);
}

.info-card {
    background: #FFF8EC;
    border: 1px solid #F5D28A;
    border-radius: 16px;
    padding: 0.9rem 1rem;
    color: #7A5312;
    font-weight: 600;
}

/* Títulos con iconos */
.section-title {
    display: flex;
    align-items: center;
    gap: 0.70rem;
    color: var(--azul-principal);
    font-weight: 800;
    font-size: 1.75rem;
    margin-top: 0.6rem;
    margin-bottom: 0.9rem;
}

.section-title-sm {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    color: var(--azul-principal);
    font-weight: 800;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    margin-bottom: 0.7rem;
}

.icon-badge {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #F5A623 0%, #E69500 100%);
    color: #101B4D;
    box-shadow: 0 6px 16px rgba(245, 166, 35, 0.28);
    font-size: 1rem;
}

.icon-badge-dark {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(90deg, #101B4D 0%, #16245F 100%);
    color: white;
    box-shadow: 0 6px 16px rgba(16, 27, 77, 0.20);
    font-size: 0.95rem;
}

.sidebar-title {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-weight: 800;
    font-size: 1.1rem;
    margin-bottom: 0.6rem;
    color: white;
}

.sidebar-title i {
    color: #F5A623;
}

.exec-card {
    background: #FFFFFF;
    border: 1px solid #DCE3EE;
    border-left: 6px solid #101B4D;
    border-radius: 18px;
    padding: 1rem 1rem 0.9rem 1rem;
    box-shadow: 0 6px 18px rgba(16, 27, 77, 0.06);
    margin-bottom: 1rem;
}

.exec-note {
    color: #5F6B7A;
    font-size: 0.95rem;
}

.upload-card {
    background: #FFFFFF;
    border: 1px solid #DCE3EE;
    border-left: 6px solid #F5A623;
    border-radius: 18px;
    padding: 1rem 1rem 0.9rem 1rem;
    box-shadow: 0 6px 18px rgba(16, 27, 77, 0.06);
    margin-bottom: 1rem;
}

.log-box {
    background: #0B1029;
    color: #DCE7FF;
    border-radius: 14px;
    padding: 0.9rem;
    border: 1px solid #233067;
    font-family: Consolas, monospace;
    font-size: 0.84rem;
    white-space: pre-wrap;
    max-height: 380px;
    overflow-y: auto;
}

/* Dialog / modal */
div[data-testid="stDialog"] div[role="dialog"] {
    border-radius: 24px !important;
    border: 1px solid #DCE3EE !important;
    box-shadow: 0 20px 60px rgba(16, 27, 77, 0.18) !important;
}

.dialog-alert-icon-wrap {
    text-align: center;
    margin-top: 0.2rem;
    margin-bottom: 0.9rem;
}

.dialog-alert-icon {
    width: 78px;
    height: 78px;
    margin: 0 auto;
    border-radius: 50%;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    font-weight: 800;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}

.dialog-alert-title {
    text-align: center;
    font-size: 30px;
    font-weight: 800;
    color: #101B4D;
    margin-bottom: 10px;
}

.dialog-alert-text {
    text-align: center;
    font-size: 16px;
    line-height: 1.55;
    color: #475569;
    margin-bottom: 8px;
}

p {
    color: #1F2A44;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="badge-brand">NovaNet • MVP de predicción de churn</div>', unsafe_allow_html=True)

# =========================================================
# RUTAS DEL PROYECTO
# =========================================================
project_root = Path(__file__).resolve().parent

data_raw_path = project_root / "data" / "raw"
data_exports_path = project_root / "data" / "exports"
outputs_tables_path = project_root / "outputs" / "tables"
outputs_figures_path = project_root / "outputs" / "figures"
reports_path = project_root / "reports"
notebooks_path = project_root / "notebooks"

data_raw_path.mkdir(parents=True, exist_ok=True)

full_scored_path = data_exports_path / "clientes_scoreados_completos.csv"
top10_path = data_exports_path / "top10_clientes_riesgo.csv"
top25_path = data_exports_path / "top25_clientes_riesgo.csv"

baseline_metrics_path = outputs_tables_path / "tabla_metricas_baseline.csv"
model_metrics_path = outputs_tables_path / "tabla_metricas_modelo.csv"
comparison_path = outputs_tables_path / "comparativa_baseline_vs_modelo.csv"
improvement_path = outputs_tables_path / "mejora_relativa_baseline_vs_modelo.csv"
checklist_path = outputs_tables_path / "checklist_validacion_mvp.csv"

shap_summary_path = outputs_figures_path / "shap_summary.png"
shap_bar_path = outputs_figures_path / "shap_bar.png"

summary_md_path = reports_path / "resumen_resultados.md"

notebook_input_path = notebooks_path / "01_experimento_final.ipynb"
notebook_output_path = notebooks_path / "01_experimento_final_ejecutado.ipynb"

INTERNAL_DATASET_FILENAME = "input_dataset.csv"
internal_dataset_path = data_raw_path / INTERNAL_DATASET_FILENAME

EXPECTED_TELCO_COLUMNS = [
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
]

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
def load_csv_if_exists(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def load_text_if_exists(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Archivo no encontrado."

def estilo_riesgo(valor: str) -> str:
    valor = str(valor).upper()
    if valor == "ALTO":
        return "🔴 ALTO"
    if valor == "MEDIO":
        return "🟠 MEDIO"
    return "🟢 BAJO"

def format_probability(value):
    try:
        return f"{float(value):.2%}"
    except Exception:
        return value

filter_value_maps = {
    "nivel_riesgo": {
        "ALTO": "Alto",
        "MEDIO": "Medio",
        "BAJO": "Bajo"
    },
    "Contract": {
        "Month-to-month": "Mes a mes",
        "One year": "Un año",
        "Two year": "Dos años"
    },
    "InternetService": {
        "DSL": "DSL",
        "Fiber optic": "Fibra óptica",
        "No": "Sin internet"
    },
    "PaymentMethod": {
        "Electronic check": "Cheque electrónico",
        "Mailed check": "Cheque por correo",
        "Bank transfer (automatic)": "Transferencia bancaria automática",
        "Credit card (automatic)": "Tarjeta de crédito automática"
    }
}

def translate_filter_value(column_name, raw_value):
    return filter_value_maps.get(column_name, {}).get(raw_value, raw_value)

def get_filter_options(df, column_name):
    raw_values = sorted(df[column_name].dropna().astype(str).unique().tolist())
    display_values = ["Todos"] + [translate_filter_value(column_name, value) for value in raw_values]

    reverse_map = {
        translate_filter_value(column_name, value): value
        for value in raw_values
    }

    return display_values, reverse_map

def validar_archivos_necesarios():
    archivos = {
        "clientes_scoreados_completos.csv": full_scored_path.exists(),
        "top10_clientes_riesgo.csv": top10_path.exists(),
        "top25_clientes_riesgo.csv": top25_path.exists(),
        "tabla_metricas_baseline.csv": baseline_metrics_path.exists(),
        "tabla_metricas_modelo.csv": model_metrics_path.exists(),
        "comparativa_baseline_vs_modelo.csv": comparison_path.exists(),
        "mejora_relativa_baseline_vs_modelo.csv": improvement_path.exists(),
        "checklist_validacion_mvp.csv": checklist_path.exists(),
        "shap_summary.png": shap_summary_path.exists(),
        "shap_bar.png": shap_bar_path.exists(),
        "resumen_resultados.md": summary_md_path.exists(),
    }
    return archivos

def sanitize_filename(filename: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
    return safe_name or "uploaded_dataset.csv"

def validate_uploaded_dataset(uploaded_file):
    result = {
        "is_valid": False,
        "errors": [],
        "warnings": [],
        "df": pd.DataFrame(),
        "row_count": 0,
        "column_count": 0,
        "missing_columns": [],
    }

    if uploaded_file is None:
        result["errors"].append("No se recibió ningún archivo.")
        return result

    if not uploaded_file.name.lower().endswith(".csv"):
        result["errors"].append("El archivo debe tener extensión .csv")
        return result

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        result["errors"].append(f"No se pudo leer el CSV: {exc}")
        return result

    result["df"] = df
    result["row_count"] = len(df)
    result["column_count"] = len(df.columns)

    if df.empty:
        result["errors"].append("El archivo CSV está vacío.")
        return result

    missing_columns = [col for col in EXPECTED_TELCO_COLUMNS if col not in df.columns]
    result["missing_columns"] = missing_columns

    if missing_columns:
        result["errors"].append(
            "Faltan columnas obligatorias del esquema Telco Customer Churn: "
            + ", ".join(missing_columns)
        )

    if "Churn" not in df.columns:
        result["errors"].append("La columna 'Churn' es obligatoria.")
    else:
        churn_values = (
            df["Churn"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .unique()
            .tolist()
        )
        allowed_churn_values = {"yes", "no", "1", "0", "true", "false"}
        invalid_churn_values = sorted(set(churn_values) - allowed_churn_values)
        if invalid_churn_values:
            result["errors"].append(
                "La columna 'Churn' contiene valores no válidos: "
                + ", ".join(invalid_churn_values)
            )

    if "TotalCharges" in df.columns:
        total_charges_original = df["TotalCharges"].copy()
        total_charges_numeric = pd.to_numeric(total_charges_original, errors="coerce")
        invalid_totalcharges = int(
            total_charges_numeric.isna().sum() - total_charges_original.isna().sum()
        )
        if invalid_totalcharges > 0:
            result["warnings"].append(
                f"Se detectaron {invalid_totalcharges} valores no numéricos en 'TotalCharges'. "
                "El notebook los convertirá a nulos."
            )

    null_ratio = float(df.isna().mean().mean()) * 100
    if null_ratio > 5:
        result["warnings"].append(
            f"El dataset tiene {null_ratio:.2f}% de valores nulos en promedio."
        )

    if len(df) < 100:
        result["warnings"].append(
            "El dataset tiene menos de 100 filas; los resultados pueden ser poco estables."
        )

    if len(df) < 1000:
        result["warnings"].append(
            "El dataset es relativamente pequeño para una evaluación robusta."
        )

    result["is_valid"] = len(result["errors"]) == 0
    return result

def save_uploaded_dataset(uploaded_file, target_path: Path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_bytes(uploaded_file.getvalue())

ALERT_STYLES = {
    "success": {"color": "#16A34A", "icon": "✓"},
    "error": {"color": "#DC2626", "icon": "✕"},
    "warning": {"color": "#F59E0B", "icon": "!"},
    "info": {"color": "#2563EB", "icon": "i"},
}

def queue_pipeline_alert(alert_type="success", title="Proceso completado", text="Operación realizada correctamente."):
    st.session_state["_pipeline_alert"] = {
        "alert_type": alert_type,
        "title": title,
        "text": text
    }

@st.dialog("Notificación")
def render_pipeline_alert_dialog():
    alert = st.session_state.get("_pipeline_alert")

    if not alert:
        return

    style = ALERT_STYLES.get(alert["alert_type"], ALERT_STYLES["success"])
    title_safe = escape(str(alert["title"]))
    text_safe = escape(str(alert["text"]))

    st.markdown(
        dedent(
            f"""
            <div class="dialog-alert-icon-wrap">
                <div class="dialog-alert-icon" style="background:{style['color']};">
                    {style['icon']}
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="dialog-alert-title">{title_safe}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="dialog-alert-text">{text_safe}</div>',
        unsafe_allow_html=True
    )

    left_btn, center_btn, right_btn = st.columns([1, 1.4, 1])

    with center_btn:
        if st.button("Entendido", key="close_pipeline_alert", use_container_width=True):
            st.session_state.pop("_pipeline_alert", None)
            st.rerun()

def render_pipeline_alert():
    if "_pipeline_alert" in st.session_state:
        render_pipeline_alert_dialog()

def ejecutar_pipeline_completo(log_placeholder, dataset_filename: str):
    cmd = [
        sys.executable,
        "-m",
        "papermill",
        str(notebook_input_path),
        str(notebook_output_path),
        "-p",
        "dataset_filename",
        dataset_filename,
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=str(notebooks_path)
    )

    logs = []
    while True:
        line = process.stdout.readline()
        if line:
            logs.append(line.rstrip())
            log_placeholder.markdown(
                f'<div class="log-box">{"<br>".join(logs[-80:])}</div>',
                unsafe_allow_html=True
            )

        if process.poll() is not None:
            break

    remaining_output = process.stdout.read()
    if remaining_output:
        for extra_line in remaining_output.splitlines():
            logs.append(extra_line)

    log_placeholder.markdown(
        f'<div class="log-box">{"<br>".join(logs[-120:])}</div>',
        unsafe_allow_html=True
    )

    return process.returncode, logs

render_pipeline_alert()

# =========================================================
# HERO / ENCABEZADO
# =========================================================
st.markdown("""
<div class="hero-box">
    <h2>Panel de Riesgo de Churn (Top-N)</h2>
    <p>
        Interfaz interactiva del MVP basada en los artefactos generados por el notebook reproducible.
        Permite cargar y validar un dataset, ejecutar el pipeline completo, filtrar clientes,
        visualizar el ranking top-N, revisar el detalle del caso, consultar métricas
        y mostrar la explicabilidad global del modelo.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("Validación experimental con Telco Customer Churn; interfaz objetivo inspirada en el contexto operativo de NovaNet.")

# =========================================================
# CARGA Y VALIDACIÓN DEL DATASET
# =========================================================
st.markdown("""
<div class="section-title">
    <span class="icon-badge"><i class="fa-solid fa-file-arrow-up"></i></span>
    <span>Carga y validación del dataset</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="upload-card">
    <div class="exec-note">
        Paso 1. Sube un archivo CSV con la estructura esperada del dataset de churn.
        El sistema validará el archivo antes de habilitar la ejecución del pipeline.
        Internamente se guardará como <b>input_dataset.csv</b> en <b>data/raw</b>.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_dataset = st.file_uploader(
    "Sube el dataset CSV",
    type=["csv"],
    accept_multiple_files=False,
    help="El archivo debe seguir el esquema esperado de Telco Customer Churn."
)

dataset_ready_for_pipeline = False
validated_dataset_df = pd.DataFrame()
validated_dataset_name = None

if uploaded_dataset is not None:
    validation = validate_uploaded_dataset(uploaded_dataset)

    if validation["is_valid"]:
        save_uploaded_dataset(uploaded_dataset, internal_dataset_path)
        st.session_state["validated_dataset_filename"] = INTERNAL_DATASET_FILENAME
        st.session_state["validated_dataset_original_name"] = sanitize_filename(uploaded_dataset.name)

        dataset_ready_for_pipeline = True
        validated_dataset_df = validation["df"].copy()
        validated_dataset_name = uploaded_dataset.name

        st.success(
            f"Dataset válido. Archivo original: {uploaded_dataset.name}. "
            f"Se guardó internamente como {INTERNAL_DATASET_FILENAME}."
        )

        stats_col_1, stats_col_2, stats_col_3 = st.columns(3)
        stats_col_1.metric("Filas", validation["row_count"])
        stats_col_2.metric("Columnas", validation["column_count"])
        stats_col_3.metric("Archivo interno", INTERNAL_DATASET_FILENAME)

        if validation["warnings"]:
            for warning_msg in validation["warnings"]:
                st.warning(warning_msg)

        st.markdown("#### Vista previa del dataset")
        st.dataframe(validated_dataset_df.head(10), use_container_width=True, hide_index=True)
    else:
        st.session_state.pop("validated_dataset_filename", None)
        st.session_state.pop("validated_dataset_original_name", None)

        for error_msg in validation["errors"]:
            st.error(error_msg)

        if validation["warnings"]:
            for warning_msg in validation["warnings"]:
                st.warning(warning_msg)

        if not validation["df"].empty:
            st.markdown("#### Vista previa del archivo cargado")
            st.dataframe(validation["df"].head(10), use_container_width=True, hide_index=True)
else:
    st.info("Sube un archivo CSV válido para habilitar el pipeline.")

# =========================================================
# EJECUCIÓN DEL PIPELINE
# =========================================================
st.markdown("""
<div class="section-title">
    <span class="icon-badge"><i class="fa-solid fa-play"></i></span>
    <span>Ejecución del pipeline</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="exec-card">
    <div class="exec-note">
        Paso 2. Una vez validado el dataset, puedes ejecutar el notebook completo del experimento.
        El proceso regenerará métricas, artefactos, archivos CSV/Excel, resumen y visualizaciones SHAP.
    </div>
</div>
""", unsafe_allow_html=True)

run_col_1, run_col_2 = st.columns([1, 3])

with run_col_1:
    ejecutar_pipeline = st.button(
        "Ejecutar pipeline completo",
        use_container_width=True,
        disabled=not dataset_ready_for_pipeline
    )

with run_col_2:
    if dataset_ready_for_pipeline:
        st.caption(
            f"Dataset listo para pipeline: {validated_dataset_name} "
            f"→ {INTERNAL_DATASET_FILENAME}"
        )
    else:
        st.caption("Primero valida un archivo CSV correcto para habilitar esta acción.")

log_placeholder = st.empty()

if ejecutar_pipeline:
    if not notebook_input_path.exists():
        st.error("No se encontró el notebook principal en la ruta esperada.")
        st.stop()

    selected_dataset_filename = st.session_state.get("validated_dataset_filename")
    if not selected_dataset_filename:
        st.error("No hay dataset validado para ejecutar el pipeline.")
        st.stop()

    with st.spinner("Ejecutando notebook completo..."):
        return_code, logs = ejecutar_pipeline_completo(
            log_placeholder=log_placeholder,
            dataset_filename=selected_dataset_filename
        )

    if return_code == 0:
        queue_pipeline_alert(
            alert_type="success",
            title="Pipeline completado",
            text="El notebook terminó correctamente y la interfaz ya fue actualizada con los resultados nuevos."
        )
        st.rerun()
    else:
        queue_pipeline_alert(
            alert_type="error",
            title="Ejecución fallida",
            text="La ejecución del notebook falló. Revisa el log mostrado arriba para identificar el problema."
        )
        render_pipeline_alert()
        st.stop()

# =========================================================
# CARGA DE ARTEFACTOS
# =========================================================
archivos_estado = validar_archivos_necesarios()

full_scored_df = load_csv_if_exists(full_scored_path)
baseline_metrics_df = load_csv_if_exists(baseline_metrics_path)
model_metrics_df = load_csv_if_exists(model_metrics_path)
comparison_df = load_csv_if_exists(comparison_path)
improvement_df = load_csv_if_exists(improvement_path)
checklist_df = load_csv_if_exists(checklist_path)

summary_md = load_text_if_exists(summary_md_path)

# =========================================================
# VALIDACIÓN DE RESULTADOS
# =========================================================
if full_scored_df.empty:
    st.warning("Aún no hay artefactos generados o no se encontró `clientes_scoreados_completos.csv`.")
    st.info("Valida un dataset y luego ejecuta el pipeline completo desde la web.")
    st.stop()

required_cols = ["cliente_id", "probabilidad", "nivel_riesgo", "motivo_principal", "top_3_motivos"]
missing_cols = [col for col in required_cols if col not in full_scored_df.columns]

if missing_cols:
    st.error(f"Faltan columnas requeridas en clientes_scoreados_completos.csv: {missing_cols}")
    st.stop()

full_scored_df["probabilidad"] = pd.to_numeric(full_scored_df["probabilidad"], errors="coerce")
full_scored_df = full_scored_df.dropna(subset=["probabilidad"]).copy()
full_scored_df = full_scored_df.sort_values("probabilidad", ascending=False).reset_index(drop=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("""
<div class="sidebar-title">
    <i class="fa-solid fa-sliders"></i>
    <span>Configuración del panel</span>
</div>
""", unsafe_allow_html=True)

n_option = st.sidebar.selectbox(
    "Selecciona el tamaño del ranking (N)",
    options=[10, 25],
    index=0
)

nivel_riesgo_raw_values = sorted(
    full_scored_df["nivel_riesgo"].dropna().astype(str).unique().tolist()
)
nivel_riesgo_options = ["Todos"] + [translate_filter_value("nivel_riesgo", value) for value in nivel_riesgo_raw_values]
nivel_riesgo_reverse_map = {
    translate_filter_value("nivel_riesgo", value): value
    for value in nivel_riesgo_raw_values
}

selected_risk_level_display = st.sidebar.selectbox("Filtrar por nivel de riesgo", nivel_riesgo_options)
selected_risk_level = nivel_riesgo_reverse_map.get(selected_risk_level_display, selected_risk_level_display)

contract_options = ["Todos"]
contract_reverse_map = {}
if "Contract" in full_scored_df.columns:
    contract_options, contract_reverse_map = get_filter_options(full_scored_df, "Contract")
selected_contract_display = st.sidebar.selectbox("Filtrar por tipo de contrato", contract_options)
selected_contract = contract_reverse_map.get(selected_contract_display, selected_contract_display)

internet_options = ["Todos"]
internet_reverse_map = {}
if "InternetService" in full_scored_df.columns:
    internet_options, internet_reverse_map = get_filter_options(full_scored_df, "InternetService")
selected_internet_display = st.sidebar.selectbox("Filtrar por servicio de internet", internet_options)
selected_internet = internet_reverse_map.get(selected_internet_display, selected_internet_display)

payment_options = ["Todos"]
payment_reverse_map = {}
if "PaymentMethod" in full_scored_df.columns:
    payment_options, payment_reverse_map = get_filter_options(full_scored_df, "PaymentMethod")
selected_payment_display = st.sidebar.selectbox("Filtrar por método de pago", payment_options)
selected_payment = payment_reverse_map.get(selected_payment_display, selected_payment_display)

mostrar_shap = st.sidebar.checkbox("Mostrar explicabilidad SHAP", value=True)
mostrar_metricas = st.sidebar.checkbox("Mostrar métricas del modelo", value=True)
mostrar_checklist = st.sidebar.checkbox("Mostrar checklist MVP", value=True)

# =========================================================
# FILTROS
# =========================================================
filtered_df = full_scored_df.copy()

if selected_risk_level != "Todos":
    filtered_df = filtered_df[filtered_df["nivel_riesgo"].astype(str) == selected_risk_level]

if selected_contract != "Todos" and "Contract" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["Contract"].astype(str) == selected_contract]

if selected_internet != "Todos" and "InternetService" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["InternetService"].astype(str) == selected_internet]

if selected_payment != "Todos" and "PaymentMethod" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["PaymentMethod"].astype(str) == selected_payment]

filtered_df = filtered_df.sort_values("probabilidad", ascending=False).head(n_option).reset_index(drop=True)

if filtered_df.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

cliente_options = filtered_df["cliente_id"].astype(str).tolist()
selected_cliente_detail = st.selectbox(
    "Selecciona un cliente para ver el detalle",
    options=cliente_options,
    index=0
)

detail_df = filtered_df[filtered_df["cliente_id"].astype(str) == selected_cliente_detail].copy()
cliente_detalle = detail_df.iloc[0]

# =========================================================
# KPIS RÁPIDOS
# =========================================================
col_kpi_1, col_kpi_2, col_kpi_3, col_kpi_4 = st.columns(4)
col_kpi_1.metric("Clientes visibles", len(filtered_df))
col_kpi_2.metric("N seleccionado", n_option)
col_kpi_3.metric("Probabilidad promedio", f"{filtered_df['probabilidad'].mean():.2%}")
col_kpi_4.metric(
    "Riesgo alto",
    int((filtered_df["nivel_riesgo"].astype(str).str.upper() == "ALTO").sum())
)

# =========================================================
# LAYOUT PRINCIPAL
# =========================================================
left_col, right_col = st.columns([1.65, 1.0])

# =========================================================
# IZQUIERDA: TABLA TOP-N
# =========================================================
with left_col:
    st.markdown("""
    <div class="section-title">
        <span class="icon-badge"><i class="fa-solid fa-table-list"></i></span>
        <span>Lista priorizada (Top-N)</span>
    </div>
    """, unsafe_allow_html=True)

    display_df = filtered_df.copy()
    display_df["probabilidad"] = display_df["probabilidad"].apply(format_probability)

    if "nivel_riesgo" in display_df.columns:
        display_df["nivel_riesgo"] = display_df["nivel_riesgo"].apply(estilo_riesgo)

    rename_columns = {
        "cliente_id": "Cliente",
        "probabilidad": "Probabilidad",
        "nivel_riesgo": "Nivel de riesgo",
        "motivo_principal": "Motivo principal"
    }

    columnas_mostrar = [
        col for col in [
            "cliente_id",
            "probabilidad",
            "nivel_riesgo",
            "motivo_principal"
        ] if col in display_df.columns
    ]

    tabla_df = display_df[columnas_mostrar].rename(columns=rename_columns)

    st.dataframe(
        tabla_df,
        use_container_width=True,
        hide_index=True
    )

    csv_export = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar ranking filtrado (CSV)",
        data=csv_export,
        file_name=f"ranking_top_{n_option}_filtrado.csv",
        mime="text/csv"
    )

# =========================================================
# DERECHA: DETALLE CLIENTE
# =========================================================
with right_col:
    st.markdown("""
    <div class="section-title">
        <span class="icon-badge-dark"><i class="fa-solid fa-id-card"></i></span>
        <span>Detalle del cliente</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="client-box">', unsafe_allow_html=True)

    st.markdown(f"**Cliente:** {cliente_detalle.get('cliente_id', 'N/A')}")
    st.markdown(f"**Probabilidad churn:** {format_probability(cliente_detalle.get('probabilidad', 'N/A'))}")
    st.markdown(f"**Nivel de riesgo:** {estilo_riesgo(cliente_detalle.get('nivel_riesgo', 'N/A'))}")
    st.markdown(f"**Motivo principal:** {cliente_detalle.get('motivo_principal', 'N/A')}")

    st.markdown("""
    <div class="section-title-sm">
        <span class="icon-badge"><i class="fa-solid fa-magnifying-glass-chart"></i></span>
        <span>Top-3 motivos</span>
    </div>
    """, unsafe_allow_html=True)
    st.write(cliente_detalle.get("top_3_motivos", "N/A"))

    st.markdown("""
    <div class="section-title-sm">
        <span class="icon-badge"><i class="fa-solid fa-diagram-project"></i></span>
        <span>Variables del cliente</span>
    </div>
    """, unsafe_allow_html=True)

    variable_labels = {
        "Contract": "Tipo de contrato",
        "InternetService": "Servicio de internet",
        "PaymentMethod": "Método de pago",
        "tenure": "Antigüedad",
        "MonthlyCharges": "Cargo mensual",
        "TotalCharges": "Cargo acumulado"
    }

    vars_cliente = []
    for col in ["Contract", "InternetService", "PaymentMethod", "tenure", "MonthlyCharges", "TotalCharges"]:
        if col in cliente_detalle.index:
            etiqueta = variable_labels.get(col, col)
            valor_mostrado = cliente_detalle[col]
            if col in ["Contract", "InternetService", "PaymentMethod"]:
                valor_mostrado = translate_filter_value(col, str(cliente_detalle[col]))
            vars_cliente.append(f"**{etiqueta}:** {valor_mostrado}")

    if vars_cliente:
        st.markdown("  \n".join(vars_cliente))
    else:
        st.caption("No hay variables adicionales disponibles para este cliente.")

    st.markdown("""
    <div class="section-title-sm">
        <span class="icon-badge"><i class="fa-solid fa-phone-volume"></i></span>
        <span>Acción sugerida</span>
    </div>
    """, unsafe_allow_html=True)

    motivo_principal = str(cliente_detalle.get("motivo_principal", "")).lower()

    if "cargo" in motivo_principal or "precio" in motivo_principal:
        st.markdown('<div class="info-card">Sugerencia: llamada de retención con oferta o revisión del plan.</div>', unsafe_allow_html=True)
    elif "contrato" in motivo_principal:
        st.markdown('<div class="info-card">Sugerencia: contacto preventivo para fidelización o migración a un plan de mayor permanencia.</div>', unsafe_allow_html=True)
    elif "internet" in motivo_principal or "soporte" in motivo_principal or "seguridad" in motivo_principal:
        st.markdown('<div class="info-card">Sugerencia: validación técnica o acompañamiento del servicio.</div>', unsafe_allow_html=True)
    elif "antigüedad" in motivo_principal:
        st.markdown('<div class="info-card">Sugerencia: llamada preventiva y revisión comercial/técnica del caso.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-card">Sugerencia: llamada preventiva con revisión integral del caso.</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MÉTRICAS
# =========================================================
if mostrar_metricas:
    st.markdown("---")
    st.markdown("""
    <div class="section-title">
        <span class="icon-badge"><i class="fa-solid fa-chart-line"></i></span>
        <span>Métricas del modelo</span>
    </div>
    """, unsafe_allow_html=True)

    met_col_1, met_col_2 = st.columns(2)

    with met_col_1:
        st.markdown("""
        <div class="section-title-sm">
            <span class="icon-badge-dark"><i class="fa-solid fa-scale-balanced"></i></span>
            <span>Baseline vs Modelo</span>
        </div>
        """, unsafe_allow_html=True)
        if not comparison_df.empty:
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontró la tabla comparativa.")

    with met_col_2:
        st.markdown("""
        <div class="section-title-sm">
            <span class="icon-badge-dark"><i class="fa-solid fa-arrow-trend-up"></i></span>
            <span>Mejora relativa</span>
        </div>
        """, unsafe_allow_html=True)
        if not improvement_df.empty:
            st.dataframe(improvement_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No se encontró la tabla de mejora relativa.")

# =========================================================
# SHAP
# =========================================================
if mostrar_shap:
    st.markdown("---")
    st.markdown("""
    <div class="section-title">
        <span class="icon-badge"><i class="fa-solid fa-brain"></i></span>
        <span>Explicabilidad (SHAP)</span>
    </div>
    """, unsafe_allow_html=True)

    shap_col_1, shap_col_2 = st.columns(2)

    with shap_col_1:
        st.markdown("""
        <div class="section-title-sm">
            <span class="icon-badge-dark"><i class="fa-solid fa-chart-area"></i></span>
            <span>SHAP Summary</span>
        </div>
        """, unsafe_allow_html=True)
        if shap_summary_path.exists():
            shap_img_1 = Image.open(shap_summary_path)
            st.image(shap_img_1, use_container_width=True)
        else:
            st.warning("No se encontró shap_summary.png")

    with shap_col_2:
        st.markdown("""
        <div class="section-title-sm">
            <span class="icon-badge-dark"><i class="fa-solid fa-bars-progress"></i></span>
            <span>SHAP Bar Plot</span>
        </div>
        """, unsafe_allow_html=True)
        if shap_bar_path.exists():
            shap_img_2 = Image.open(shap_bar_path)
            st.image(shap_img_2, use_container_width=True)
        else:
            st.warning("No se encontró shap_bar.png")

# =========================================================
# CHECKLIST MVP
# =========================================================
if mostrar_checklist:
    st.markdown("---")
    st.markdown("""
    <div class="section-title">
        <span class="icon-badge"><i class="fa-solid fa-list-check"></i></span>
        <span>Checklist de validación del MVP</span>
    </div>
    """, unsafe_allow_html=True)

    if not checklist_df.empty:
        st.dataframe(checklist_df, use_container_width=True, hide_index=True)
    else:
        st.warning("No se encontró el checklist de validación.")

# =========================================================
# RESUMEN FINAL
# =========================================================
st.markdown("---")
st.markdown("""
<div class="section-title">
    <span class="icon-badge"><i class="fa-solid fa-file-lines"></i></span>
    <span>Resumen final del experimento</span>
</div>
""", unsafe_allow_html=True)

with st.expander("Ver resumen generado por el notebook"):
    st.markdown(summary_md)

# =========================================================
# ESTADO DE ARTEFACTOS
# =========================================================
st.markdown("---")
st.markdown("""
<div class="section-title">
    <span class="icon-badge"><i class="fa-solid fa-folder-tree"></i></span>
    <span>Estado de artefactos del MVP</span>
</div>
""", unsafe_allow_html=True)

estado_df = pd.DataFrame([
    {"archivo": nombre, "disponible": "Sí" if existe else "No"}
    for nombre, existe in archivos_estado.items()
])

st.dataframe(estado_df, use_container_width=True, hide_index=True)