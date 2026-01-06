# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew for Agentic AI Architecture and Auditing"""

    # The @CrewBase decorator handles the loading of agents.yaml and tasks.yaml
    # based on the method names below.

    @agent
    def agentic_architect(self) -> Agent:
        return Agent(
            config=self.agents_config['agentic_architect'],
            verbose=True,
            # Architect may need search tools to research current SOTA patterns
            tools=[SerperDevTool()] 
        )

    @agent
    def enterprise_critique(self) -> Agent:
        return Agent(
            config=self.agents_config['enterprise_critique'],
            verbose=True
        )

    @task
    def design_architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_architecture_task'],
        )

    @task
    def critique_and_audit_task(self) -> Task:
        return Task(
            config=self.tasks_config['critique_and_audit_task'],
            # The output file path is now relative to the project root
            output_file='output/architecture_audit_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Agentic Design and Audit crew"""
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            # Sequential ensures the Architect finishes before the Critique begins
            process=Process.sequential,
            verbose=True,
        )