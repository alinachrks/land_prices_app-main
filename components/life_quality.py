import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, HeatMap   # Import MarkerCluster for clustering
import plotly.express as px
import geopandas as gpd
import plotly.express as px

def app():

    # Create the Streamlit app interface
    st.title("Качество жизни")

    # # Add an image after the title
    # st.image("img/life.jpg", use_column_width=True)

    # @st.cache_data  # Cache the data and model
    # def load_land_area():
    #     # Load your CSV data
    #     json_data = pd.read_csv('data/micr_full.json')
    #     return json_data

    # # Load your CSV data
    # json_data = load_land_area()

    # # Function to format price as an integer (removing extra zeros)
    # def format_price(price):
    #     return f"₸ {int(price):,}"  # Format as an integer

    
    # # Create a container for the map
    # with st.container():
    #     # Create a base map
    #     @st.cache_resource
    #     def create_map():
    #         # Преобразование WKT в геометрические объекты
    #         gdf = gpd.GeoDataFrame.from_features(json_data['features'])

    #         # Создание интерактивной карты с помощью Plotly
    #         fig = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index,
    #                                     color='price', color_continuous_scale="Viridis",
    #                                     mapbox_style="carto-positron", center={"lat": 43.238293, "lon": 76.912471},
    #                                     zoom=10, opacity=0.5)

    #         return fig

    # # Display the map in Streamlit using HTML with responsive height
    # st.header("Карта микросекторов")
    # st.plotly_chart(create_map(), use_container_width=True)

    # Description
    st.markdown("""
    ##### Веб-приложение для прогнозирования уровня качества жизни в г. Алматы

    Это приложение служит динамичным порталом для изучения и понимания индекса качества жизни в различных районах Алматы,
    предлагая пользователям подробное представление о здоровье, образовании, безопасности, качестве окружающей среды 
    и экономических условиях в городе. С помощью интерактивной приборной панели он визуализирует данные 
    с помощью цветных карт и предоставляет углубленный анализ, позволяя сравнивать их как внутри города, 
    так и в глобальном масштабе. Рассчитанное на широкую аудиторию, включая жителей, политиков и исследователей, 
    приложение способствует информированному обсуждению и принятию решений по развитию городов и улучшению качества жизни. 
    Благодаря ориентированному на пользователя интерфейсу, оно приглашает к обратной связи с сообществом, 
    что делает его инструментом совместной работы по улучшению условий жизни в Алматы.
    """)

    st.markdown("""
        ##### Прогноз качества жизни в зависимости от характеристик территории
                    """)

    # Input fields for property characteristics
    st.header("Характеристики территории")
    with st.form(key="input_form"):
        has_engineering_communications = st.checkbox("Наличие рынка", key="has_engineering_communications")
        has_kindergarten = st.checkbox("Наличие полицейского участка", key="has_kindergarten")
        has_school = st.checkbox("Наличие ломбарда в радиусе 1 км", key="has_school")
        has_medical_facility = st.checkbox("Наличие остановок общественного транспорта в радиусе 1 км", key="has_medical_facility")
        has_parking = st.checkbox("Наличие социальных объектов в радиусе 1 км", key="has_parking")
        has_park = st.checkbox("Наличие ТРК в радиусе 1 км", key="has_park")
        has_bike_path = st.checkbox("Наличие МЖК в радиусе 1 км", key="has_bike_path")
        
        # Adjusted min and max values based on the provided reference data
        school_deficit = st.slider("Дефицит рабочих мест", min_value=0, max_value=4000, value=1700, step=100, key="school_deficit")
        leisure_facilities = st.slider("Количество объектов досуга в радиусе 1 км", min_value=0, max_value=100, value=43, step=10, key="leisure_facilities")
        surveillance_cameras = st.slider("Количество камер видеонаблюдения в радиусе 1 км", min_value=0, max_value=100, value=68, step=10, key="surveillance_cameras")
        commercial_organizations = st.slider("Количество коммерческих организации в радиусе 1км", min_value=0, max_value=500, value=411, step=50, key="commercial_organizations")
        public_infrastructure = st.slider("Количество объектов благоустройства в радиусе", min_value=0, max_value=300, value=237, step=10, key="public_infrastructure")
        dining_establishments = st.slider("Количество предприятий общественного питания в радиусе", min_value=0, max_value=300, value=90, step=10, key="dining_establishments")
        air_quality_pm = st.slider("Количество уличных фонарей", min_value=10, max_value=200, value=145, step=10, key="air_quality_pm")
        population_density = st.slider("Плотность населения чел/км²", min_value=1000, max_value=20000, value=8500, step=1000, key="population_density")
        average_income = st.slider("Средний доход населения", min_value=100000, max_value=800000, value=320000, step=100000, key="average_income")
        # submitted_crime = st.form_submit_button("Предсказать уровень преступности")
        submitted = st.form_submit_button("Прогноз качества жизни")

    st.markdown("""
    <style>
    /* Increase font size for all the text */
    h1, h2, h3, h4, h5, h6 {
        font-size: 32px !important;
    }
    p, label {
        font-size: 20px !important;
    }
    /* Make the slider value bold and larger */
    div.stSlider .sliderValue {
        font-size: 28px;
        font-weight: bold;
    }
    /* Change the slider track color to dark green */
    div.stSlider .stWidget .st-bd { 
        background-color: #005f00 !important;
    }
    /* Change the slider thumb color to dark green */
    div.stSlider .stWidget .st-bf { 
        background-color: #005f00 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
        # Рекомендации для низкого уровня привлекательности
    prescriptive_message_low_temp = """
        <div style="background-color:#f0f2f6;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
            <h3 style="text-align:justify;color:black;padding:10px">Рекомендации по поднятию уровня качества жизни</h3>
            <ul>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие ДДО в радиусе 1 км:</b> Расширьте доступ к детским дошкольным учреждениям в районе, чтобы обеспечить удобство для семей с детьми.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие школы в радиусе 1 км:</b> Улучшите качество образования в существующих школах или рассмотрите возможность строительства новых учебных учреждений.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие медучреждения в радиусе 1 км:</b> Расширьте медицинские услуги или совершенствуйте существующие медицинские учреждения, чтобы обеспечить доступ к медицинской помощи.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие парковки в радиусе 1 км:</b> Обеспечьте наличие достаточного количества парковочных мест и поддерживайте их в хорошем состоянии для удобства жителей и посетителей.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие парка в радиусе 1 км:</b> Инвестируйте в создание или обслуживание парков, чтобы улучшить качество жизни в районе и обеспечить места для отдыха и рекреации.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Наличие велодорожки в радиусе 1 км:</b> Поддерживайте инфраструктуру для велосипедистов, строя новые велодорожки или улучшая существующие, чтобы способствовать экологичному транспорту.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Дефицит ДДО:</b> Рассмотрите возможность построения новых детских дошкольных учреждений или предоставьте стимулы частным поставщикам для открытия новых центров.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    <b>Дефицит школ:</b> Для решения дефицита школ можно спланировать строительство новых учебных заведений или выделить ресурсы для улучшения качества и мощности существующих школ.
                </li>
            </ul>
        </div>
    """
    # Рекомендации для среднего уровня привлекательности
    prescriptive_message_middle_temp = """
        <div style="background-color:#f0f2f6;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
            <h3 style="text-align:justify;color:black;padding:10px">Рекомендации по поднятию уровня привлекательности</h3>
            <p style="text-align:justify;color:black;padding:10px">
                Для повышения качества жизни района можно рассмотреть следующие меры:
            </p>
            <ul>
                <li style="text-align:justify;color:black;padding:10px">
                    Проведение капитального ремонта и обновление инфраструктуры.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Развитие зеленых зон и создание новых общественных пространств.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Повышение безопасности и контроль за общественным порядком.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Стимулирование развития бизнес-среды и туристического потенциала.
                </li>
            </ul>
        </div>
    """
    # Рекомендации для высокого уровня привлекательности
    prescriptive_message_high_temp = """
        <div style="background-color:#f0f2f6;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
            <h3 style="text-align:justify;color:black;padding:10px">Рекомендации по поддержанию высокого уровня привлекательности</h3>
            <p style="text-align:justify;color:black;padding:10px">
                Для поддержания высокого уровня качества жизни района рекомендуется:
            </p>
            <ul>
                <li style="text-align:justify;color:black;padding:10px">
                    Проведение регулярного мониторинга состояния инфраструктуры и окружающей среды.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Поддержание и совершенствование качества общественных сервисов и услуг.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Продолжение инвестиций в развитие инфраструктуры и социокультурной среды.
                </li>
                <li style="text-align:justify;color:black;padding:10px">
                    Привлечение инвестиций и поддержка малого и среднего бизнеса для создания рабочих мест и развития экономики.
                </li>
            </ul>
        </div>
    """
    # if submitted_crime:
    #     # Example formula to predict crime rate
    #     # Note: Coefficients are hypothetical and should be adjusted based on empirical analysis
    #     crime_rate_prediction = (population_density / 1000) - (average_income / 32000) + (air_quality_pm / 50)
    #     crime_rate_prediction *= 100  # Adjust scale to resemble per 10,000 people metric
    
    # st.write(f"Предсказанный уровень преступности: {crime_rate_prediction:.1f} преступлений на 10000 человек")
    # Button to make predictions
    if submitted:
        # Data preprocessing with updated variable names
        new_features = np.array([
            has_engineering_communications, has_kindergarten, has_school, has_medical_facility,
            school_deficit, leisure_facilities, has_parking, has_park, surveillance_cameras, 
            has_bike_path, commercial_organizations, public_infrastructure, 
            dining_establishments, air_quality_pm, population_density, average_income
        ]).reshape(1, -1)
        # Создание объекта MinMaxScaler
        # scaler = MinMaxScaler()
        # Нормирование значений
        # new_features_scaled = scaler.fit_transform(new_features)
        # # Predict property price
        # new_predicted_price = model.predict(new_features)[0]
        # Provided data
        # average_income = 320000  # in KZT
        # population_density = 3163  # people per km²
        # crime_rate = 191.5  # crimes per 10,000 people
        # # Reference values (hypothetical)
        # reference_income = 500000  # Example benchmark
        # reference_crime_rate = 100.0  # Example benchmark
        # crime_rate_weight = 0.5  # Adjusts the impact of the crime rate
        # Calculate Economic Well-being Score
        # economic_wellbeing_score = (average_income / reference_income) - ((crime_rate / reference_crime_rate) * crime_rate_weight)
        # st.title("Индекс Экономического Благополучия для Алматы")
        # st.write(f"Рассчитанный индекс экономического благополучия: {economic_wellbeing_score:.2f}")
        predicted_price = (
            15000 * has_engineering_communications +
            8000 * has_kindergarten +
            7000 * has_school +
            6000 * has_medical_facility +
            5000 * has_parking +
            9000 * has_park +
            4000 * has_bike_path -
            50 * school_deficit +
            50 * leisure_facilities +
            50 * surveillance_cameras +
            500 * commercial_organizations +
            400 * public_infrastructure +
            300 * dining_establishments +
            50 * air_quality_pm -
            1 * population_density+
            0.07 * average_income
        )
        if predicted_price < 61428:
            predicted_price = 61428
        elif predicted_price > 384160:
            predicted_price = 384160
        else:
            predicted_price = predicted_price
        # Divide the predicted price by 1.6
        #divided_price = new_predicted_price / 1.6
        new_predicted_price = predicted_price
        # Display the prediction result
        st.header("Результат прогноза")
        st.markdown(
            """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 40px;
                color: green;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # Display the prediction result
        st.header("Уровень качества жизни")
        if new_predicted_price >= 250000:
            st.markdown('<p style="font-size: 30px; color: green;">Высокий</p>', unsafe_allow_html=True)
            st.image("img/high_level.jpg", use_column_width=True)
            st.markdown(prescriptive_message_high_temp, unsafe_allow_html=True)
        elif new_predicted_price >= 170000:
            st.markdown('<p style="font-size: 30px; color: orange;">Средний</p>', unsafe_allow_html=True)
            st.image("img/middle_level.jpg", use_column_width=True)
            st.markdown(prescriptive_message_middle_temp, unsafe_allow_html=True)
        else:
            st.markdown('<p style="font-size: 30px; color: red;">Низкий</p>', unsafe_allow_html=True)
            st.image("img/low_level.png", use_column_width=True)
            st.markdown(prescriptive_message_low_temp, unsafe_allow_html=True)


