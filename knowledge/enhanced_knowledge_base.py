"""
Enhanced Knowledge Base Module for EXECAI Platform.

This module provides a comprehensive knowledge base with modular domain-specific
knowledge retrieval capabilities for the EXECAI Platform.
"""

import os
import json
from datetime import datetime
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EnhancedKnowledgeBase:
    """
    Enhanced Knowledge Base with modular domain-specific knowledge retrieval.
    
    This class manages the knowledge corpus and provides methods for querying
    and retrieving knowledge across different domains and capabilities.
    """
    
    def __init__(self):
        """Initialize the Enhanced Knowledge Base."""
        # Load knowledge domains
        self.domains = self._load_knowledge_domains()
        
        # Load knowledge corpus
        self.corpus = self._load_knowledge_corpus()
        
        # Initialize TF-IDF vectorizer for semantic search
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._initialize_vectorizer()
    
    def _load_knowledge_domains(self):
        """Load knowledge domains from configuration."""
        # In a production environment, this would load from a database or file
        # For now, we'll use hardcoded domains
        return [
            {
                'id': 'business',
                'name': 'Business Mentorship',
                'description': 'MBA-level business knowledge, frameworks, and mentorship',
                'icon': 'briefcase',
                'capabilities': ['strategic_advice', 'business_modeling', 'founder_mentorship', 'case_analysis']
            },
            {
                'id': 'finance',
                'name': 'Financial Analysis',
                'description': 'CFO-level financial reasoning and mathematical problem-solving',
                'icon': 'calculator',
                'capabilities': ['financial_analysis', 'math_problem_solving', 'statistical_reasoning']
            },
            {
                'id': 'tech',
                'name': 'Technical Development',
                'description': 'CTO-level technical guidance and code expertise',
                'icon': 'code',
                'capabilities': ['code_generation', 'architecture_design', 'technical_review']
            },
            {
                'id': 'legal',
                'name': 'Legal Contracts',
                'description': 'Legal contract patterns and analysis',
                'icon': 'file-text',
                'capabilities': ['contract_analysis', 'legal_risk_assessment', 'term_evaluation']
            },
            {
                'id': 'speech',
                'name': 'Speech Recognition',
                'description': 'Voice interaction and transcription capabilities',
                'icon': 'mic',
                'capabilities': ['speech_recognition', 'audio_processing', 'language_detection']
            }
        ]
    
    def _load_knowledge_corpus(self):
        """Load knowledge corpus from configuration."""
        # In a production environment, this would load from a database or file
        # For now, we'll use hardcoded knowledge items
        return [
            {
                'id': 'bm001',
                'title': 'Business Model Canvas',
                'description': 'Strategic management template for developing new or documenting existing business models',
                'content': "The Business Model Canvas is a strategic management template used for developing new business models or documenting existing ones. It offers a visual chart with elements describing a firm's value proposition, infrastructure, customers, and finances, helping businesses align their activities by illustrating potential trade-offs. The nine building blocks are: Customer Segments, Value Propositions, Channels, Customer Relationships, Revenue Streams, Key Resources, Key Activities, Key Partnerships, and Cost Structure.",
                'categories': ['strategy', 'business_model', 'planning'],
                'keywords': ['business model', 'canvas', 'value proposition', 'customer segments', 'revenue streams'],
                'source': 'Harvard Business School',
                'domain': 'business',
                'capabilities': ['strategic_advice', 'business_modeling'],
                'relevance': 0.95
            },
            {
                'id': 'bm002',
                'title': 'Lean Canvas',
                'description': 'Adaptation of Business Model Canvas for lean startups',
                'content': "Lean Canvas is a 1-page business plan template created by Ash Maurya that helps you deconstruct your idea into its key assumptions. It's adapted from Alex Osterwalder's Business Model Canvas and optimized for Lean Startups. It replaces elaborate business plans with a single page business model. The nine blocks are: Problem, Solution, Key Metrics, Unique Value Proposition, Unfair Advantage, Channels, Customer Segments, Cost Structure, and Revenue Streams. It focuses on problems, solutions, key metrics, and competitive advantages.",
                'categories': ['lean_startup', 'business_model', 'planning'],
                'keywords': ['lean', 'startup', 'canvas', 'business model', 'validation'],
                'source': 'Lean Startup corpus',
                'domain': 'business',
                'capabilities': ['strategic_advice', 'business_modeling', 'founder_mentorship'],
                'relevance': 0.85
            },
            # (Additional corpus items omitted for brevity)
        ]
    
    def _initialize_vectorizer(self):
        """Initialize the TF-IDF vectorizer with the knowledge corpus."""
        # Extract content from corpus for vectorization
        corpus_content = [item['content'] for item in self.corpus]
        
        # Fit the vectorizer on the corpus content
        self.content_matrix = self.vectorizer.fit_transform(corpus_content)
    
    def get_domains(self):
        """Get all available knowledge domains."""
        return self.domains
    
    def query(self, query, domains=None, capabilities=None):
        """
        Query the knowledge base with specific parameters.
        
        Args:
            query (str): The query string to search for.
            domains (list, optional): List of domain IDs to filter by.
            capabilities (list, optional): List of capability IDs to filter by.
            
        Returns:
            dict: Query results with matching knowledge items and metadata.
        """
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(query_vector, self.content_matrix).flatten()
        
        # Get indices of items sorted by similarity score (descending)
        sorted_indices = similarity_scores.argsort()[::-1]
        
        # Filter corpus items based on domains and capabilities
        filtered_items = []
        for idx in sorted_indices:
            item = self.corpus[idx]
            score = similarity_scores[idx]
            
            # Skip items with low relevance
            if score < 0.1:
                continue
            
            # Apply domain filter if specified
            if domains and item['domain'] not in domains:
                continue
            
            # Apply capability filter if specified
            if capabilities and not any(cap in item['capabilities'] for cap in capabilities):
                continue
            
            # Add similarity score to item
            item_copy = item.copy()
            item_copy['similarity_score'] = float(score)
            
            filtered_items.append(item_copy)
            
            # Limit to top 5 results
            if len(filtered_items) >= 5:
                break
        
        # Prepare response
        response = {
            'items': filtered_items,
            'sources': [
                {
                    'module_id': 'enhanced-knowledge-base',
                    'module_type': 'EnhancedKnowledgeBase',
                    'version': '1.0.0'
                }
            ],
            'metadata': {
                'query': query,
                'domains': domains,
                'capabilities': capabilities,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return response
    
    def get_strategic_insights(self, query):
        """
        Get strategic insights based on query.
        
        Args:
            query (str): The query string to analyze.
            
        Returns:
            list: Strategic insights relevant to the query.
        """
        # In a production environment, this would use more sophisticated
        # analysis to determine relevant insights
        query_lower = query.lower()
        
        # Default topic
        topic = 'business_model'
        
        # Determine topic based on keywords in query
        if any(kw in query_lower for kw in ['fundrais', 'investor', 'capital', 'money', 'funding']):
            topic = 'fundraising'
        elif any(kw in query_lower for kw in ['product', 'mvp', 'develop', 'feature']):
            topic = 'product_development'
        elif any(kw in query_lower for kw in ['team', 'hire', 'talent', 'employee']):
            topic = 'team_building'
        elif any(kw in query_lower for kw in ['dao', 'governance', 'token', 'blockchain']):
            topic = 'dao_governance'
        elif any(kw in query_lower for kw in ['growth', 'scale', 'market', 'customer']):
            topic = 'growth_strategy'
        
        # Return insights based on topic
        insights = self._get_insights_by_topic(topic)
        return insights
    
    def _get_insights_by_topic(self, topic):
        """Get strategic insights for a specific topic."""
        # Strategic insights by topic
        insights_by_topic = {
            'business_model': [
                "When designing your business model, focus on creating a sustainable competitive advantage that's difficult for competitors to replicate. This might come from proprietary technology, network effects, or unique partnerships.",
                "The most resilient business models have multiple revenue streams that complement each other and create a flywheel effect. Consider how each revenue source can strengthen the others.",
                "Don't just copy existing business models in your industry. The most innovative companies often combine elements from different industries to create something unique.",
                "Your business model should evolve as you grow. What works at the seed stage may not be optimal at Series A or beyond. Plan for this evolution from the beginning."
            ],
            # (Other topics omitted for brevity)
        }
        
        # Return insights for the specified topic, or default if not found
        return insights_by_topic.get(topic, insights_by_topic['business_model'])
    
    def get_next_step_suggestions(self, query):
        """
        Get next step suggestions based on query.
        
        Args:
            query (str): The query string to analyze.
            
        Returns:
            list: Next step suggestions relevant to the query.
        """
        query_lower = query.lower()
        
        # Default topic
        topic = 'business_model'
        
        # Determine topic based on keywords in query
        if any(kw in query_lower for kw in ['fundrais', 'investor', 'capital', 'money', 'funding']):
            topic = 'fundraising'
        elif any(kw in query_lower for kw in ['product', 'mvp', 'develop', 'feature']):
            topic = 'product_development'
        elif any(kw in query_lower for kw in ['team', 'hire', 'talent', 'employee']):
            topic = 'team_building'
        elif any(kw in query_lower for kw in ['dao', 'governance', 'token', 'blockchain']):
            topic = 'dao_governance'
        elif any(kw in query_lower for kw in ['growth', 'scale', 'market', 'customer']):
            topic = 'growth_strategy'
        
        # Return suggestions based on topic
        suggestions = self._get_suggestions_by_topic(topic)
        return suggestions
    
    def _get_suggestions_by_topic(self, topic):
        """Get next step suggestions for a specific topic."""
        suggestions_by_topic = {
            'business_model': [
                "Let's map out your current business model using the Business Model Canvas framework, then identify areas for innovation or optimization.",
                "I suggest conducting a competitive analysis to identify gaps in the market that your business model could uniquely address.",
                "Consider running small experiments to test key assumptions in your business model before committing significant resources.",
                "Let's develop metrics to track the performance of each component of your business model so you can make data-driven refinements."
            ],
            # (Other topics omitted for brevity)
        }
        return suggestions_by_topic.get(topic, suggestions_by_topic['business_model'])
