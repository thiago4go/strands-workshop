# Exercise 3: Research Team - Multi-Agent Collaboration
# Module 3 - Multi-Agent Systems

"""
Learning Objectives:
1. Understand multi-agent orchestration patterns
2. Implement specialized agents working together
3. Practice task decomposition and result aggregation
4. Experience the power of collaborative AI systems

This exercise demonstrates the Orchestrator-Worker pattern where:
- A coordinator agent manages the overall workflow
- Specialized agents handle specific aspects of research
- Results are aggregated into a comprehensive final report
"""

from strands import Agent
from strands_tools import http_request, calculator, current_time
from strands.models import BedrockModel
from typing import Dict, Any
import json

class ResearchTeam:
    """
    A collaborative multi-agent research team that demonstrates
    the power of specialized agents working together.
    """
    
    def __init__(self):
        # Create the model configuration (shared across agents)
        self.model = BedrockModel(
            model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            region_name='us-east-1',
            temperature=0.3
        )
        
        # Initialize specialized agents
        self._create_team_members()
    
    def _create_team_members(self):
        """Create specialized agents for different research tasks."""
        
        # 1. Research Coordinator - Orchestrates the entire process
        self.coordinator = Agent(
            model=self.model,
            system_prompt="""You are the Research Team Coordinator. Your role:
            1. Understand the research request and break it into subtasks
            2. Delegate appropriate tasks to team specialists
            3. Synthesize results from all team members
            4. Create comprehensive final reports
            
            Be decisive and efficient in task allocation. Always provide
            clear, actionable instructions to your team members."""
        )
        
        # 2. Information Gatherer - Finds and collects data
        self.researcher = Agent(
            model=self.model,
            tools=[http_request],
            system_prompt="""You are the Information Gatherer specialist. Your expertise:
            - Finding accurate, current information from reliable sources
            - Validating information credibility
            - Extracting key facts and data points
            - Summarizing findings concisely
            
            Always cite your sources and focus on factual accuracy."""
        )
        
        # 3. Data Analyst - Processes and analyzes information
        self.analyst = Agent(
            model=self.model,
            tools=[calculator, current_time],
            system_prompt="""You are the Data Analyst specialist. Your expertise:
            - Identifying patterns and trends in data
            - Performing statistical analysis and calculations
            - Creating insights from raw information
            - Highlighting significant findings and anomalies
            
            Focus on quantitative analysis and data-driven insights."""
        )
        
        # 4. Strategic Advisor - Provides recommendations and implications
        self.strategist = Agent(
            model=self.model,
            system_prompt="""You are the Strategic Advisor specialist. Your expertise:
            - Developing actionable recommendations
            - Analyzing implications and consequences
            - Identifying risks and opportunities
            - Creating implementation strategies
            
            Think strategically about long-term impacts and practical applications."""
        )
    
    def conduct_research(self, research_topic: str) -> Dict[str, Any]:
        """
        Conduct comprehensive research using the multi-agent team.
        
        Args:
            research_topic (str): The topic to research
            
        Returns:
            Dict[str, Any]: Complete research results from all team members
        """
        print(f"🎯 Research Team activated for topic: {research_topic}")
        print("=" * 60)
        
        # Step 1: Coordinator creates research plan
        print("\n📋 STEP 1: Research Planning")
        print("-" * 30)
        
        planning_prompt = f"""
        Create a detailed research plan for: {research_topic}
        
        Break this down into specific tasks for our team:
        1. Information Gatherer - what data to collect
        2. Data Analyst - what analysis to perform  
        3. Strategic Advisor - what recommendations to develop
        
        Provide clear, actionable instructions for each team member.
        """
        
        research_plan = self.coordinator(planning_prompt)
        print(f"Research Plan:\n{research_plan}")
        
        # Step 2: Information Gatherer collects data
        print("\n🔍 STEP 2: Information Gathering")
        print("-" * 30)
        
        gathering_prompt = f"""
        Based on this research plan: {research_plan}
        
        Gather comprehensive information about: {research_topic}
        
        Focus on:
        - Current facts and statistics
        - Recent developments and trends
        - Key players and organizations
        - Relevant data points and metrics
        """
        
        research_data = self.researcher(gathering_prompt)
        print(f"Research Data Collected:\n{research_data[:500]}...")
        
        # Step 3: Data Analyst processes the information
        print("\n📊 STEP 3: Data Analysis")
        print("-" * 30)
        
        analysis_prompt = f"""
        Analyze this research data: {research_data}
        
        Provide:
        - Key patterns and trends identified
        - Statistical insights and calculations
        - Significant findings and anomalies
        - Data-driven conclusions
        
        Focus on quantitative analysis where possible.
        """
        
        analysis_results = self.analyst(analysis_prompt)
        print(f"Analysis Results:\n{analysis_results[:500]}...")
        
        # Step 4: Strategic Advisor develops recommendations
        print("\n🎯 STEP 4: Strategic Recommendations")
        print("-" * 30)
        
        strategy_prompt = f"""
        Based on this research data: {research_data}
        And this analysis: {analysis_results}
        
        Develop strategic recommendations for: {research_topic}
        
        Include:
        - Key opportunities and risks
        - Actionable recommendations
        - Implementation considerations
        - Success metrics and KPIs
        """
        
        strategic_recommendations = self.strategist(strategy_prompt)
        print(f"Strategic Recommendations:\n{strategic_recommendations[:500]}...")
        
        # Step 5: Coordinator synthesizes final report
        print("\n📝 STEP 5: Final Report Synthesis")
        print("-" * 30)
        
        synthesis_prompt = f"""
        Create a comprehensive executive summary combining all team inputs:
        
        Research Plan: {research_plan}
        Research Data: {research_data}
        Analysis: {analysis_results}
        Strategy: {strategic_recommendations}
        
        Format as a professional research report with:
        1. Executive Summary
        2. Key Findings
        3. Data Analysis
        4. Strategic Recommendations
        5. Next Steps
        """
        
        final_report = self.coordinator(synthesis_prompt)
        
        # Return complete results
        return {
            "topic": research_topic,
            "research_plan": research_plan,
            "research_data": research_data,
            "analysis": analysis_results,
            "strategy": strategic_recommendations,
            "final_report": final_report
        }

