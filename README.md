# Modern AI Resources

## 1. General Resources
- [100 Days of AI - Topics List for Learners](/100-days-of-AI.md)

## 2. [RAG Patterns](/RAG)

- ***Foundational Patterns***
    - **[Standard/Naive/Single-hop RAG](/RAG/LangChain-Standard.py)** - 
        The "Hello World" of RAG. You embed a user query, retrieve the top-k chunks from a vector database, and feed them to the LLM. It is fast but suffers from low precision if the document chunks are messy or the query is vague.

- ***Indexing & Context Optimization***
    - **Parent-Child (Small-to-Big) RAG** - Split documents into small "child" chunks for high-precision search. When a child is matched, you retrieve its larger "parent" chunk (or the whole document) to feed the LLM. This ensures the LLM gets enough context to answer correctly.
    - **Sentence Window Retrieval** - Similar to Parent-Child. You index individual sentences for search. When a sentence is found, the system retrieves a "window" of 3–5 sentences before and after it to provide context.
    - **KG‑augmented RAG** - Augments the vector search by querying a Knowledge Graph (KG) to inject structured relationships (entities and connections) that vector similarity might miss.
    - **GraphRAG** - An evolution of KG-augmented RAG. It performs "community detection" on the graph to summarize entire clusters of information. It excels at answering global questions like "What are the major themes in these documents?" which standard RAG fails to address.

- ***Query & Retrieval Refinement***
    - **Hybrid RAG** - Combines Vector Search (semantic meaning) with Keyword Search/BM25 (exact term matching). This is crucial for domains with specific jargon or product IDs where semantic search often fails.
    - **Rerank‑enhanced RAG** - Retrieves a large number of documents (e.g., 50) first, then uses a specialized "Cross-Encoder" model (a Reranker) to meticulously score and re-order them, passing only the top 5 highly relevant ones to the LLM.
    - **RAG Fusion** - Generates multiple variations of the user's query (e.g., rewriting the question 3 times). It retrieves documents for all variations and uses an algorithm called Reciprocal Rank Fusion (RRF) to consolidate the results.
    - **HyDE** (Hypothetical Document Embeddings) - The LLM first hallucinates a hypothetical answer to the user's question. This hypothetical answer is then used for the vector search (instead of the raw question), often leading to better semantic matches.

- ***Logic, Routing & Verification***
    - **Adaptive RAG** - A router analyzes the complexity of the query before starting.
    - **Corrective RAG (CRAG)** - After retrieval, a lightweight evaluator checks if the retrieved documents are actually relevant. If they are irrelevant/ambiguous, it triggers a fallback action (like a web search) instead of hallucinating an answer.
    - **Self-RAG** - The LLM is fine-tuned to generate "reflection tokens" (tags) during generation. It critiques its own retrieval and its own answer in real-time, deciding if it needs to retrieve more data or if the answer is fully supported.

- ***Autonomous & Multi-Step Workflows***
    - **Multi‑hop RAG** - Used when the answer requires combining information from multiple distinct documents (e.g., "Compare the revenue of Company A in 2021 with Company B in 2022"). The system performs one retrieval, analyzes it, and uses that to generate a second retrieval query.
    - **Agentic RAG** - The LLM acts as an autonomous agent with access to "tools" (one of which is a retrieval engine). The agent plans a sequence of actions, can use RAG multiple times, use a calculator, or search the web to solve the user's problem.

- ***Specialized Modalities***
    - **SQL‑augmented RAG** - Converts natural language into SQL queries to interact with structured relational databases, often combining the results with unstructured text retrieval.
    - **Multi‑modal RAG** - Handles inputs and outputs involving images, audio, or video alongside text (e.g., searching a video archive using a text description).
        

## 3. Agentic AI Patterns
- ***Single-Agent and Workflow Patterns***
    - **ReAct (Reason + Act) loop** - he classic dynamic loop: Thought $\to$ Action $\to$ Observation. It allows the agent to "figure things out" step-by-step but can be unstable in long runs.
    - **Prompt‑chaining / sequential pipeline** - Deterministic flows where the output of step A always becomes the input of step B. Used for reliable tasks like "Research $\to$ Summarize $\to$ Translate"
    - **Planner–executor (plan‑then‑act)** - Separates "Thinking" from "Doing." The agent first writes a manifest of 5 steps, then executes them deterministically. Reduces the chance of the agent getting "distracted" mid-task.
    - Self‑reflection / self‑critique loop
    - **Tool‑augmented single agent (Function Calling)** - An LLM that detects when to call an API (e.g., OpenAI Function Calling) to get data before answering.
    - **Router / dispatcher agents** - A gateway that classifies user intent (e.g., "Billing" vs. "Tech Support") and routes the query to a specialized downstream agent or prompt.
    - **Evaluator-Optimizer (Reflexion)** - A "quality assurance" pattern. One LLM call generates a draft, and a second call acts as a "Critic" to score it and request improvements. Proven to significantly boost coding/writing quality.

- ***Multi-Agent Patterns***
    - **Supervisor / orchestrator + worker agents / Hub-and-Spoke** - The Multi-Agent Standard. A central "Manager" agent breaks down the task, delegates sub-tasks to specific "Worker" agents (Coder, Researcher), and aggregates their answers
    - **Parallel specialist agents (fan‑out/fan‑in)** - Map-Reduce for LLMs. A manager spins up multiple identical agents to process different files or tasks simultaneously, then aggregates the results.
    - **Hand-offs / Swarm Pattern** - Decentralized control. Agent A realizes it can't finish a task and "transfers" the user directly to Agent B (e.g., Triage Agent $\to$ Sales Agent), with no central manager involved.
    - **Role‑based crew / team pattern** - Agents simulate a human team meeting, often conversing with each other in a round-robin or hierarchical fashion to solve a problem.
    - **Agents‑as‑Tools Pattern** - Encapsulation. A complex agent (e.g., a "SQL Writer Agent") is wrapped up and given as a single "tool" to a higher-level agent.

- ***Production Reliability & Safety Patterns***
    - **Human-in-the-Loop (HITL)** The agent pauses execution at critical junctures—like sending an email or spending budget—to wait for human approval via API/UI.
    - **Compliance / Guardrail Co-pilot** - A secondary, lower-intelligence "Monitor" model watches the main agent's output in real-time. It blocks toxic content, PII leaks, or off-topic actions before they reach the user.
    - **Corrective & Self‑healing Agents** - Agents equipped with error-handling logic. If a tool fails (e.g., API timeout), the agent analyzes the error message and tries a different parameter or alternative tool.

- ***Advanced / Frontier Architectures***
    
    - **Memory‑centric / persona‑persistent agents** - Agents with long-term memory layers (like MemGPT) that remember user details across sessions weeks apart
    - **Environment‑/simulation‑based agents** - Agents that "live" inside a sandbox (like a coding environment or game) and learn via Reinforcement Learning or trial-and-error.
    - **Hierarchical Multi‑level Planning** - Extremely complex systems with multiple layers of supervisors (e.g., a CEO Agent managing Manager Agents managing Worker Agents).

