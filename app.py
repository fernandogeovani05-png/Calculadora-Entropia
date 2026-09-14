import math
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Calculadora de Entropía - Edición Pro",
    page_icon="✨",
    layout="wide",
)

# --- Estilos CSS personalizados para un look más moderno ---
st.markdown(
    """
    <style>
    /* Estilo para el título principal */
    h1.main-title {
        color: #1E88E5;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        padding-bottom: 1rem;
    }
    /* Estilo para los subtítulos */
    h2.sub-title {
        color: #424242;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 500;
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    /* Estilo para las métricas destacadas (tarjetas) */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Encabezado con estilo moderno ---
st.markdown('<h1 class="main-title">Calculadora de Cuantificación y Entropía</h1>', unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; font-size: 1.2rem; color: #666; padding-bottom: 2rem;">
        Ingresa o edita los valores de <b>t (nivel)</b> y <b>f (frecuencia)</b> en la tabla interactiva.<br>
        La aplicación calculará probabilidades, entropía y generará un gráfico interactivo al instante.
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Sección de Entrada de Datos (Tabla Interactiva) ---
st.markdown('<h2 class="sub-title">1. Entrada de Datos Manual</h2>', unsafe_allow_html=True)

# Definir columnas iniciales y algunos datos de ejemplo limpios
datos_iniciales = pd.DataFrame({"t": [0.00125, 0.00250], "f": [100.0, 123.0]})

# Usar columns para centrar la tabla un poco y darle mejor aspecto
col_tabla1, col_tabla2, col_tabla3 = st.columns([1, 6, 1])
with col_tabla2:
    df_editado = st.data_editor(
        datos_iniciales,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_datos",
    )

# --- Sección de Resultados ---
st.markdown('<h2 class="sub-title">2. Resultados y Análisis Visual</h2>', unsafe_allow_html=True)

# Botón principal de cálculo con estilo
if st.button("⚡ Calcular Análisis Completo", type="primary", use_container_width=True):
    try:
        # Validaciones de entrada
        df_editado.columns = [str(col).strip().lower() for col in df_editado.columns]

        if "t" not in df_editado.columns or "f" not in df_editado.columns:
            st.error("Error: La tabla debe contener las columnas exactas 't' y 'f'.")
            st.stop()

        t = pd.to_numeric(df_editado["t"], errors="coerce")
        f = pd.to_numeric(df_editado["f"], errors="coerce")

        if t.isnull().any() or f.isnull().any():
            st.error("Error: Todas las celdas deben contener números válidos.")
            st.stop()

        suma_f = f.sum()

        if suma_f == 0:
            st.error("Error: La suma de las frecuencias (f) no puede ser cero.")
            st.stop()
        else:
            # --- Cálculos ---
            probabilidades = f / suma_f
            df_editado["Probabilidad P(i)"] = probabilidades

            entropia_total = 0.0
            for p in probabilidades:
                if p > 0:
                    entropia_total -= p * math.log2(p)

            st.success("¡Análisis generado correctamente!")

            # --- Diseño Moderno de Resultados ---

            # Fila 1: Métricas clave en tarjetas estilizadas
            st.markdown("### Métricas Globales")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Suma Total de Frecuencias (F)", value=f"{suma_f:,}")
            with m2:
                st.metric(label="Entropía Total del Sistema (H)", value=f"{entropia_total:.6f} bits", delta_color="off")
            with m3:
                # Otra métrica interesante: Número de niveles activos
                st.metric(label="Número de Niveles Distintos", value=len(df_editado))

            st.markdown("<hr>", unsafe_allow_html=True) # Línea divisoria moderna

            # Fila 2: Gráfico Interactivo y Tabla
            st.markdown("### Visualización y Tabla Detallada")
            c1, c2 = st.columns([2, 3]) # Gráfico más pequeño que la tabla

            with c1:
                # Gráfico circular moderno usando Plotly
                fig = px.pie(
                    df_editado,
                    values='f',
                    names='t',
                    title='Distribución de Frecuencias por Nivel (t)',
                    hole=0.4, # Estilo 'donut' moderno
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_traces(textinfo='percent+label')
                fig.update_layout(title_x=0.5, showlegend=False) # Título centrado, leyenda oculta
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                # Tabla de resultados final con formato numérico
                st.dataframe(
                    df_editado.style.format({'t': '{:.6f}', 'f': '{:.1f}', 'Probabilidad P(i)': '{:.6f}'}),
                    use_container_width=True
                )

    except Exception as e:
        st.error(f"Ocurrió un error inesperado durante el cálculo: {e}")