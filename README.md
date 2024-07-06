# Unsupervised Link Prediction 
A Python implementation of unsupervised link prediction problem using `NetworkX` library.


__`import` statements__:
```
from scoring_function import preferential_attachment
from data_splitting import k_fold_cross_validation, get_train_test_graphs_for, train_test_split
from evaluation import auc, precision
from link_prediction import edge_scoring, reverse_link_prediction
from networkx import karate_club_graph
from networkx import complement
```
## Normal Link Prediction or Positive Link Prediction (PLP)
### Train Test Split

```
g_karate = karate_club_graph()
g_train, g_test = train_test_split(g_karate)
scored_links = edge_scoring(g_train, preferential_attachment)
print('Precis ->', precision(g_test, scored_links))
print('AUC ->', auc(g_karate, g_train, g_test, preferential_attachment))
```

### K-Fold Cross Validation
```
g_karate = karate_club_graph()
k_fold_data = k_fold_cross_validation(g_karate, 3, True)
precision_list = []
auc_list = []
for fold_number, fold_edges in k_fold_data.items():
    train_graph, test_graph = get_train_test_graphs_for(g_karate, fold_edges)
    scored_links = edge_scoring(train_graph, preferential_attachment)
    precision_list.append(
        precision(test_graph, scored_links)
    )
    auc_list.append(
        auc(
            g_karate, train_graph, test_graph, preferential_attachment
        )
    )
final_precision = sum(precision_list) / len(precision_list)
final_auc = sum(auc_list) / len(auc_list)
print('Precis ->', final_precision)
print('AUC ->', final_auc)
```

## Reverse Link Prediction (RLP)
```
g_karate = karate_club_graph()
g_train, g_test = train_test_split(g_karate)
scored_links = reverse_link_prediction(g_train, preferential_attachment)
print('Precis ->', precision(g_test, scored_links))
print('AUC ->', auc(g_karate, g_train, g_test, preferential_attachment))
```

## Negative Link Prediction (NLP)
The NLP approach works similarly to the PLP approach and applies PLP to the complement graph. First, the graph must be complemented, and after that, the PLP approach is applied.
```
g_karate = karate_club_graph()
g_complemented = complement(graph)
g_train, g_test = train_test_split(g_complemented)
scored_links = edge_scoring(g_train, preferential_attachment)
print('Precis ->', precision(g_test, scored_links))
print('AUC ->', auc(g_complemented, g_train, g_test, preferential_attachment))
```