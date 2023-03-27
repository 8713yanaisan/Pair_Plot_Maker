# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:41:40 2023

@author: u00180134
"""

from io import BytesIO

import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt # プロット用
import matplotlib.cm as cm
import plotly.express as px


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

#TimeStampの変換するかどうか
time_check = st.checkbox('Color is time')
if time_check:
    df["Time_unix"]=df[color].map(pd.Timestamp.timestamp)



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
        fig_pair.show()
    else:
        fig_pair=px.scatter_matrix(df_pair)
        fig_pair.show()



