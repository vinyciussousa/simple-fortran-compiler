from grammar import Grammar
from predict import predict_algorithm


def is_ll1(G: Grammar, pred_alg: predict_algorithm) -> bool:
    for A in G.nonterminals():
        pred_set = set()
        # print(f'Veryfing for {A}')
        for p in G.productions_for(A):
            pred = pred_alg.predict(p)
            # print(f'Rule {G.lhs(p)} -> {G.rhs(p)} has {pred} as prediction')
            # print(f'{pred} and {pred_set}')
            if not pred_set.isdisjoint(pred):
                # print('Problem here')
                return False
            pred_set.update(pred)
    return True
