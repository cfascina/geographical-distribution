import geopandas as gpd
import locale
import pandas as pd
import plotly.express as px
import streamlit as st

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
st.set_page_config(page_title = 'Evolução de Assinaturas Ativas', layout = 'wide')

df = pd.read_csv('sources/results.csv')
df['Mês'] = pd.to_datetime(df['month'], format = '%Y%m').dt.strftime('%B/%Y').str.capitalize()
df = df.iloc[:, [0, 5, 1, 2, 3, 4]]
df.columns = ['Mês (ordenação)', 'Mês', 'UF', 'Código', 'Assinaturas', 'Peso']
gdf_simplified = gpd.read_file('sources/basemap-simplified.geojson')

st.header('Evolução de Assinaturas Ativas')
col1, col2 = st.columns(2, border = True)

# Map Chart
with col1:
	st.subheader('Distribuição Geográfica')
	fig_map = px.choropleth(
		df,
		geojson = gdf_simplified,
		locations = 'Código', # Coluna no DataFrame para cruzamento com o GeoJSON
		featureidkey = 'properties.code', # Chave no GeoJON para cruzmaneto com o DataFrame
		color = 'Peso',
		hover_name = 'UF',
		hover_data = {
			'Código': False,
			'Assinaturas': True,
			'Peso': ':.2f'
		},
		animation_frame = 'Mês',
		projection = 'equirectangular',
		color_continuous_scale = 'Reds',
		range_color=[df['Peso'].quantile(0.05), df['Peso'].quantile(0.95)]
	)
	fig_map.update_geos(
		fitbounds = 'locations',
		visible = False
	)
	fig_map.update_layout(
		coloraxis_colorbar = dict(
			title = 'Peso',
			tickformat = '.2f'
		)
	)
	st.plotly_chart(fig_map, use_container_width = False)

# Bar Chart
with col2:
	st.subheader('Ranking de Estados')
	fig_bar = px.bar(
		df,
		x = 'Assinaturas',
		y = 'UF',
		color = 'UF',
		animation_frame = 'Mês',
		orientation = 'h',
		opacity = .75,
		hover_data = {'Assinaturas': ':d'}
	)
	fig_bar.update_layout(
		yaxis = {'categoryorder': 'total ascending'},
		showlegend = False,
		bargap = 0.25
	)
	st.plotly_chart(fig_bar, use_container_width = False)

st.divider()

# Table
st.subheader('Tabela')
st.dataframe(df)
