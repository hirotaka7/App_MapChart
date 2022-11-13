import streamlit as st
import pandas as pd
import numpy as np
import folium as fl
import geopandas as gpd
from folium.plugins import BeautifyIcon
import plotly.express as px

BaseColor=['#80BBAD', '#435254', '#17E88F', '#DBD99A', '#D2785A', '#885073', '#A388BF', '#1F3765', '#3E7CA6', '#CAD1D3']
PU_Start='<div style="font-size: 12pt; color : #435254; font-weight: bold;"><span style="white-space: nowrap;">'
PU_End='</span></div>'


st.set_page_config(layout="wide")
st.title('Map & Charts Challenge')
tab1,tab2,tab3,tab4,tab5=st.tabs(['Map','Plotly Data','Plotly Graph','Manual Input','Manual Input Graph'])
with st.sidebar:
    st.title('Input')
    GoogleXY=st.text_input('GoogleXY :','35.67910332269817, 139.76214627560367')
    if ', ' in GoogleXY:
        POINT_X=float(GoogleXY.split(', ')[1])
        POINT_Y=float(GoogleXY.split(', ')[0])
        st.write(f'経度：{POINT_X}')
        st.write(f'緯度：{POINT_Y}')
        df=pd.DataFrame(data={'POINT_Y':[POINT_Y],'POINT_X':[POINT_X]})
        gdf=gpd.GeoDataFrame(
            crs=6668,
            data=df.copy(),
            geometry=gpd.points_from_xy(
                list(df.POINT_X),
                list(df.POINT_Y)
            )
        )
    else:
        st.error('Google Map からコピペして下さい', icon="🗺️")
    
    Ring_Kilo=st.select_slider('Ring Kilo :',[1,2,3,5,10],3)
    st.title(f'半径{Ring_Kilo}km 圏')
    Ring=gdf.to_crs(6688).buffer(Ring_Kilo*1000).to_crs(6668)
    gdf_Ring=gpd.GeoDataFrame(Ring,columns=['geometry'],crs=6668)
    Map_1=fl.Map(
        location=[gdf.geometry.y[0],gdf.geometry.x[0]],
        tiles='cartodbpositron',
        zoom_start=16
    )
    Group=fl.FeatureGroup(name='対象物件').add_to(Map_1)
    Group.add_child(
        fl.Marker(
            location=[gdf.geometry.y[0],gdf.geometry.x[0]],
            icon=BeautifyIcon(icon='star',border_width=2,border_color=BaseColor[0],text_color=BaseColor[0],spin=True)
        )
    )
    st.components.v1.html(fl.Figure().add_child(Map_1).render(),height=300)
    csv=st.file_uploader("Phonetic.csv をアップロード", type='csv')
    if csv is not None:
        df2=pd.read_csv(csv,encoding='utf-8')
    else:
        df2=pd.DataFrame({
            'Phonetic':['Alfa','Bravo','Chailie','Delta','Echo','Foxtrot','Golf','Hotel'],
            'JPN':['アルファ','ブラボー','チャーリー','デルタ','エコー','フォックストロット','ゴルフ','ホテル'],
        })
        df2=df2.assign(Value1=0)
        df2=df2.assign(Value2=0)


Map=fl.Map(
    location=[gdf.geometry.y[0],gdf.geometry.x[0]],
    tiles='cartodbpositron',
    zoom_start=12
)

Group=fl.FeatureGroup(name='対象物件').add_to(Map)
Group.add_child(
    fl.Marker(
        location=[gdf.geometry.y[0],gdf.geometry.x[0]],
        popup=PU_Start+'対象物件'+PU_End,
        icon=BeautifyIcon(icon='star',border_width=2,border_color=BaseColor[0],text_color=BaseColor[0],spin=True)
    )
)
Group=fl.FeatureGroup(name=f'半径{Ring_Kilo}km 圏').add_to(Map)
Group.add_child(
    fl.GeoJson(
        data=gdf_Ring,
        style_function=lambda x:{'fillColor':BaseColor[0],'color':BaseColor[0],'weight':2,'fillOpacity':0.1}
    )
)
fl.LayerControl().add_to(Map)



with tab1:
    st.components.v1.html(fl.Figure().add_child(Map).render(),height=650)
    st.download_button('🗺️ Map Download', fl.Figure().add_child(Map).render(),file_name='Map.html')
    
with tab2:
    df=pd.DataFrame({
        'Phonetic':['Alfa','Bravo','Chailie','Delta','Echo','Foxtrot','Golf','Hotel'],
        'JPN':['アルファ','ブラボー','チャーリー','デルタ','エコー','フォックストロット','ゴルフ','ホテル'],
    })
    df=df.assign(Value1=np.random.randint(10,100,len(df)))
    df=df.assign(Value2=np.random.randint(100,1000,len(df)))
    st.dataframe(df,use_container_width=True)
    st.download_button('📋 csv Download', df.to_csv(index=False).encode('utf-8'),file_name='Data.csv')


with tab3:
    PhoneticList=st.multiselect('Select Phonetic', df.Phonetic, df.Phonetic)
    df_Sort=df[df.Phonetic.isin(PhoneticList)].reset_index(drop=True)
    fig=px.bar(df_Sort,x=df_Sort.Phonetic,y=df_Sort.Value1,color='Phonetic',color_discrete_sequence=BaseColor)
    fig.update_traces(
            width=0.75,
            texttemplate='%{y:,}',
            textposition='inside'
        )
    fig.update_layout(
        height=500,
        margin=dict(t=10,b=10,l=10,r=10),
    )
    fig2=px.bar(df_Sort,x=df_Sort.Phonetic,y=df_Sort.Value2,color='Phonetic',color_discrete_sequence=BaseColor)
    fig2.update_traces(
            width=0.75,
            texttemplate='%{y:,}',
            textposition='inside'
        )
    fig2.update_layout(
        height=500,
        margin=dict(t=10,b=10,l=10,r=10),
    )
    v=st.radio('Select Show Value',['Value1','Value2'])
    if v=='Value1':
        st.plotly_chart(fig,use_container_width=True)
    if v=='Value2':
        st.plotly_chart(fig2,use_container_width=True)
with tab4:
    st.dataframe(df2,use_container_width=True)
with tab5:
    fig=px.bar(df2,x=df.Phonetic,y=df2.Value1,color='Phonetic',color_discrete_sequence=BaseColor)
    fig.update_traces(
            width=0.75,
            texttemplate='%{y:,}',
            textposition='inside'
        )
    fig.update_layout(
        height=500,
        margin=dict(t=10,b=10,l=10,r=10),
    )
    fig2=px.bar(df2,x=df2.Phonetic,y=df2.Value2,color='Phonetic',color_discrete_sequence=BaseColor)
    fig2.update_traces(
            width=0.75,
            texttemplate='%{y:,}',
            textposition='inside'
        )
    fig2.update_layout(
        height=500,
        margin=dict(t=10,b=10,l=10,r=10),
    )
    v=st.radio('Select Show Value',['MValue1','MValue2'])
    if v=='MValue1':
        st.plotly_chart(fig,use_container_width=True)
    if v=='MValue2':
        st.plotly_chart(fig2,use_container_width=True)
    
    
    

    

    