 # CrewaiHelloworld

Welcome to the Crewai Helloworld project. Refer to [crewAI](https://crewai.com). This app demonstrates a multi-agent scenario.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

You have to instal CrewAI
```
uv pip install crewai
```

Since I am using a model from Gemini (specifically, gemini/gemini-2.5-flash-lite) for this demo, I have installed:
```
uv pip install "crewai[google-genai]"
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/crewai_helloworld/config/agents.yaml` to define your agents
- Modify `src/crewai_helloworld/config/tasks.yaml` to define your tasks
- Modify `src/crewai_helloworld/crew.py` to add your own logic, tools and specific args
- Modify `src/crewai_helloworld/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the CrewAI-HelloWorld Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The CrewAI-HelloWorld Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the CrewaiHelloworld Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)

