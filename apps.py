import streamlit as st
import streamlit.components.v1 as components
from network import draw_network
from utils import load_option, search_text, dump_option

st.set_page_config(
     page_title="Citation Network",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
)
temp_network = False

titles = load_option('titles')
id_list = load_option('id_list')


# side bar
st.sidebar.title("Options:")
keywords = st.sidebar.text_area('')
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


st.header("Science paper network visualization")
# main page
if temp_network:
    draw_network(chosen_id)
    HtmlFile = open('temp/temp.html', 'r',  encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600, width = 1200)
else:
    HtmlFile = open('temp/base.html', 'r',  encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600, width = 1200)
    
st.text("Thành viên - Lê Thanh Tùng - 20007905 - Vu Hoang Dung - xxx")
