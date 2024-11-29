from typing import List

import numpy as np


class RetrievalEvaluator:
    def __init__(self, retrieved: List[str], relevant: List[str]):
        """
        Initialize the RetrievalEvaluator with retrieved and relevant documents.

        Args:
            retrieved (List[str]): List of retrieved document IDs.
            relevant (List[str]): List of relevant document IDs.
        """
        self.retrieved = retrieved
        self.relevant = relevant
        self.retrieved_set = set(retrieved)
        self.relevant_set = set(relevant)
        self.num_relevant = len(relevant)

    def hit_rate_at_k(self, k: int) -> float:
        """
        Calculate the hit rate at rank k.

        Args:
            k (int): Rank position for hit rate calculation.

        Returns:
            float: Hit rate as a fraction at rank k.
        """
        top_k_retrieved = set(self.retrieved[:k])
        relevant_retrieved = self.relevant_set & top_k_retrieved
        if not top_k_retrieved:
            return 0.0
        return len(relevant_retrieved) / len(top_k_retrieved)

    def precision(self) -> float:
        """
        Calculate Precision of the retrieved documents.

        Returns:
            float: Precision score.
        """
        true_positives = len(self.retrieved_set & self.relevant_set)
        if len(self.retrieved) == 0:
            return 0.0
        return true_positives / len(self.retrieved)

    def recall(self) -> float:
        """
        Calculate Recall of the retrieved documents.

        Returns:
            float: Recall score.
        """
        true_positives = len(self.retrieved_set & self.relevant_set)
        if self.num_relevant == 0:
            return 0.0
        return true_positives / self.num_relevant

    def f1_score(self) -> float:
        """
        Calculate F1-Score of the retrieved documents.

        Returns:
            float: F1-Score.
        """
        prec = self.precision()
        rec = self.recall()
        if prec + rec == 0:
            return 0.0
        return 2 * (prec * rec) / (prec + rec)

    def average_precision(self) -> float:
        """
        Calculate Average Precision (AP) for the retrieved documents.

        Returns:
            float: Average Precision score.
        """
        num_relevant = 0
        precision_sum = 0.0
        for i, doc in enumerate(self.retrieved):
            if doc in self.relevant_set:
                num_relevant += 1
                precision_sum += num_relevant / (i + 1)
        if num_relevant == 0:
            return 0.0
        return precision_sum / num_relevant

    @staticmethod
    def mean_average_precision(retrievals: List[List[str]], relevant_docs: List[List[str]]) -> float:
        """
        Calculate Mean Average Precision (MAP) for multiple queries.

        Args:
            retrievals (List[List[str]]): List of lists of retrieved document IDs for multiple queries.
            relevant_docs (List[List[str]]): List of lists of relevant document IDs for multiple queries.

        Returns:
            float: Mean Average Precision score.
        """
        ap_sum = 0.0
        for retrieved, relevant in zip(retrievals, relevant_docs):
            evaluator = RetrievalEvaluator(retrieved, relevant)
            ap_sum += evaluator.average_precision()
        return ap_sum / len(retrievals)

    def reciprocal_rank(self) -> float:
        """
        Calculate Reciprocal Rank (RR) of the retrieved documents.

        Returns:
            float: Reciprocal Rank score.
        """
        for i, doc in enumerate(self.retrieved):
            if doc in self.relevant_set:
                return 1 / (i + 1)
        return 0.0

    @staticmethod
    def mean_reciprocal_rank(retrievals: List[List[str]], relevant_docs: List[List[str]]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR) for multiple queries.

        Args:
            retrievals (List[List[str]]): List of lists of retrieved document IDs for multiple queries.
            relevant_docs (List[List[str]]): List of lists of relevant document IDs for multiple queries.

        Returns:
            float: Mean Reciprocal Rank score.
        """
        mrr_sum = 0.0
        for retrieved, relevant in zip(retrievals, relevant_docs):
            evaluator = RetrievalEvaluator(retrieved, relevant)
            mrr_sum += evaluator.reciprocal_rank()
        return mrr_sum / len(retrievals)

    def dcg(self) -> float:
        """
        Calculate Discounted Cumulative Gain (DCG) for the retrieved documents.

        Returns:
            float: Discounted Cumulative Gain score.
        """
        gains = [1 if doc in self.relevant_set else 0 for doc in self.retrieved]
        discounts = [np.log2(i + 2) for i in range(len(self.retrieved))]
        return sum(g / d for g, d in zip(gains, discounts))

    def idcg(self, k: int) -> float:
        """
        Calculate Ideal Discounted Cumulative Gain (IDCG) at rank k.

        Args:
            k (int): Rank position for IDCG calculation.

        Returns:
            float: Ideal Discounted Cumulative Gain score.
        """
        sorted_relevant = sorted(self.relevant, reverse=True)[:k]
        evaluator = RetrievalEvaluator(sorted_relevant, sorted_relevant)
        return evaluator.dcg()

    def ndcg(self, k: int) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain (NDCG) at rank k.

        Args:
            k (int): Rank position for NDCG calculation.

        Returns:
            float: Normalized Discounted Cumulative Gain score.
        """
        dcg_score = self.dcg()
        idcg_score = self.idcg(k)
        if idcg_score == 0:
            return 0.0
        return dcg_score / idcg_score

    def recall_at_k(self, k: int) -> float:
        """
        Calculate Recall at rank k.

        Args:
            k (int): Rank position for recall calculation.

        Returns:
            float: Recall score at rank k.
        """
        retrieved_at_k = self.retrieved[:k]
        retrieved_at_k_set = set(retrieved_at_k)
        true_positives = len(retrieved_at_k_set & self.relevant_set)
        if self.num_relevant == 0:
            return 0.0
        return true_positives / self.num_relevant

    def precision_at_k(self, k: int) -> float:
        """
        Calculate Precision at rank k.

        Args:
            k (int): Rank position for precision calculation.

        Returns:
            float: Precision score at rank k.
        """
        retrieved_at_k = self.retrieved[:k]
        if len(retrieved_at_k) == 0:
            return 0.0
        return len(set(retrieved_at_k) & self.relevant_set) / len(retrieved_at_k)

    def average_precision_at_k(self, k: int) -> float:
        """
        Calculate Average Precision at rank k.

        Args:
            k (int): Rank position for average precision calculation.

        Returns:
            float: Average Precision score at rank k.
        """
        relevant_set = set(self.relevant)
        precision_sum = 0.0
        num_relevant = 0
        for i in range(k):
            if i >= len(self.retrieved):
                break
            if self.retrieved[i] in relevant_set:
                num_relevant += 1
                precision_sum += num_relevant / (i + 1)
        if num_relevant == 0:
            return 0.0
        return precision_sum / min(self.num_relevant, k)

    def r_precision(self) -> float:
        """
        Calculate R-Precision, which is precision when the number of retrieved documents equals the number of relevant documents.

        Returns:
            float: R-Precision score.
        """
        if self.num_relevant == 0:
            return 0.0
        return self.precision_at_k(self.num_relevant)
