# -*- coding: utf-8 -*-

"""

Created on Mon Mar 20 11:41:40 2023

 

@author: yanai

"""

 

 

 

import pandas as pd

import streamlit as st

import datetime

import plotly.express as px

from plotly import graph_objects as go



 

st.title('グラフ作成')

 

# xlsxファイルのドラッグアンドドロップによる入力を受け付ける

uploaded_file = st.file_uploader("Excelファイルをアップロードしてください")

 

# xlsxファイルを読み込む

if uploaded_file is not None:

     df = pd.read_excel(uploaded_file)

 

df = st.experimental_data_editor(df, num_rows="dynamic")

 

 

#列名のリスト

clm=list(df.columns)

 

st.write("Color Map")

 

 

#フィルタリングするかどうか

filter_check = st.checkbox('フィルターしますか')

if filter_check:

     fil=st.selectbox('filter',clm)

     'filterは',fil,'です。'

     selected_erea = st.multiselect('グラフに表示する要素を選択',

list(set(list(df[fil]))))

     df = df[(df[fil].isin(selected_erea))]

 

 

 

x=st.selectbox('x軸',

     clm)

'x軸は',x,'です。'

 

y=st.selectbox('y軸',

     clm)

'y軸は',y,'です。'

 

color=st.selectbox('color',

     clm)

'colorは',color,'です。'

 

df["Time_unix"]=df[color]

 

range_check = st.checkbox('変数の範囲を設定')

if range_check:

    value_range=st.selectbox('変数の範囲',

         clm)

    value_range,'の範囲を下記スライダーで設定。'

   

    values = st.slider(

        '変数の最小値と最大値を決める',

        min(df[value_range]), max(df[value_range]), (min(df[value_range]),

                                                     max(df[value_range])))

   

    df = df[(values[0] <= df[value_range]) & (values[1] >= df[value_range])]

 

 

#TimeStampの変換するかどうか

#time_check = st.checkbox('Colorのデータ型： time')

 

if pd.api.types.is_datetime64_any_dtype(df[color]):

     tick_num = 5

     df["Time_unix"]=df[color].map(pd.Timestamp.timestamp)

     time_max = df["Time_unix"].max()

     time_min = df["Time_unix"].min()

     tickrows = [i * df.shape[0] // tick_num for i in range(tick_num)]

     tickvals = [time_min + i * (time_max - time_min) / tick_num for i in range(tick_num)]

     print(tickvals)

     ticktext = [datetime.datetime.fromtimestamp(i, datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y/%m/%d") for i in tickvals]

     print(tickvals, ticktext)

 

     fig = go.Figure(

          data = go.Scatter(

               x=df[x],

               y=df[y],

               mode = "markers",

               marker = dict(

                    color = df["Time_unix"],

                    showscale=True

               ),

               marker_colorbar=dict(tickvals=tickvals,

                         ticktext=ticktext,

                         title = "date-time"

                         ),

               hoverinfo="skip",

               hovertemplate = x+" : %{x}<br>"+y+" : %{y}"

          )

     )

 

else: #こちらは元のままです

     fig=px.scatter(

          #df.query(""),

          x=df[x],

          y=df[y],

          color=df["Time_unix"],

          hover_name=df[color],

          labels=dict(x=x, y=y, color=color)

          )

 

 

st.plotly_chart(fig, theme="streamlit", use_container_width=True)

 

 

 

 

#Pair plot

 

st.write("Pair Plot")

options = st.multiselect(

     'Select for Pair Plot',

     clm)

 

st.write('You selected:', options)

 

 

#dfの中からoptionで選んだ要素でデータフレーム作成

df_pair=df[[col for col in options]]

 

#Color_Plotにするかどうか

color_check = st.checkbox('Color?')

 

if color_check:

     color_pair=st.selectbox('Color',

         clm)

     'Colorは',color_pair,'です。'

 

     df_pair=pd.concat([df_pair,df[color_pair]],axis=1)

 

 

#ボタンを押してグラフ作成

graph_btn=st.button("Make Graph: Move to other page")

if graph_btn==True:

     if color_check==True:

         fig_pair=px.scatter_matrix(df_pair,

                   color=color_pair)

         st.plotly_chart(fig_pair, theme="streamlit", use_container_width=True)

     else:

         fig_pair=px.scatter_matrix(df_pair)

         st.plotly_chart(fig_pair, theme="streamlit", use_container_width=True)

 