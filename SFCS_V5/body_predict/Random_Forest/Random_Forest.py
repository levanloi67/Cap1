from .Decision_Tree import *

def bootstrap_sample(X, y):
    n_samples = X.shape[0]
    idxs = np.random.choice(n_samples, n_samples, replace=True)
    return X[idxs], y[idxs]

class Random_Forest:
    def __init__(self, n_trees, max_depth= 100, min_samples_split= 2):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def fit(self, X_data, y_data):
        for i in range(self.n_trees):
            X_train ,y_train = bootstrap_sample(X_data, y_data)
            tree = Decision_Tree(max_depth= self.max_depth, min_samples_split= self.min_samples_split)
            tree.fit(X_train, y_train)
            self.trees.append(tree)
    
    def predict(self, X):
        y_pred = [tree.predict(X) for tree in self.trees]
        y_pred = np.swapaxes(y_pred, 0, 1)
        y_pred = [most_common_label(i) for i in y_pred]
        return y_pred
        
