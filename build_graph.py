from db import get_connection_1
from twitter_user import TwitterUser
from relationship import TOP_100
from datetime import date
import networkx as nx
import matplotlib.pyplot as plt

def build_graph():
    pair_list = TwitterUser.get_top_100_pair()
    DG = nx.DiGraph()
    DG.add_edges_from([(foer, twitter_user) for twitter_user, foer in
        pair_list])
    betweenness = nx.betweenness_centrality(DG)
    closeness = nx.closeness_centrality(DG)
    edge_betweenness = nx.edge_betweenness(DG)
    clustering_co = nx.clustering(nx.Graph(DG))
    page_rank = nx.pagerank(DG)
    for twitter_id in DG.nodes():
        t = TwitterUser.get_by_id(twitter_id)
        node = DG.node[twitter_id]
        node['user_id'] = t.user_id
        node['label'] = t.scrn_name
        node['follower_count'] = t.foer_cnt
        node['friend_count'] = t.friend_cnt
        node['status_count'] = t.status_cnt
        node['location'] = t.location
        node['verified'] = t.verified
        node['twitter_age'] = (date.today() - t.created_at).days
        node['daily_tweet'] = t.status_cnt*1.0/node['twitter_age']
        node['indegree'] = len([(id, foer) for id, foer 
            in pair_list if id == twitter_id])
        node['outdegree'] = len([(id, foer) for id, foer 
            in pair_list if foer == twitter_id])
        node['cluster'] = clustering_co[twitter_id]
        node['betweenness'] = betweenness[twitter_id]
        node['closeness'] = closeness[twitter_id]
        node['page_rank'] = page_rank[twitter_id]
    for out_n, in_n in DG.edges():
        DG[out_n][in_n]['edge_betweenness'] = edge_betweenness[(out_n,in_n)]

    return DG

def build_graph_encoded():
    pair_list = TwitterUser.get_top_100_pair()
    print
    DG = nx.DiGraph()
    DG.add_edges_from(pair_list)
    for twitter_id in DG.nodes():
        t = TwitterUser.get_by_id(twitter_id)
        node = DG.node[twitter_id]
        node['twitter_id'] = t.user_id
        node['label'] = t.scrn_name.encode('utf-8')
        node['screen_name'] = t.scrn_name.encode('utf-8')
        node['name'] = t.name.encode('utf-8')
        node['follower_count'] = t.foer_cnt
        node['friend_count'] = t.friend_cnt
        node['status_count'] = t.status_cnt
        node['description']  = t.desc.encode('utf-8')
        node['location'] = t.location.encode('utf-8')
        node['created_at'] = str(t.created_at)
        node['verified'] = t.verified
        node['twitter_age'] = (date.today() - t.created_at).days
        node['daily_tweet'] = t.status_cnt*1.0/node['twitter_age']
        node['follower_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if id == twitter_id])
        node['friend_count_top100'] = len([(id, foer) for id, foer 
            in pair_list if foer == twitter_id])

    return DG
    
if __name__ == '__main__':
    G = build_graph()
    nx.write_graphml(G, 'twitter_paper.graphml')
    plt.draw()
