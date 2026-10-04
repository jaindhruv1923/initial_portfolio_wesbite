"""
Heterogeneous Graph & Recruitment Syndication Ring Detector
===========================================================
Constructs a multi-partite network of Employers, Requisitions, Locations,
and Shared Description Shingles using NetworkX.

Applies community detection (Greedy Modularity) and PageRank centrality
to identify coordinated phantom posting syndicates and recruiter rings.
"""

import os
import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, Any, List, Tuple

class RecruitmentSyndicationGraph:
    def __init__(self, similarity_threshold: float = 0.80):
        self.similarity_threshold = similarity_threshold
        self.G = nx.Graph()
        self.communities = []
        self.centrality_scores = {}

    def build_from_dataframe(self, df: pd.DataFrame) -> nx.Graph:
        """
        Builds the heterogeneous network from job listing records.
        """
        self.G.clear()
        
        # 1. Add Employer Nodes
        companies = df["company_name"].dropna().unique()
        for comp in companies:
            comp_str = str(comp).strip()
            if comp_str:
                self.G.add_node(comp_str, type="employer", label=comp_str)
                
        # 2. Add Location / Category bipartite edges
        for _, row in df.iterrows():
            comp = str(row.get("company_name", "")).strip()
            city = str(row.get("location_city", "")).strip()
            cat = str(row.get("job_category", "")).strip()
            
            if comp and city and city != "nan":
                city_node = f"City:{city}"
                if not self.G.has_node(city_node):
                    self.G.add_node(city_node, type="city", label=city)
                self.G.add_edge(comp, city_node, relation="LOCATED_IN", weight=1.0)
                
        # 3. Add Cross-Company Syndication Edges
        # If plagiarism or text shingle data is present
        plag_path = "data/cross_company_plagiarism.csv"
        if os.path.exists(plag_path):
            plag_df = pd.read_csv(plag_path)
            for _, r in plag_df.iterrows():
                c1 = str(r.get("company_1", r.get("company_name", ""))).strip()
                c2 = str(r.get("company_2", r.get("most_similar_company", ""))).strip()
                sim = float(r.get("cosine_similarity", r.get("cross_company_max_sim", 0.85)))
                
                if c1 and c2 and c1 != c2 and sim >= self.similarity_threshold:
                    if not self.G.has_node(c1):
                        self.G.add_node(c1, type="employer", label=c1)
                    if not self.G.has_node(c2):
                        self.G.add_node(c2, type="employer", label=c2)
                    self.G.add_edge(c1, c2, relation="SYNDICATES_WITH", weight=sim)
        else:
            # Deterministically link employers with identical boilerplate titles/cities
            emp_by_cat = df.groupby(["job_category", "location_city"])["company_name"].unique()
            for (cat, city), co_list in emp_by_cat.items():
                if len(co_list) >= 2 and len(co_list) <= 6:
                    for i in range(len(co_list)):
                        for j in range(i + 1, len(co_list)):
                            c1, c2 = str(co_list[i]).strip(), str(co_list[j]).strip()
                            if c1 and c2 and c1 != c2:
                                self.G.add_edge(c1, c2, relation="CO_LOCATED_CLUSTER", weight=0.82)
                                
        # 4. Compute PageRank centrality
        if len(self.G) > 0:
            try:
                self.centrality_scores = nx.pagerank(self.G, weight="weight", alpha=0.85, max_iter=200)
            except Exception:
                self.centrality_scores = {n: 1.0 / len(self.G) for n in self.G.nodes()}
                
        # 5. Community Detection for Ghost Rings
        # Extract employer-employer subgraph
        employer_nodes = [n for n, d in self.G.nodes(data=True) if d.get("type") == "employer"]
        subgraph = self.G.subgraph(employer_nodes)
        
        if len(subgraph) > 0 and subgraph.number_of_edges() > 0:
            try:
                from networkx.algorithms.community import greedy_modularity_communities
                raw_comm = greedy_modularity_communities(subgraph, weight="weight")
                self.communities = [list(c) for c in raw_comm if len(c) >= 2]
            except Exception:
                self.communities = [list(c) for c in nx.connected_components(subgraph) if len(c) >= 2]
                
        return self.G

    def get_syndication_summary(self) -> Dict[str, Any]:
        """Returns macro network statistics and top ghost syndication rings."""
        emp_nodes = [n for n, d in self.G.nodes(data=True) if d.get("type") == "employer"]
        synd_edges = [
            (u, v) for u, v, d in self.G.edges(data=True)
            if d.get("relation") == "SYNDICATES_WITH"
        ]
        
        # Rank top central employers in the syndication ring
        emp_centrality = {
            n: self.centrality_scores.get(n, 0.0) 
            for n in emp_nodes if n in self.centrality_scores
        }
        top_central = sorted(emp_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_nodes": self.G.number_of_nodes(),
            "total_edges": self.G.number_of_edges(),
            "employer_nodes_count": len(emp_nodes),
            "syndication_edges_count": len(synd_edges),
            "detected_rings_count": len(self.communities),
            "top_ringleader_employers": top_central,
            "largest_syndication_ring_size": max([len(c) for c in self.communities]) if self.communities else 0
        }

    def get_network_plot_data(self, max_nodes: int = 60) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Generates 2D spring layout coordinates for interactive Plotly rendering.
        """
        # Focus on the most connected employer nodes
        employer_nodes = [n for n, d in self.G.nodes(data=True) if d.get("type") == "employer"]
        degrees = dict(self.G.degree(employer_nodes))
        top_nodes = sorted(degrees, key=degrees.get, reverse=True)[:max_nodes]
        
        subG = self.G.subgraph(top_nodes)
        if len(subG) == 0:
            return [], []
            
        pos = nx.spring_layout(subG, k=0.35, seed=42)
        
        nodes_data = []
        for n in subG.nodes():
            x, y = pos[n]
            deg = subG.degree(n)
            pr = self.centrality_scores.get(n, 0.001)
            nodes_data.append({
                "id": n,
                "label": n,
                "x": float(x),
                "y": float(y),
                "degree": int(deg),
                "pagerank": float(pr),
                "size": max(10, min(35, deg * 4 + 8))
            })
            
        edges_data = []
        for u, v, d in subG.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edges_data.append({
                "source": u,
                "target": v,
                "x0": float(x0),
                "y0": float(y0),
                "x1": float(x1),
                "y1": float(y1),
                "relation": d.get("relation", "LINK")
            })
            
        return nodes_data, edges_data

# Singleton instance
syndication_graph = RecruitmentSyndicationGraph()
