import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

edges = [
    ('S', 'K', '0'),
    ('K', 'M', '1'),
    ('L', 'K', '0'),
    ('M', 'R', '1'),
    ('M', 'R', '0'),
    ('N', 'M', '1'),
    ('O', 'N', '0'),
    ('Q', 'R', '0'),
    ('T', 'Q', '1'),
    ('T', 'U', ')'),
    ('R', 'L', '#'),
    ('R', 'U', ')'),
    ('R', 'O', '~'),
    ('P', 'R', '1'),
    ('F', 'P', '0'),
    ('F', 'U', ')')
]

# Добавление ребер в граф
for (u, v, label) in edges:
    G.add_edge(u, v, label=label)

# Позиционирование узлов
pos = nx.spring_layout(G)

# Отрисовка графа
plt.figure(figsize=(12, 8))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=16, font_weight='bold', arrows=True)

# Отрисовка подписей ребер
edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12, font_color='red')

plt.title('Ориентированный граф с подписанными ребрами')
plt.show()