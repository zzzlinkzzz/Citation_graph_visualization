from pyvis.network import Network
import json
from pymongo import MongoClient
from numpy import log2

client = MongoClient(
    "mongodb+srv://TungLe:396369@cluster0.7tetj.mongodb.net/visualization?retryWrites=true&w=majority")
db = client.get_database('visualization')
collection = db.get_collection('citation_network')

def find_ref(id_list):
    '''
    tim kiem paper trong database
    return: 
        metadata cua paper trong list (list of object (json))
        danh sach id cac bai bao da trich dan (list of paper id (str))
    '''
    result, ref_list = list(), set()
    for id in id_list:
        items = collection.find({'id': id})
        for item in items:
            result.append(item)
            for ref in item['references']:
                ref_list.add(ref)
                    
                    
        items.close()
    return result, list(ref_list)

def draw_network(id_list):
    # tim kiem bai bao trich dan theo 4 cap
    items1, ref_list1 = find_ref(id_list)
    items2, ref_list2 = find_ref(ref_list1)
    items3, ref_list3 = find_ref(ref_list2)
    # items4, ref_list4 = find_ref(ref_list3)
    
    # node & edge color
    red = "#FF3008"
    blue = "#2b7ce9"
    cyan = "#97c2fc"
    green = "#349E54"
    yelow = "#DED007"
    
    # chon kieu visual
    def map_algs(g, alg="barnes"):
        if alg == "barnes":
            g.barnes_hut(gravity=-100000, central_gravity=0.3, spring_length=1000, spring_strength=0.0001, damping=0.09, overlap=0)
        if alg == "forced":
            g.force_atlas_2based()
        if alg == "hr":
            g.hrepulsion()
    
    # tao base graph
    g = Network(height = '550px', width = "100%", bgcolor = "#222222", font_color="White")
    
    # them cac node vao graph
    for node in items1:
        g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 25*log2(node['cited_num']), color = red, shape = "star", physics = False)
    for node in items2:
        g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 25*log2(node['cited_num']), color = yelow, shape = "dot")
    for node in items3:
        g.add_node(node['id'], label = node['title'] + '. Citation: ' + str(node['cited_num']), size = 25*log2(node['cited_num']), color = cyan, shape = "dot")
    # for node in items4:
    #     g.add_node(node['id'], label = node['title'], size = node['cited_num'], color = green, shape = "dot")
    
    # them cac edge vao graph
    for node in items1:
        for ref in node['references']:
            g.add_edge(node['id'],ref,color = blue, width  = 4)
    for node in items2:
        for ref in node['references']:
            g.add_edge(node['id'],ref,color = blue, width  = 4)
    # for node in items3:
    #     for ref in node['references']:
    #         g.add_edge(node['id'],ref,color = blue, width  = 4)
            
    map_algs(g, alg="barnes")
    g.save_graph('temp/temp.html')


if __name__ == '__main__':
    id_list = ['0cb982a9-0458-4478-904b-e05a0ff969b8']
    draw_network(id_list)
