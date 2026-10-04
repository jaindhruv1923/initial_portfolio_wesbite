"""
Vectorized High-Performance Machine Learning Classifiers (Pure NumPy/SciPy)
==========================================================================
Engineered for zero-dependency portability and hardened against OS-level
Application Control policies.
Includes:
  1. NumPyLogisticRegression (L2 regularized, class-balanced)
  2. NumPyDecisionTree (Gini / MSE split search with min_samples_leaf & max_depth)
  3. NumPyRandomForest (Bootstrap bagged ensemble with sqrt(p) feature subspace)
  4. NumPyGradientBoosting (Log-loss pseudo-residual boosting with shrinkage)
  5. NumPyStackingClassifier (Stacking meta-learner)
"""

import numpy as np

class NumPyLogisticRegression:
    def __init__(self, lr: float = 0.05, max_iter: int = 400, l2_reg: float = 0.1, class_weight: str = "balanced"):
        self.lr = lr
        self.max_iter = max_iter
        self.l2_reg = l2_reg
        self.class_weight = class_weight
        self.weights = None
        self.bias = 0.0
        self.mean_ = None
        self.std_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "NumPyLogisticRegression":
        # Feature standardization
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        self.std_[self.std_ == 0] = 1.0
        X_scaled = (X - self.mean_) / self.std_
        
        n_samples, n_features = X_scaled.shape
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        
        # Sample weights for class imbalance
        if self.class_weight == "balanced":
            pos_ratio = np.mean(y == 1)
            sample_weights = np.where(y == 1, 0.5 / max(pos_ratio, 1e-4), 0.5 / max(1.0 - pos_ratio, 1e-4))
        else:
            sample_weights = np.ones(n_samples)
            
        # Vectorized Gradient Descent
        for _ in range(self.max_iter):
            linear = np.dot(X_scaled, self.weights) + self.bias
            # Stable sigmoid
            probs = np.where(linear >= 0, 1.0 / (1.0 + np.exp(-linear)), np.exp(linear) / (1.0 + np.exp(linear)))
            errors = (probs - y) * sample_weights
            
            dw = (np.dot(X_scaled.T, errors) / n_samples) + (self.l2_reg * self.weights)
            db = np.mean(errors)
            
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
            
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        X_scaled = (X - self.mean_) / self.std_
        linear = np.dot(X_scaled, self.weights) + self.bias
        probs = np.where(linear >= 0, 1.0 / (1.0 + np.exp(-linear)), np.exp(linear) / (1.0 + np.exp(linear)))
        return probs

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    @property
    def is_leaf(self):
        return self.value is not None


class NumPyDecisionTree:
    def __init__(self, max_depth: int = 5, min_samples_split: int = 10, min_samples_leaf: int = 5, max_features=None, criterion="gini"):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.criterion = criterion
        self.root = None

    def fit(self, X: np.ndarray, y: np.ndarray, sample_weight=None) -> "NumPyDecisionTree":
        self.root = self._build_tree(X, y, depth=0, sample_weight=sample_weight)
        return self

    def _build_tree(self, X: np.ndarray, y: np.ndarray, depth: int, sample_weight=None):
        n_samples, n_feats = X.shape
        
        # Stopping criteria
        if depth >= self.max_depth or n_samples < self.min_samples_split or len(np.unique(y)) == 1:
            leaf_val = np.average(y, weights=sample_weight) if sample_weight is not None else np.mean(y)
            return Node(value=leaf_val)
            
        # Select feature subset
        if self.max_features == "sqrt":
            feat_count = max(1, int(np.sqrt(n_feats)))
            feat_indices = np.random.choice(n_feats, feat_count, replace=False)
        elif isinstance(self.max_features, float):
            feat_count = max(1, int(self.max_features * n_feats))
            feat_indices = np.random.choice(n_feats, feat_count, replace=False)
        else:
            feat_indices = np.arange(n_feats)
            
        best_feat, best_thresh, best_gain = None, None, -1.0
        
        # Current impurity
        if self.criterion == "gini":
            p = np.mean(y)
            current_imp = 1.0 - (p**2 + (1.0 - p)**2)
        else: # mse for boosting residuals
            current_imp = np.var(y)
            
        for feat in feat_indices:
            vals = X[:, feat]
            # Use percentiles for fast split finding
            candidates = np.percentile(vals, np.linspace(10, 90, 12))
            candidates = np.unique(candidates)
            
            for t in candidates:
                left_mask = vals <= t
                right_mask = ~left_mask
                
                n_l, n_r = np.sum(left_mask), np.sum(right_mask)
                if n_l < self.min_samples_leaf or n_r < self.min_samples_leaf:
                    continue
                    
                y_l, y_r = y[left_mask], y[right_mask]
                if self.criterion == "gini":
                    p_l = np.mean(y_l)
                    imp_l = 1.0 - (p_l**2 + (1.0 - p_l)**2)
                    p_r = np.mean(y_r)
                    imp_r = 1.0 - (p_r**2 + (1.0 - p_r)**2)
                else:
                    imp_l = np.var(y_l)
                    imp_r = np.var(y_r)
                    
                gain = current_imp - ((n_l / n_samples) * imp_l + (n_r / n_samples) * imp_r)
                if gain > best_gain:
                    best_gain = gain
                    best_feat = feat
                    best_thresh = t
                    
        if best_gain <= 0.0 or best_feat is None:
            leaf_val = np.average(y, weights=sample_weight) if sample_weight is not None else np.mean(y)
            return Node(value=leaf_val)
            
        left_mask = X[:, best_feat] <= best_thresh
        left_child = self._build_tree(X[left_mask], y[left_mask], depth + 1, sample_weight[left_mask] if sample_weight is not None else None)
        right_child = self._build_tree(X[~left_mask], y[~left_mask], depth + 1, sample_weight[~left_mask] if sample_weight is not None else None)
        
        return Node(feature=best_feat, threshold=best_thresh, left=left_child, right=right_child)

    def predict_one(self, x: np.ndarray, node: Node) -> float:
        if node.is_leaf:
            return node.value
        if x[node.feature] <= node.threshold:
            return self.predict_one(x, node.left)
        return self.predict_one(x, node.right)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self.predict_one(x, self.root) for x in X])


