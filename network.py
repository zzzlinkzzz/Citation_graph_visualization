from pyvis.network import Network
import json
from numpy import log2
import pandas as pd
from utils import find_ref, dump_option, map_algs,tfidf
from functools import reduce
# =============================================================================
# node & edge color
red = "#FF3008"
blue = "#2b7ce9"
cyan = "#97c2fc"
green = "#349E54"
yelow = "#DED007"
# =============================================================================
def draw_network(id_list):
    # tim kiem bai bao trich dan theo 4 cap
    items1, ref_list1 = find_ref(id_list)
    items2, ref_list2 = find_ref(ref_list1)
    items3, ref_list3 = find_ref(ref_list2)
    items4, ref_list4 = find_ref(ref_list3)
    
    # save info dfs
    col = [ 'year', 'cited_num','title']
    df1 = pd.DataFrame(items1)[col]
    df1.to_hdf('temp/temp1.h5',key='df')
    df2 = pd.DataFrame(items2)[col]
    df2.to_hdf('temp/temp2.h5',key='df')
    df3 = pd.DataFrame(items3)[col]
    df3.to_hdf('temp/temp3.h5',key='df')
    df4 = pd.DataFrame(items4)[col]
    df4.to_hdf('temp/temp4.h5',key='df')
    
    # titles for tf-idf
    query_titles = reduce(lambda a,b: pd.concat([a,b], axis=0),[df1,df2,df3,df4])['title'].values.tolist()
    dump_option(query_titles,'temp_titles')
    tfidf('temp_titles')
# =============================================================================
#     # tao base graph
#     g = Network(height = '550px', width = "100%", directed=True, bgcolor = "#222222", font_color="White")
#     
#     # them cac node vao graph
#     for node in items1:
#         g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 30*log2(node['cited_num']), color = green, shape = "star", physics = False)
#     for node in items2:
#         g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 30*log2(node['cited_num']), color = yelow, shape = "dot")
#     for node in items3:
#         g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 30*log2(node['cited_num']), color = red, shape = "dot")
#     for node in items4:
#         g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 30*log2(node['cited_num']), color = cyan, shape = "dot")
#     for node in items1:
#         g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 30*log2(node['cited_num']), color = green, shape = "star", physics = False)
#     
#     # them cac edge vao graph
#     for node in items1:
#         for ref in node['references']:
#             g.add_edge(node['id'],ref,color = blue, width  = 10)
#     for node in items2:
#         for ref in node['references']:
#             g.add_edge(node['id'],ref,color = blue, width  = 10)
#     for node in items3:
#         for ref in node['references']:
#             g.add_edge(node['id'],ref,color = blue, width  = 10)
#     
#     # chon kieu visual
#     map_algs(g, alg="barnes")
#     
#     # save
#     g.save_graph('temp/temp.html')
# =============================================================================

# =============================================================================
if __name__ == '__main__':
    id_list = ['0cb982a9-0458-4478-904b-e05a0ff969b8']
    test = draw_network(id_list)