def main():
    """Main function to demonstrate the research team in action."""
    
    print("🚀 Multi-Agent Research Team Demo")
    print("=" * 50)
    
    # Create the research team
    team = ResearchTeam()
    
    # Example research topics (try different ones!)
    research_topics = [
        "The impact of AI agents on software development productivity",
        "Current trends in serverless computing adoption",
        "Market opportunities for multi-agent AI systems"
    ]
    
    # Let user choose or use default
    topic = research_topics[0]  # Change index to try different topics
    
    print(f"Selected Research Topic: {topic}")
    
    # Conduct the research
    results = team.conduct_research(topic)
    
    # Display final results
    print("\n" + "=" * 60)
    print("🎉 FINAL RESEARCH REPORT")
    print("=" * 60)
    print(results["final_report"])
    
    # Optional: Save results to file
    save_results = input("\nSave results to file? (y/n): ").lower().strip()
    if save_results == 'y':
        filename = f"research_report_{topic.replace(' ', '_')[:30]}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to: {filename}")

if __name__ == "__main__":
    main()

# 🎓 Learning Exercises:
# 
# 1. **Modify Agent Roles**: Try changing the system prompts to create
#    different specialist roles (e.g., Technical Expert, Market Researcher)
#
# 2. **Add New Agents**: Create additional specialists like:
#    - Competitive Intelligence Agent
#    - Risk Assessment Agent  
#    - Financial Analysis Agent
#
# 3. **Experiment with Tools**: Add more tools to different agents:
#    - Give the researcher access to specific APIs
#    - Add data visualization tools to the analyst
#    - Include planning tools for the strategist
#
# 4. **Parallel Processing**: Modify the workflow to run some agents
#    in parallel instead of sequentially
#
# 5. **Error Handling**: Add robust error handling for when agents
#    fail or provide incomplete responses
#
# 6. **Quality Control**: Add a quality assurance agent that reviews
#    and validates the work of other agents