class NumPyRandomForest:
    def __init__(self, n_estimators: int = 80, max_depth: int = 7, min_samples_leaf: int = 4, max_features="sqrt", random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.trees = []
        self.feature_importances_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "NumPyRandomForest":
        rng = np.random.RandomState(self.random_state)
        n_samples, n_feats = X.shape
        self.trees = []
        
        # Calculate balanced sample weights
        pos_ratio = np.mean(y == 1)
        w1 = 0.5 / max(pos_ratio, 1e-4)
        w0 = 0.5 / max(1.0 - pos_ratio, 1e-4)
        weights = np.where(y == 1, w1, w0)
        
        feat_counts = np.zeros(n_feats)
        for _ in range(self.n_estimators):
            boot_idx = rng.choice(n_samples, size=n_samples, replace=True)
            X_b, y_b = X[boot_idx], y[boot_idx]
            w_b = weights[boot_idx]
            
            tree = NumPyDecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_leaf * 2,
                min_samples_leaf=self.min_samples_leaf,
                max_features=self.max_features,
                criterion="gini"
            )
            tree.fit(X_b, y_b, sample_weight=w_b)
            self.trees.append(tree)
            
            # Feature usage counter
            def count_features(node):
                if node and not node.is_leaf:
                    feat_counts[node.feature] += 1
                    count_features(node.left)
                    count_features(node.right)
            count_features(tree.root)
            
        total_splits = np.sum(feat_counts)
        self.feature_importances_ = feat_counts / max(1, total_splits)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        all_preds = np.array([tree.predict(X) for tree in self.trees])
        return np.mean(all_preds, axis=0)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)


class NumPyGradientBoosting:
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.08, max_depth: int = 4, subsample: float = 0.8, min_samples_leaf: int = 5, random_state: int = 42):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.subsample = subsample
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.trees = []
        self.init_log_odds = 0.0
        self.feature_importances_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "NumPyGradientBoosting":
        rng = np.random.RandomState(self.random_state)
        n_samples, n_feats = X.shape
        
        # Initial prediction: log(prior / (1 - prior))
        p_base = np.clip(np.mean(y), 1e-4, 1.0 - 1e-4)
        self.init_log_odds = np.log(p_base / (1.0 - p_base))
        
        F = np.full(n_samples, self.init_log_odds)
        self.trees = []
        feat_counts = np.zeros(n_feats)
        
        for _ in range(self.n_estimators):
            # Compute negative gradient of binary log-loss: y - p
            p = 1.0 / (1.0 + np.exp(-F))
            residuals = y - p
            
            # Subsampling
            if self.subsample < 1.0:
                sub_idx = rng.choice(n_samples, size=int(n_samples * self.subsample), replace=False)
                X_step, res_step = X[sub_idx], residuals[sub_idx]
            else:
                X_step, res_step = X, residuals
                
            tree = NumPyDecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_leaf * 2,
                min_samples_leaf=self.min_samples_leaf,
                max_features=0.8,
                criterion="mse"
            )
            tree.fit(X_step, res_step)
            self.trees.append(tree)
            
            # Update predictions with shrinkage
            update = tree.predict(X)
            F += self.learning_rate * update
            
            def count_features(node):
                if node and not node.is_leaf:
                    feat_counts[node.feature] += 1
                    count_features(node.left)
                    count_features(node.right)
            count_features(tree.root)
            
        total_splits = np.sum(feat_counts)
        self.feature_importances_ = feat_counts / max(1, total_splits)
        return self

    def predict_log_odds(self, X: np.ndarray) -> np.ndarray:
        F = np.full(len(X), self.init_log_odds)
        for tree in self.trees:
            F += self.learning_rate * tree.predict(X)
        return F

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        F = self.predict_log_odds(X)
        return 1.0 / (1.0 + np.exp(-F))

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)


class NumPyStackingClassifier:
    def __init__(self, base_models: dict, meta_lr: float = 0.1):
        self.base_models = base_models
        self.meta_model = NumPyLogisticRegression(lr=meta_lr, max_iter=250, l2_reg=0.2)

    def fit(self, X: np.ndarray, y: np.ndarray) -> "NumPyStackingClassifier":
        meta_features = []
        for name, model in self.base_models.items():
            model.fit(X, y)
            probs = model.predict_proba(X)
            meta_features.append(probs)
            
        S = np.column_stack(meta_features)
        self.meta_model.fit(S, y)
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        meta_features = [model.predict_proba(X) for model in self.base_models.values()]
        S = np.column_stack(meta_features)
        return self.meta_model.predict_proba(S)

    def predict(self, X: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_proba(X) >= threshold).astype(int)
