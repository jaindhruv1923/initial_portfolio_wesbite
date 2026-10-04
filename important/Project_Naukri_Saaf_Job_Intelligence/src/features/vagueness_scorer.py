"""
Job Description Vagueness & Generic Fluff Scorer
================================================
Quantifies syntactic and semantic vagueness in job descriptions.

Genuine technical job listings feature high densities of concrete tools,
frameworks, explicit qualifications, and active measurable verbs.
Ghost postings and placeholder listings typically rely on corporate buzzwords,
vague cliches ("rockstar", "wear many hats"), and low concrete entity density.
"""

import re
import numpy as np
import pandas as pd

class VaguenessScorer:
    def __init__(self):
        # Concrete technical skills & credentials
        self.tech_entities = {
            "python", "java", "c++", "c#", "go", "golang", "rust", "sql", "nosql",
            "javascript", "typescript", "r", "scala", "bash", "linux", "git",
            "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
            "docker", "kubernetes", "k8s", "terraform", "aws", "azure", "gcp",
            "spark", "kafka", "hadoop", "airflow", "snowflake", "bigquery", "postgres",
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "pytorch",
            "tensorflow", "scikit-learn", "keras", "pandas", "numpy", "tableau",
            "power bi", "excel", "ci/cd", "rest api", "graphql", "microservices",
            "bachelor", "master", "phd", "b.tech", "m.tech", "degree", "certification"
        }
        
        # Corporate buzzwords & filler phrases
        self.buzzword_patterns = [
            r"\brockstar\b", r"\bninja\b", r"\bguru\b", r"\bwizard\b",
            r"\bwear (?:many|multiple) hats\b",
            r"\bfast[- ]paced (?:environment|culture)\b",
            r"\bdynamic (?:environment|team|culture)\b",
            r"\bself[- ]starter\b", r"\bhit the ground running\b",
            r"\bgo[- ]getter\b", r"\bteam player\b",
            r"\bcollaborative synergy\b", r"\bpassion for excellence\b",
            r"\bresults[- ]driven\b", r"\bwork hard play hard\b",
            r"\bdeep dive\b", r"\bmove the needle\b",
            r"\bthought leadership\b", r"\bseamless(?:ly)?\b",
            r"\bparadigm shift\b", r"\bout[- ]of[- ]the[- ]box\b",
            r"\bworld[- ]class\b", r"\bdisrupt(?:ive)?\b",
            r"\bproven track record\b", r"\beverything in between\b"
        ]
        self.buzzword_regex = re.compile("|".join(self.buzzword_patterns), re.IGNORECASE)
        
        # Vague vs Concrete verbs
        self.concrete_verbs = {
            "architect", "architected", "build", "built", "design", "designed",
            "develop", "developed", "deploy", "deployed", "implement", "implemented",
            "optimize", "optimized", "refactor", "refactored", "benchmark", "benchmarked",
            "automate", "automated", "integrate", "integrated", "configure", "configured"
        }
        self.vague_verbs = {
            "assist", "assisted", "support", "supported", "help", "helped",
            "handle", "handled", "participate", "participated", "contribute", "contributed",
            "involve", "involved", "oversee", "overseeing", "work with", "coordinate"
        }

    def score_text(self, text: str) -> dict:
        if not isinstance(text, str) or len(text.strip()) == 0:
            return {
                "concrete_tech_density": 0.0,
                "buzzword_density": 0.0,
                "concrete_to_vague_verb_ratio": 0.5,
                "bullet_point_density": 0.0,
                "jd_vagueness_index": 0.85
            }
            
        lower_text = text.lower()
        words = re.findall(r"\b[a-z0-9+#.-]+\b", lower_text)
        word_count = max(1, len(words))
        
        # 1. Concrete tech entities count
        tech_count = sum(1 for w in words if w in self.tech_entities)
        # Check compound phrases
        if "power bi" in lower_text:
            tech_count += 1
        if "ci/cd" in lower_text:
            tech_count += 1
        tech_density = (tech_count / word_count) * 100.0  # per 100 words
        
        # 2. Buzzword density
        buzzwords_found = len(self.buzzword_regex.findall(text))
        buzzword_density = (buzzwords_found / word_count) * 100.0
        
        # 3. Action Verb Specificity
        n_concrete = sum(1 for w in words if w in self.concrete_verbs)
        n_vague = sum(1 for w in words if w in self.vague_verbs)
        verb_ratio = (n_concrete + 1.0) / (n_concrete + n_vague + 2.0)
        
        # 4. Bullet point density (structured lists vs walls of text)
        lines = text.split("\n")
        bullet_lines = sum(1 for line in lines if line.strip().startswith(("-", "*", "•", "1.", "2.", "3.", "4.")))
        bullet_density = bullet_lines / max(1, len(lines))
        
        # 5. Composite Vagueness Index (0.0 to 1.0)
        # Higher score = more vague/fluff/ghost
        # Low tech density (< 2 per 100 words), high buzzwords, low verb ratio, low bullets
        norm_tech = np.clip(1.0 - (tech_density / 5.0), 0.0, 1.0)
        norm_buzz = np.clip(buzzword_density / 1.5, 0.0, 1.0)
        norm_verb = np.clip(1.0 - verb_ratio, 0.0, 1.0)
        norm_bullet = np.clip(1.0 - bullet_density, 0.0, 1.0)
        
        vagueness_index = (
            0.40 * norm_tech +
            0.25 * norm_buzz +
            0.20 * norm_verb +
            0.15 * norm_bullet
        )
        
        return {
            "concrete_tech_density": round(float(tech_density), 4),
            "buzzword_density": round(float(buzzword_density), 4),
            "concrete_to_vague_verb_ratio": round(float(verb_ratio), 4),
            "bullet_point_density": round(float(bullet_density), 4),
            "jd_vagueness_index": round(float(vagueness_index), 4)
        }

    def score_dataframe(self, df: pd.DataFrame, text_col: str = "job_description") -> pd.DataFrame:
        results = [self.score_text(t) for t in df[text_col]]
        res_df = pd.DataFrame(results)
        res_df.insert(0, "listing_id", df["listing_id"].values)
        return res_df
