from collections import Counter
import numpy as np

def entropy(y):
    hist = np.bincount(y)
    ps = hist / len(y)
    return -np.sum([p * np.log2(p) for p in ps if p > 0])
    
def most_common_label(y):
    counter_obj = Counter(y)
    value, _ = counter_obj.most_common(1)[0]
    return value

class Node:
    def __init__(self, left = None ,right = None, feature = None, threshold = None, value = None):
        self.left = left
        self.right = right
        self.feature = feature
        self.threshold = threshold 
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self) -> str:
        return str(self.feature) +" "+str(self.threshold)+" "+str(self.value)

class Decision_Tree:
    def __init__(self, max_depth = 100, min_samples_split = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None

    def fit(self, X_data, y_data):
        self.root = self.build_tree(X_data, y_data)

    def build_tree(self, X, y, depth = 0):
        n_labels = len(np.unique(y))
        if depth > self.max_depth or len(X) <= self.min_samples_split or n_labels == 1:
            value = most_common_label(y)
            return Node(value= value)
        
        feature, thresold = self.best_case(X, y)

        idx_left, idx_right = self.split_data(X, feature, thresold)
        
        print(len(idx_left),len(idx_right))
        
        if len(idx_left) == 0 or len(idx_right) == 0:
            value = most_common_label(y)
            return Node(value= value)

        node_left = self.build_tree(X[idx_left], y[idx_left], depth + 1)
        node_right = self.build_tree(X[idx_right], y[idx_right], depth + 1)

        return Node(left= node_left, right= node_right, feature= feature, threshold= thresold)

    def split_data(self, X, feature, thresold):
        idx_left = np.where(X[:,feature] <= thresold)[0]
        idx_right = np.where(X[:,feature] > thresold)[0]
        return idx_left, idx_right

    def gain(self, X, y, feature, thresold):
        idx_left, idx_right = self.split_data(X, feature, thresold)

        n = len(X)
        result = entropy(y) - len(idx_left)/n * entropy(y[idx_left]) - len(idx_right)/n * entropy(y[idx_right])
        return result


    def best_case(self, X, y):
        n_sample, n_features = X.shape

        gain_best = float('-inf')
        feature_best = 0
        thresold_best = 0

        for feature in range(n_features):
            data_feature = X[:,feature]
            uq_data = np.unique(data_feature)
            for thre in uq_data:
                gain = self.gain(X, y, feature, thre)
                if gain > gain_best:
                    gain_best = gain
                    feature_best = feature
                    thresold_best = thre
        return feature_best, thresold_best

    def predict(self, X):
        y_pre = [self.traversal_tree(i) for i in X]
        return np.array(y_pre)

    def traversal_tree(self, X, node = None):
        if node == None: node = self.root
        if node.get_value() != None:
            return node.get_value()
        elif X[node.feature] > node.threshold:
            return self.traversal_tree(X, node.right)
        else:
            return self.traversal_tree(X, node.left)