# predecir_propina.py
import streamlit as st
import requests

# Diseño página
st.set_page_config(
    layout="centered",
)

# Estilos personalizados para el fondo y los colores de texto
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFFACD;  /* Amarillo tenue */
        color: black;  /* Texto en negro */
        font-family: 'Helvetica', sans-serif;  /* Fuente característica */
    }
    .stButton>button {
        background-color: green;
        color: white;
        font-family: 'Helvetica', sans-serif;
    }
    .stSelectbox label, .stNumberInput label {
        font-weight: bold;
        margin-bottom: 5px;
        color: black;
        font-family: 'Helvetica', sans-serif;
    }
    .block-container {
        padding-top: 20px;
    }
    .css-1lcbmhc {
        align-items: start;
    }
    .success-box {
        background-color: #ADD8E6;  /* Fondo celeste */
        color: black;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Helvetica', sans-serif;
    }
    .error-box {
        background-color: #FFA500;  /* Fondo naranjo */
        color: black;
        padding: 10px;
        border-radius: 5px;
        font-family: 'Helvetica', sans-serif;
    }
    .custom-title {
        font-size: 36px;
        font-weight: bold;
        color: blue;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        margin-top: 20px;  
    }
    .custom-subheader {
        font-size: 24px;
        color: blue;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        margin-bottom: 20px;
    }
    .footer-text {
        font-size: 12px;  /* Tamaño de fuente menor */
        text-align: right;  /* Alineado a la derecha */
        margin-top: 50px;  /* Espacio adicional hacia abajo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título y subtítulo utilizando HTML
st.markdown('<div class="custom-title">New York City Taxi Association</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subheader">Predicción de Propina según su viaje</div>', unsafe_allow_html=True)


description = "Datos requeridos:"
st.write(description)

# Layout 
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    pickup_weekday = st.selectbox(
        "Día de la Semana (Lunes a Domingo)",
        options=[0, 1, 2, 3, 4, 5, 6],
        format_func=lambda x: ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"][x]
    )
    work_hours = st.selectbox(
        "Horas Laborales (Sí, No)", 
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Sí"
    )
    passenger_count = st.selectbox(
        "Cantidad de Pasajeros", 
        options=list(range(1, 9))
    )
    trip_distance = st.number_input(
        "Distancia del Viaje (millas)", 
        min_value=0.0, step=1.0  # Incremento de a 1
    )

with col2:
    pickup_hour = st.selectbox(
        "Hora de Recogida (1-24 horas)", 
        options=list(range(24))
    )
    pickup_minute = st.selectbox(
        "Minuto de Recogida", 
        options=list(range(60))
    )
    trip_time = st.number_input(
        "Tiempo del Viaje (en minutos)", 
        min_value=0.0, step=1.0
    )
    trip_speed = st.number_input(
        "Velocidad Media del Viaje (en mph)", 
        min_value=0.0, step=1.0  # Incremento de a 1
    )

with col3:
    PULocationID = st.number_input(
        "Zona de Recogida (1-262)", 
        min_value=0, step=1
    )
    DOLocationID = st.number_input(
        "Zona de Destino (1-262)", 
        min_value=0, step=1
    )
    RatecodeID = st.number_input(
    "Código de Tarifa (1-7)", 
    min_value=1,
    max_value=7,
    step=1
)
    confidence = st.selectbox(
        "Umbral de Confianza (0.1 a 1.0)", 
        options=[round(x * 0.1, 1) for x in range(0, 11)]
    )

# Botón
if st.button("Predecir Propina"):
    features = {
        "pickup_weekday": pickup_weekday,
        "pickup_hour": pickup_hour,
        "work_hours": work_hours,
        "pickup_minute": pickup_minute,
        "passenger_count": passenger_count,
        "trip_distance": trip_distance,
        "trip_time": trip_time,
        "trip_speed": trip_speed,
        "PULocationID": PULocationID,
        "DOLocationID": DOLocationID,
        "RatecodeID": RatecodeID,
    }
   
    # Solicitud al backend
    response = requests.post(
        "https://matiasbunsterraby--predecir-propina-fastapi-app.modal.run/predict",  # URL de Modal
        json=features, 
        params={"confidence": confidence}
    )
      
    # Mostrar la respuesta
    if response.status_code == 200:
        prediction = response.json().get("predicted_class")
        if prediction == 1:
            st.markdown('<div class="success-box">Predicción: El pasajero dejará una propina ALTA</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">Predicción: El pasajero dejará una propina BAJA</div>', unsafe_allow_html=True)
    else:
        st.error(f"Error: {response.status_code}")

# Texto referencia
st.markdown(
    '<div class="footer-text">Alumno: J. Matías Bunster Raby<br>UDD/ Magister en Datascience</div>',
    unsafe_allow_html=True
)

