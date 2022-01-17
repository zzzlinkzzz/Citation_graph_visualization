import streamlit as st
import streamlit.components.v1 as components
from network import draw_network
from nltk.tokenize import MWETokenizer
import pandas as pd
from utils import load_option, search_text, dump_option
import plotly.graph_objects as go
# =============================================================================
st.set_page_config(
     page_title="Citation Network",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",)
pd.set_option('max_colwidth', 1150)
temp_network = False
titles = load_option('titles')
id_list = load_option('id_list')
multiwords = load_option('multiwords')
tokenizer = MWETokenizer(multiwords,separator='_')
temp = False
# =============================================================================
# side bar
st.sidebar.title("Options:")
keywords = st.sidebar.text_input('Keywords')
search_button = st.sidebar.button("Search")

if search_button:
    result, index = search_text(keywords,titles)
    dump_option(result,'result')
    dump_option(index,'index')
try:
    result = load_option('result')
    index = load_option('index')
except:
    result = []
chosen_papers = st.sidebar.radio('Select titles', result)
chosen_id = [id_list[index[result.index(chosen_papers)]]]
temp_network = st.sidebar.button("Draw")
# =============================================================================
# main page
st.header("Science paper network visualization")

if temp_network:
    temp = True
    # graph
    draw_network(chosen_id)
    HtmlFile = open('temp/temp.html', 'r',  encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600, width = 1200)

else:
    # graph
    HtmlFile = open('temp/base.html', 'r',  encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600, width = 1200)
    
if temp:
    # tf-idf
    sub_titles = load_option('temp_titles')
    feature_names = load_option('temp_feature_names')
    denselist = load_option('temp_denselist')
    filted_titles = load_option('temp_filted_titles')
    st.subheader('Keywords score using TF-IDF')

    # select paper to calcuate
    choice = st.selectbox('Select title', sub_titles)
    row_index = sub_titles.index(choice)
    calculate = st.button('Calculate')

    # horizontal bar chart
    if calculate:
        text = tokenizer.tokenize(filted_titles[row_index].split())
        indies = [feature_names.index(x) for x in text]
        score = [round(denselist[row_index][col_index],3) for col_index in indies]
        
        fig = go.Figure(go.Bar(x=score[::-1],y=text[::-1],orientation='h'))
        fig.update_layout(title=choice,font=dict(size=18,color="#7f7f7f"))
        st.plotly_chart(fig, use_container_width=True)
    
    # show paper table
    st.subheader('Paper info')
    df = pd.read_hdf('temp/temp1.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#349E54'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 1')
    df = pd.read_hdf('temp/temp2.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#DED007'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 2')
    df = pd.read_hdf('temp/temp3.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#FF3008'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 3')
    df = pd.read_hdf('temp/temp4.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#97c2fc'),
                    ('font-size', '25px'),]}]
        ), width=1200)

else:
    # tf-idf
    sub_titles = load_option('base_titles')
    feature_names = load_option('base_feature_names')
    denselist = load_option('base_denselist')
    filted_titles = load_option('base_filted_titles')
    st.subheader('Keywords score using TF-IDF')

    # select paper to calcuate
    choice = st.selectbox('Select title', sub_titles)
    row_index = sub_titles.index(choice)
    calculate = st.button('Calculate')

    # horizontal bar chart
    if calculate:
        text = tokenizer.tokenize(filted_titles[row_index].split())
        indies = [feature_names.index(x) for x in text]
        score = [round(denselist[row_index][col_index],3) for col_index in indies]
        
        fig = go.Figure(go.Bar(x=score[::-1],y=text[::-1],orientation='h'))
        fig.update_layout(title=choice,font=dict(size=18,color="#7f7f7f"))
        st.plotly_chart(fig, use_container_width=True)

    # show paper table
    st.subheader('Paper info')
    df = pd.read_hdf('temp/base1.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#349E54'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 1')
    df = pd.read_hdf('temp/base2.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#DED007'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 2')
    df = pd.read_hdf('temp/base3.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#FF3008'),
                    ('font-size', '25px'),]}]
        ), width=1200)
    
    st.subheader('References level 3')
    df = pd.read_hdf('temp/base4.h5',key='df')
    st.dataframe(df.style.set_table_styles(
        [{'selector': '',
          'props': [('color', '#97c2fc'),
                    ('font-size', '25px'),]}]
        ), width=1200)
# =============================================================================
