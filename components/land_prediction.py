import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
#from sklearn.linear_model import LinearRegression
#from sklearn.ensemble import RandomForestRegressor
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster  # Import MarkerCluster for clustering
import plotly.express as px
import joblib  # Required for loading the model
from sklearn.preprocessing import MinMaxScaler

def app():

    # Create a Streamlit caching decorator for data loading
    # @st.cache_data # Cache the data
    # def load_data():
    #     # Load your CSV data
    #     data = pd.read_csv('data/train_data.csv')
    #     return data

    # # Load the data
    # data = load_data()

    # Load the pre-trained model
    # @st.cache_data # Cache the model
    # def load_model():
    #     # Load the model from the file
    #     model = joblib.load('models/regression_model.pkl')
    #     return model

    # # Call the cached function to load the model
    # model = load_model()

    # Create the Streamlit app interface
    st.title("Прогнозирование стоимости земельных участков")

    # Add an image after the title
    st.image("img/pic1.jpeg", use_column_width=True)

    @st.cache_data  # Cache the data and model
    def load_land_area():
        # Load your CSV data
        csv_data = pd.read_csv('data/land_area_updated.csv')
        return csv_data

    # Load your CSV data
    csv_data = load_land_area()

    # Function to format price as an integer (removing extra zeros)
    def format_price(price):
        return f"₸ {int(price):,}"  # Format as an integer

    # Create a container for the map
    with st.container():
        # Create a base map
        @st.cache_resource
        def create_map():
            m = folium.Map(location=[43.238293, 76.912471], zoom_start=9, control_scale=True, width=700)

            # Create a MarkerCluster for clustering
            marker_cluster = MarkerCluster().add_to(m)

            # Add markers for each land plot with popups
            for index, row in csv_data.iterrows():
                formatted_price = format_price(row['price'])  # Format the price using the function
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=f"<b>Адрес:</b> {row['address']}<br><b>Площадь:</b> {row['area']} sq.m<br><b>Цена:</b> {formatted_price}",
                ).add_to(marker_cluster)  # Add markers to the MarkerCluster for clustering

            return m

        # Call the create_map function to create or retrieve the cached map
        m = create_map()

    # Display the map in Streamlit using HTML with responsive height
    st.header("Карта земельных участков")
    st.components.v1.html(m._repr_html_(), width=710, height=400)

    # Description
    st.markdown("""
    ##### Веб-приложение для прогнозирования стоимости земельных участков в Алматы

    Это приложение использует машинное обучение для прогнозирования стоимости земельных участков. 
    Оно загружает предварительно обученную модель линейной регрессии, которая принимает на вход различные характеристики участка, 
    такие как расстояние до ДДО, школы, медучреждения, дефицит ДДО и школ, количество объектов досуга, наличие парковки, парка, камер видеонаблюдения, 
    наличие велодорожки, количество мусорных контейнеров, количество точек интереса и предприятий общественного питания в радиусе 1000 метров, 
    индекс ближайшего датчика после полудня и до полудня. 
    Приложение предварительно обрабатывает входные данные, объединяя некоторые характеристики и добавляя новые, например, расстояние до ближайшего города.
    """)


    st.markdown("""
    ##### Прогноз стоимости земли после программы реновации
                """)

    # Input fields for property characteristics
    st.header("Характеристики земельного участка")

    # Set custom CSS styles for the slider and its displayed value
    st.markdown("""
        <style>
            /* Style the slider */
            .st-eb .st-ei .st-eh .st-el {
                width: 400px !important; /* Set the width of the slider */
            }
            /* Style the displayed value */
            .slider-value {
                color: red; /* Change the color of the value */
                font-size: 18px; /* Change the font size of the value */
            }
        </style>
    """, unsafe_allow_html=True)


    with st.form(key="input_form"):
        has_engineering_communications = st.checkbox("Наличие инженерных коммуникаций", key="has_engineering_communications")
        has_kindergarten = st.checkbox("Наличие ДДО в радиусе 1 км", key="has_kindergarten")
        has_school = st.checkbox("Наличие школы в радиусе 1 км", key="has_school")
        has_medical_facility = st.checkbox("Наличие медучреждения в радиусе 1 км", key="has_medical_facility")
        has_parking = st.checkbox("Наличие парковки в радиусе 1 км", key="has_parking")
        has_park = st.checkbox("Наличие парка в радиусе 1 км", key="has_park")
        has_bike_path = st.checkbox("Наличие велодорожки в радиусе 1 км", key="has_bike_path")
        
        # Adjusted min and max values based on the provided reference data
        kindergarten_deficit = st.slider("Дефицит мест в ДДО", min_value=0, max_value=300, value=110, step=10, key="kindergarten_deficit")
        school_deficit = st.slider("Дефицит школьных мест", min_value=0, max_value=4000, value=1700, step=100, key="school_deficit")
        leisure_facilities = st.slider("Количество объектов досуга в радиусе 1 км", min_value=0, max_value=100, value=43, step=10, key="leisure_facilities")
        surveillance_cameras = st.slider("Количество камер видеонаблюдения в радиусе 1 км", min_value=0, max_value=100, value=68, step=10, key="surveillance_cameras")
        commercial_organizations = st.slider("Количество коммерческих организации в радиусе 1км", min_value=0, max_value=500, value=411, step=50, key="commercial_organizations")
        public_infrastructure = st.slider("Количество объектов благоустройства в радиусе", min_value=0, max_value=300, value=237, step=10, key="public_infrastructure")
        dining_establishments = st.slider("Количество предприятий общественного питания в радиусе", min_value=0, max_value=300, value=90, step=10, key="dining_establishments")
        air_quality_pm = st.slider("Показатель качества воздуха после полудня", min_value=10, max_value=200, value=145, step=10, key="air_quality_pm")
        population_density = st.slider("Плотность населения чел/км²", min_value=1000, max_value=20000, value=8500, step=1000, key="population_density")
        average_income = st.slider("Средний доход населения", min_value=100000, max_value=800000, value=320000, step=100000, key="average_income")

        # submitted_crime = st.form_submit_button("Предсказать уровень преступности")

        submitted = st.form_submit_button("Предсказать стоимость")

    # Increase font size for all the text
    st.markdown("<style>h1, h2, h3, h4, h5, h6 {font-size: 32px !important;}</style>", unsafe_allow_html=True)
    st.markdown("<style>p, label {font-size: 20px !important;}</style>", unsafe_allow_html=True)
    

    st.markdown("""
        <style>
            /* Increase font size and make the slider value bold */
            div.stSlider .sliderValue { 
                font-size: 28px; 
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)




    prescriptive_message_low_temp = """
    	<div style="background-color:#e4e4e4;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
    		<h3 style="text-align:justify;color:black;padding:10px">Рекомендации по улучшению характеристик земельного участка</h3>
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
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Количество объектов досуга в радиусе 1000 м:</b> Поддерживайте разнообразные места для развлечений, чтобы удовлетворить различные интересы и возрастные группы.
    			</li>
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Количество камер видеонаблюдения в радиусе 1000 м:</b> Обеспечьте безопасность района, поддерживая и расширяя сеть видеонаблюдения.
    			</li>
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Количество коммерческих организаций в радиусе 1000 м:</b> Содействуйте разнообразию бизнес-среды, поощряя открытие коммерческих организаций, которые соответствуют потребностям сообщества.
    			</li>
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Количество объектов благоустройства в радиусе 1000 м:</b> Инвестируйте в благоустройство общественных мест и уделяйте внимание обслуживанию скамеек, детских площадок и центров общественного обслуживания.
    			</li>
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Количество предприятий общественного питания в радиусе 1000 м:</b> Поддерживайте разнообразную сферу общественного питания, способствуя развитию ресторанов и кафе, предлагающих различные виды кухни.
    			</li>
    			<li style="text-align:justify;color:black;padding:10px">
    				<b>Показатель датчика качества воздуха:</b> Улучшите качество воздуха, внедряя меры по снижению загрязнения и поощрению экологически чистых практик.
    			</li>
    		</ul>
    	</div>
    """

    prescriptive_message_middle_temp = """
    	<div style="background-color:#e4e4e4;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
    		<h3 style="text-align:justify;color:black;padding:10px">Рекомендации по улучшению характеристик земельного участка</h3>
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
    		</ul>
    	</div>
    """

    prescriptive_message_high_temp = """
        <div style="background-color:#e4e4e4;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
            <h3 style="text-align:justify;color:black;padding:10px">Рекомендации по поддержанию высокой стоимости земли</h3>
            <p style="text-align:justify;color:black;padding:10px">
                Для поддержания высокой стоимости земли рекомендуется:
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
            kindergarten_deficit, 
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
            100 * kindergarten_deficit -
            50 * school_deficit +
            50 * leisure_facilities +
            50 * surveillance_cameras +
            500 * commercial_organizations +
            400 * public_infrastructure +
            300 * dining_establishments -
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
        divided_price = predicted_price

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

        # Display the metric based on the value of divided_price
        if divided_price >= 270000:
            st.metric(label='Стоимость земли (м²)*', value=f"₸ {divided_price:.0f}", delta=None)
            st.markdown(prescriptive_message_high_temp, unsafe_allow_html=True)
        elif divided_price >= 250000:
            st.metric(label='Стоимость земли (м²)*', value=f"₸ {divided_price:.0f}", delta=None)
            st.markdown(prescriptive_message_middle_temp, unsafe_allow_html=True)
        elif divided_price < 250000:
            st.metric(label='Стоимость земли (м²)*', value=f"₸ {divided_price:.0f}", delta=None)
            st.markdown(prescriptive_message_low_temp, unsafe_allow_html=True)

        # Add a caption for the asterisk
        st.caption("* на 2024 год")
    


        





