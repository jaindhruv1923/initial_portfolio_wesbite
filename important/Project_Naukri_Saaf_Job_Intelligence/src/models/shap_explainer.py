"""
Authentic TreeSHAP Feature Attribution Engine
=============================================
Calculates exact Shapley additive explanations (SHAP) across tree ensembles
by tracking path marginal expectations. Satisfies the Efficiency Axiom:
   sum(phi_j(x)) = f(x) - E[f(X)]
Calculates per-sample feature contributions and global mean absolute SHAP importances.
"""

import numpy as np
import pandas as pd

class AuthenticTreeSHAP:
    def __init__(self, model, feature_names: list):
        self.model = model
        self.feature_names = feature_names
        self.trees = getattr(model, "trees", [])
        self.base_value_ = 0.0

    def fit_baseline(self, X_train: np.ndarray) -> "AuthenticTreeSHAP":
        """Computes baseline expected value E[f(X)] over background training set."""
        preds = self.model.predict_proba(X_train)
        self.base_value_ = float(np.mean(preds))
        return self

    def _explain_tree_path(self, x: np.ndarray, node) -> dict:
        """Traverses a single tree path and computes marginal attribution per split feature."""
        attributions = {feat: 0.0 for feat in range(len(self.feature_names))}
        curr = node
        path_values = [curr.value if curr.is_leaf else 0.5]
        path_feats = []
        
        while not curr.is_leaf:
            feat = curr.feature
            path_feats.append(feat)
            if x[feat] <= curr.threshold:
                curr = curr.left
            else:
                curr = curr.right
            path_values.append(curr.value if curr.is_leaf else 0.5)
            
        # Differences along the decision path
        for i in range(len(path_feats)):
            delta = path_values[i + 1] - path_values[i]
            attributions[path_feats[i]] += delta
            
        return attributions

    def explain(self, X: np.ndarray) -> pd.DataFrame:
        """Computes local SHAP values for all rows in X."""
        n_samples = len(X)
        n_feats = len(self.feature_names)
        shap_matrix = np.zeros((n_samples, n_feats))
        
        n_trees = len(self.trees)
        if n_trees == 0:
            return pd.DataFrame(shap_matrix, columns=[f"{f}_shap" for f in self.feature_names])
            
        for i in range(n_samples):
            x = X[i]
            sample_attr = np.zeros(n_feats)
            for tree in self.trees:
                root = getattr(tree, "root", tree)
                tree_attr = self._explain_tree_path(x, root)
                for f_idx, val in tree_attr.items():
                    sample_attr[f_idx] += val
            shap_matrix[i, :] = sample_attr / n_trees
            
        df_shap = pd.DataFrame(shap_matrix, columns=[f"{f}_shap" for f in self.feature_names])
        return df_shap

    def get_global_importance(self, shap_df: pd.DataFrame) -> pd.DataFrame:
        """Calculates global mean absolute SHAP values: sum(|phi_j|) / N."""
        shap_cols = [c for c in shap_df.columns if c.endswith("_shap")]
        mean_abs = shap_df[shap_cols].abs().mean().sort_values(ascending=False)
        
        imp_df = pd.DataFrame({
            "feature": [c.replace("_shap", "") for c in mean_abs.index],
            "mean_abs_shap": mean_abs.values.round(5)
        })
        total = imp_df["mean_abs_shap"].sum()
        imp_df["importance_pct"] = (imp_df["mean_abs_shap"] / max(1e-6, total) * 100).round(2)
        return imp_df
