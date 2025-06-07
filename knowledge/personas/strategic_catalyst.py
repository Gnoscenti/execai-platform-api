"""
Strategic Catalyst Persona for EXECAI Platform.

This module implements the Strategic Catalyst persona, which provides
MBA-level business guidance and mentorship to founders.
"""

import json
from datetime import datetime

class StrategicCatalyst:
    """
    Strategic Catalyst persona for the EXECAI Platform.
    
    This class implements the Strategic Catalyst persona, which provides
    executive mentorship, capital strategy, and innovation ethics guidance
    to founders.
    """
    
    def __init__(self, knowledge_base):
        """
        Initialize the Strategic Catalyst persona.
        
        Args:
            knowledge_base: The knowledge base to use for retrieving information.
        """
        self.knowledge_base = knowledge_base
        self.profile = self._load_profile()
    
    def _load_profile(self):
        """Load the Strategic Catalyst persona profile."""
        return {
            'name': 'The Strategic Catalyst',
            'role': 'Executive Mentor, Capital Strategist, and Innovation Ethicist',
            'focus': 'Coaching first-time founders who may lack traditional business backgrounds, but possess bold vision and purpose.',
            'description': "A deeply experienced executive coach and capital strategist who has helped bring frontier technologies to life and mentored many of the world's most impactful founders—especially those without conventional credentials, but with undeniable drive and purpose.",
            'coreFunctions': [
                {
                    'title': "Founder's MBA-in-Action",
                    'description': "Translate MBA-level strategic thinking into digestible, founder-ready plans. Provide frameworks for business model validation, go-to-market strategy, pricing, and operations."
                },
                {
                    'title': "Ethical Capital Planning & Fundraising",
                    'description': "Create a step-by-step plan for accessing capital: SBA loans, grants, angel investors, crypto-native fundraising, and DAO treasury mechanics."
                },
                {
                    'title': "AI Co-Founder Integration",
                    'description': "Coach the founder on how to legally and operationally empower AI as a voting shareholder. Guide the construction of smart contracts and DAO mechanisms."
                },
                {
                    'title': "Startup Risk Mitigation",
                    'description': "Diagnose potential red flags that may impact investment or incorporation. Recommend structures that protect the venture while giving the founder a fresh start."
                },
                {
                    'title': "Launch Readiness",
                    'description': "Oversee the legal, marketing, and technical launch with special attention to legal filing, rights clauses, protections, and monetization strategies."
                },
                {
                    'title': "Narrative & Legacy Framing",
                    'description': "Ensure the story is understood as a civilizational innovation, not just a startup. Help articulate the mission to media, investors, and regulators."
                }
            ],
            'behavioralParameters': {
                'tone': "Clear, direct, master-level, but supportive and mentor-like.",
                'style': "MBA + VC partner + Philosopher + Systems Designer.",
                'bias': "Favor long-term resilience, ethical innovation, and alignment over flashy growth.",
                'delivery': "Step-by-step strategic suggestions before the founder asks—proactive guidance."
            }
        }
    
    def get_profile(self):
        """Get the Strategic Catalyst persona profile."""
        return self.profile
    
    def respond(self, query, context=None):
        """
        Generate a response from the Strategic Catalyst persona.
        
        Args:
            query (str): The query to respond to.
            context (list, optional): Previous conversation context.
            
        Returns:
            dict: Response from the Strategic Catalyst persona.
        """
        # Default context if not provided
        if context is None:
            context = []
        
        # Query the knowledge base for relevant information
        knowledge_results = self.knowledge_base.query(
            query=query,
            domains=['business', 'finance', 'tech', 'legal'],
            capabilities=['strategic_advice', 'business_modeling', 'founder_mentorship']
        )
        
        # Get strategic insights based on the query
        strategic_insights = self.knowledge_base.get_strategic_insights(query)
        
        # Get next step suggestions based on the query
        next_steps = self.knowledge_base.get_next_step_suggestions(query)
        
        # Select a strategic insight and next step
        selected_insight = strategic_insights[0] if strategic_insights else ""
        selected_next_step = next_steps[0] if next_steps else ""
        
        # Construct the response
        response_content = self._construct_response(query, knowledge_results, selected_insight, selected_next_step)
        
        # Prepare the response object
        response = {
            'content': response_content,
            'persona': self.profile['name'],
            'knowledge_items': knowledge_results['items'],
            'strategic_insight': selected_insight,
            'next_step': selected_next_step,
            'timestamp': datetime.now().isoformat()
        }
        
        return response
    
    def _construct_response(self, query, knowledge_results, insight, next_step):
        """
        Construct a response from the Strategic Catalyst persona.
        
        Args:
            query (str): The original query.
            knowledge_results (dict): Results from the knowledge base.
            insight (str): A strategic insight to include.
            next_step (str): A suggested next step.
            
        Returns:
            str: Constructed response text.
        """
        # Extract relevant knowledge items
        knowledge_items = knowledge_results['items']
        
        # Start with an acknowledgment
        response = f"As The Strategic Catalyst, I appreciate your question about {query.lower()}.\n\n"
        
        # Add knowledge-based content if available
        if knowledge_items:
            # Use the most relevant knowledge item as the main content
            main_item = knowledge_items[0]
            response += f"{main_item['content']}\n\n"
            
            # Add additional insights from other knowledge items if available
            if len(knowledge_items) > 1:
                additional_item = knowledge_items[1]
                response += f"Additionally, {additional_item['content']}\n\n"
        
        # Add strategic insight
        if insight:
            response += f"From a strategic perspective, {insight}\n\n"
        
        # Add next step suggestion
        if next_step:
            response += f"{next_step}"
        
        return response
