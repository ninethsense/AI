#!/usr/bin/env python
# src/latest_ai_development/main.py
import sys
import warnings
from crewai_helloworld.crew import LatestAiDevelopmentCrew

# Suppress warnings for a cleaner CLI output
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew to design and audit an Agentic AI Architecture.
    """
    # Change the topic to a specific use case for a more detailed blueprint
    inputs = {
        'topic': 'Enterprise-grade Autonomous Financial Reporting System',
        'business_objective': 'Reduce manual audit time by 80% while maintaining 100% data lineage.'
    }
    
    try:
        LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()