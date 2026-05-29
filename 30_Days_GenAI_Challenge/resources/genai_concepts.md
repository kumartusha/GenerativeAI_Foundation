# Master Document: Key Concepts in LLMs, RAG Systems, and AI Agents

This document serves as a comprehensive study guide, reference, and concept map for Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AI Agents. It covers foundational to advanced topics in a structured, beginner-friendly way. Explanations are kept simple, using bullet points for clarity. Each concept includes a short summary, followed by the core 3-part structure: (1) What is it?, (2) What are the types?, and (3) When to use each type? Insights from my knowledge are woven in to provide practical depth, such as real-world examples or emerging patterns (e.g., agentic workflows for scalability).

Topics are organized in ascending logical order: starting with core prompting and LLM basics (A), moving to retrieval (B-C), memory (D), workflows (E), embeddings/search (F), agents (G), training (H), and system design (I). Where relevant, agent patterns (e.g., ReAct loops) are highlighted for integration across sections.

---

## A. Prompting & LLM Concepts

### Prompting
**Short Summary:** Prompting is the art of crafting inputs to guide LLMs toward desired outputs, acting as the "steering wheel" for AI behavior without code changes.

1. **What is it?**  
   Prompting involves designing text inputs (prompts) that instruct an LLM on how to respond, leveraging its pre-trained knowledge to generate accurate, creative, or structured outputs. It's like giving clear directions to a knowledgeable assistant.

2. **What are the types?**  
   - **Zero-shot:** No examples; just a direct instruction.  
   - **Few-shot:** Includes 1-5 examples in the prompt to demonstrate the task.  
   - **Chain-of-Thought (CoT):** Encourages step-by-step reasoning by adding "think step by step."  
   - **Role-based:** Assigns a persona (e.g., "You are a doctor") to shape responses.  
   - **System Prompts:** Fixed instructions at the start defining overall behavior.

3. **When to use each type?**  
   - **Zero-shot:** Best for simple, general tasks like classification (e.g., sentiment analysis on reviews); advantages: fast, no example prep; use when LLM is strong on the domain.  
   - **Few-shot:** Ideal for nuanced tasks needing patterns (e.g., translation with idioms); advantages: improves accuracy without fine-tuning; best when examples are cheap to curate.  
   - **CoT:** For complex reasoning (e.g., math problems); advantages: boosts logical outputs by 20-50% in benchmarks; use in planning agents for transparent decisions.  
   - **Role-based:** In customer service bots; advantages: consistent tone; pair with agents for role-switching in multi-turn chats.  
   - **System Prompts:** Always for chat apps (e.g., defining ethics); advantages: sets global rules; essential in agentic RAG to enforce retrieval guidelines.  
   *Added Insight:* In agent patterns, combine CoT with tools for "reason-act-observe" loops, reducing hallucinations in dynamic environments like stock analysis.

### Zero-shot Prompting
**Short Summary:** Zero-shot prompting relies on the LLM's inherent knowledge without examples, making it efficient for broad applications.

1. **What is it?**  
   A prompting technique where the model performs a task based solely on a natural language description, without any training examples in the prompt.

2. **What are the types?**  
   - **Direct Instruction:** Simple command (e.g., "Classify this text as positive or negative").  
   - **Constrained Output:** Specifies format (e.g., "Answer yes/no").  
   - **Hypothetical Scenarios:** Poses "what if" questions for creative tasks.

3. **When to use each type?**  
   - **Direct Instruction:** For quick queries like summarization; advantages: low latency; best in real-time search agents.  
   - **Constrained Output:** In APIs for structured JSON responses; advantages: parses easily; use in RAG for metadata extraction.  
   - **Hypothetical Scenarios:** Brainstorming ideas (e.g., "What if we add AI to farming?"); advantages: sparks innovation; ideal for planning agents in ideation workflows.  
   *Added Insight:* Scales well in multi-agent systems where agents delegate zero-shot subtasks, but monitor for cultural biases in global apps.

### Few-shot Prompting
**Short Summary:** Few-shot provides a handful of examples to "teach" the LLM a pattern, bridging zero-shot limitations for better precision.

1. **What is it?**  
   Involves including a small number (1-10) of input-output examples in the prompt to guide the model on unfamiliar or specific tasks.

2. **What are the types?**  
   - **In-Context Learning:** Examples embedded directly in the prompt.  
   - **Demonstration-Based:** Focuses on showing variations (e.g., edge cases).  
   - **Dynamic Few-Shot:** Selects examples at runtime based on query similarity.

3. **When to use each type?**  
   - **In-Context Learning:** For translation or QA; advantages: quick adaptation; best when context window allows (e.g., <4k tokens).  
   - **Demonstration-Based:** Handling ambiguities (e.g., legal text parsing); advantages: reduces errors by 15-30%; use in RAG for domain-specific retrieval.  
   - **Dynamic Few-Shot:** Personalized recommendations; advantages: relevance boosts; integrate with embeddings for agentic selection in e-commerce bots.  
   *Added Insight:* In ascending agent complexity, start with few-shot for tool-calling calibration, evolving to self-improving agents that curate their own examples.

### Chain-of-Thought Prompting
**Short Summary:** CoT mimics human reasoning by prompting step-by-step thoughts, enhancing LLM accuracy on logical tasks.

1. **What is it?**  
   A method that elicits intermediate reasoning steps in the prompt or output, improving performance on arithmetic, commonsense, and symbolic tasks.

2. **What are the types?**  
   - **Standard CoT:** Adds "Let's think step by step."  
   - **Self-Consistency CoT:** Generates multiple reasonings and votes on the best.  
   - **Tree-of-Thoughts (ToT):** Branches into multiple reasoning paths like a decision tree.

3. **When to use each type?**  
   - **Standard CoT:** Math word problems; advantages: simple, 2x accuracy gain; core in ReAct agents for planning.  
   - **Self-Consistency CoT:** Uncertain domains like forecasting; advantages: ensembles reduce variance; use in multi-hop RAG for verification.  
   - **ToT:** Complex puzzles (e.g., game strategies); advantages: explores alternatives; best for autonomous agents in simulation environments.  
   *Added Insight:* Pairs with graph workflows in LangGraph for visual reasoning traces, aiding debugging in production AI systems.

### System Prompts
**Short Summary:** System prompts set overarching rules for LLM behavior, like a constitution for consistent, safe interactions.

1. **What is it?**  
   A special prompt type placed at the conversation start to define the model's role, guidelines, and constraints, influencing all subsequent responses.

2. **What are the types?**  
   - **Role-Defining:** Assigns identity (e.g., "You are a helpful tutor").  
   - **Constraint-Based:** Enforces rules (e.g., "Never give medical advice").  
   - **Context-Setting:** Provides background (e.g., "We're discussing climate change").

3. **When to use each type?**  
   - **Role-Defining:** Chatbots; advantages: aligns tone; essential for multi-agent collaboration.  
   - **Constraint-Based:** Safety-critical apps; advantages: mitigates risks; integrate with guardrails in RAG for factual grounding.  
   - **Context-Setting:** Long sessions; advantages: maintains coherence; use in episodic memory for agent continuity.  
   *Added Insight:* In agent patterns, dynamic system prompts adapt via reflection, enabling self-evolution in long-running tasks like research assistants.

### Role Prompting
**Short Summary:** Role prompting casts the LLM in a specific persona to tailor responses, enhancing relevance and engagement.

1. **What is it?**  
   Instructs the model to adopt a character or expertise (e.g., "Act as a pirate"), influencing style, knowledge focus, and creativity.

2. **What are the types?**  
   - **Static Roles:** Fixed throughout (e.g., "You are Sherlock Holmes").  
   - **Dynamic Roles:** Switches based on context (e.g., teacher vs. peer).  
   - **Ensemble Roles:** Blends multiple (e.g., "Historian and storyteller").

3. **When to use each type?**  
   - **Static Roles:** Educational tools; advantages: immersion; best for single-task agents.  
   - **Dynamic Roles:** Versatile assistants; advantages: flexibility; use in router chains for task delegation.  
   - **Ensemble Roles:** Creative writing; advantages: rich outputs; pair with ToT for narrative branching.  
   *Added Insight:* Enhances multi-agent systems by assigning specialized roles, reducing overload on a single LLM instance.

### Temperature & Sampling
**Short Summary:** Temperature controls output randomness in LLMs, balancing creativity and determinism during text generation.

1. **What is it?**  
   A hyperparameter (0-2) that scales the softmax in sampling: low for focused responses, high for diverse ones. Sampling refers to methods like greedy (deterministic) vs. stochastic (random).

2. **What are the types?**  
   - **Greedy Decoding:** Always picks highest probability (temp=0).  
   - **Top-k Sampling:** Samples from top k tokens.  
   - **Nucleus (Top-p) Sampling:** Samples from smallest set summing to probability p.  
   - **Beam Search:** Explores multiple paths for best overall sequence.

3. **When to use each type?**  
   - **Greedy:** Factual QA; advantages: fast, consistent; ideal for RAG retrieval summaries.  
   - **Top-k:** Creative brainstorming; advantages: controlled diversity; use in agent planning for idea generation.  
   - **Nucleus:** Balanced storytelling; advantages: adaptive to context; best for conversational agents.  
   - **Beam Search:** Translation; advantages: higher quality; but slower—reserve for offline tasks.  
   *Added Insight:* In production, tune temperature dynamically (e.g., low for tools, high for ideation) to optimize agent action loops.

### Tokens & Context Window
**Short Summary:** Tokens are LLM's basic units (subwords/words), and context window is the max input size, limiting memory like a short-term buffer.

1. **What is it?**  
   Tokens break text into processable chunks (e.g., "chat" = 1 token); context window is the token limit for input+output (e.g., 128k for GPT-4o).

2. **What are the types?**  
   - **Subword Tokenization:** (e.g., BPE) splits rare words.  
   - **Byte-Pair Encoding (BPE):** Common in GPT models.  
   - **WordPiece:** Used in BERT.  
   - **SentencePiece:** Unigram-based for multilingual.

3. **When to use each type?**  
   - **Subword:** General NLP; advantages: handles OOV words; default for most LLMs.  
   - **BPE:** Code generation; advantages: efficient for English; use in agent tool calls.  
   - **WordPiece:** Search tasks; advantages: semantic chunks; pair with RAG chunking.  
   - **SentencePiece:** Global apps; advantages: language-agnostic; best for multimodal agents.  
   *Added Insight:* Exceeding windows triggers truncation—use summary memory in agents to compress history, enabling longer workflows.

### Tool Calling / Function Calling
**Short Summary:** Tool calling lets LLMs invoke external functions (e.g., APIs) like a programmer, extending capabilities beyond text.

1. **What is it?**  
   The LLM generates structured calls to predefined tools (e.g., JSON for weather API), processes results, and continues reasoning.

2. **What are the types?**  
   - **Single Tool:** One function per call.  
   - **Parallel Tools:** Multiple simultaneous invocations.  
   - **Chained Tools:** Sequential based on prior outputs.

3. **When to use each type?**  
   - **Single Tool:** Simple queries (e.g., calculator); advantages: low overhead; core in basic ReAct agents.  
   - **Parallel:** Data aggregation (e.g., multi-source search); advantages: speed; use in RAG for hybrid retrieval.  
   - **Chained:** Workflows (e.g., search then summarize); advantages: composable; essential for planning agents.  
   *Added Insight:* In ascending complexity, evolve from single to multi-tool in LangChain for robust error recovery via retries.

### Reasoning Frameworks (ReAct, Tree-of-Thought, etc.)
**Short Summary:** Frameworks structure LLM reasoning for better decision-making, like mental models for AI problem-solving.

1. **What is it?**  
   Systematic methods to interleave thinking, acting, and observing, improving transparency and accuracy in complex tasks.

2. **What are the types?**  
   - **ReAct (Reason-Act):** Alternates rationale, action, observation.  
   - **Tree-of-Thought (ToT):** Explores branching reason paths.  
   - **Graph-of-Thought (GoT):** Connects thoughts in a graph for non-linear flow.  
   - **Self-Refine:** Iteratively critiques and improves outputs.

3. **When to use each type?**  
   - **ReAct:** Interactive QA; advantages: grounded actions; backbone for tool-using agents.  
   - **ToT:** Optimization problems; advantages: prunes bad paths; use in game-playing agents.  
   - **GoT:** Knowledge synthesis; advantages: handles cycles; integrate with Graph RAG.  
   - **Self-Refine:** Code debugging; advantages: iterative gains; best for reflective agents.  
   *Added Insight:* These form agent patterns—ReAct for loops, ToT for exploration—scaling to multi-agent debates for consensus.

### LLM Agents (Basic Meaning)
**Short Summary:** LLM agents are autonomous systems powered by LLMs that perceive, decide, and act in environments, like smart assistants on steroids.

1. **What is it?**  
   Software entities using LLMs as brains to interact with tools/world, pursuing goals via planning and execution.

2. **What are the types?**  
   - **Reactive Agents:** Respond to inputs without memory.  
   - **Deliberative Agents:** Plan ahead with reasoning.  
   - **Learning Agents:** Adapt from experience.

3. **When to use each type?**  
   - **Reactive:** Simple automation (e.g., email sorter); advantages: fast; entry-level in workflows.  
   - **Deliberative:** Task orchestration; advantages: strategic; core for RAG-enhanced research.  
   - **Learning:** Personalized bots; advantages: improves over time; use with memory for long-term users.  
   *Added Insight:* Agents bridge LLMs and RAG—e.g., query routing in agentic RAG—enabling scalable, context-aware systems.

---

## B. RAG (Retrieval-Augmented Generation) Concepts

### What is RAG?
**Short Summary:** RAG combines retrieval from external knowledge with LLM generation, grounding responses in facts to reduce hallucinations.

1. **What is it?**  
   A hybrid approach: retrieve relevant docs from a knowledge base, then feed them to an LLM for informed generation.

2. **What are the types?**  
   - **Naive RAG:** Basic retrieve-then-generate.  
   - **Advanced RAG:** With optimizations like reranking.  
   - **Modular RAG:** Customizable components.

3. **When to use each type?**  
   - **Naive:** Prototypes; advantages: simple setup; for internal FAQs.  
   - **Advanced:** Production QA; advantages: higher precision; in enterprise search.  
   - **Modular:** Custom domains; advantages: flexible; integrate with agents for dynamic queries.  
   *Added Insight:* RAG evolves LLMs into "knowledge workers"—pair with agents for self-correcting retrieval in real-time news apps.

### Basic RAG Pipeline
**Short Summary:** The RAG pipeline is a step-by-step flow: index knowledge, retrieve matches, augment prompt, generate response.

1. **What is it?**  
   A sequence: chunk/embed/store data → query → retrieve/embed → rerank → LLM generate with context.

2. **What are the types?**  
   - **Single-Stage:** Direct retrieve-generate.  
   - **Multi-Stage:** With expansion/reranking.  
   - **End-to-End:** Fully automated with feedback loops.

3. **When to use each type?**  
   - **Single-Stage:** Low-volume apps; advantages: quick; for chatbots.  
   - **Multi-Stage:** Complex queries; advantages: accuracy; use in legal research.  
   - **End-to-End:** Scalable systems; advantages: adaptive; agentic for continuous learning.  
   *Added Insight:* In workflows, embed checkpoints for observability, ensuring traceability in regulated industries.

### Chunking (All Techniques: Fixed, Sliding Window, Recursive, Semantic)
**Short Summary:** Chunking splits documents into manageable pieces for embedding, balancing context and efficiency.

1. **What is it?**  
   Dividing large texts into smaller units to fit context windows and improve retrieval granularity.

2. **What are the types?**  
   - **Fixed-Size:** Uniform length chunks (e.g., 512 tokens).  
   - **Sliding Window:** Overlaps chunks for continuity.  
   - **Recursive:** Splits hierarchically (e.g., by paragraphs then sentences).  
   - **Semantic:** Breaks at meaning boundaries using models.

3. **When to use each type?**  
   - **Fixed-Size:** Uniform data like logs; advantages: simple, fast indexing; for time-series analysis.  
   - **Sliding Window:** Narrative texts; advantages: avoids splits mid-sentence; best for stories in RAG.  
   - **Recursive:** Structured docs (e.g., PDFs); advantages: preserves hierarchy; use with metadata filtering.  
   - **Semantic:** Technical manuals; advantages: context-aware; compute-heavy but precise for agents.  
   *Added Insight:* Hybrid chunking (fixed + semantic) in agent patterns optimizes for multi-hop queries, reducing noise.

### Splitting (Sentence-Based, Paragraph-Based, Semantic Splitting)
**Short Summary:** Splitting is a chunking variant focused on natural breaks, ensuring coherent retrieval units.

1. **What is it?**  
   Techniques to divide text at logical points, minimizing information loss across boundaries.

2. **What are the types?**  
   - **Sentence-Based:** Splits at periods/full stops.  
   - **Paragraph-Based:** By line breaks or indents.  
   - **Semantic Splitting:** Uses NLP to group related ideas.

3. **When to use each type?**  
   - **Sentence-Based:** QA on articles; advantages: fine-grained; for precise fact extraction.  
   - **Paragraph-Based:** Reports; advantages: broader context; in basic RAG pipelines.  
   - **Semantic:** Conversations; advantages: thematic coherence; enhance with embeddings for agent routing.  
   *Added Insight:* Semantic splitting shines in multimodal RAG, aligning text chunks with image captions for unified search.

### Embeddings (Dense, Sparse, Hybrid)
**Short Summary:** Embeddings convert text to vectors capturing meaning, enabling similarity-based retrieval.

1. **What is it?**  
   Numerical representations (vectors) of text where similar meanings are close in space.

2. **What are the types?**  
   - **Dense:** Fixed-size vectors from neural nets (e.g., BERT).  
   - **Sparse:** High-dim with mostly zeros (e.g., TF-IDF).  
   - **Hybrid:** Combines both for comprehensive search.

3. **When to use each type?**  
   - **Dense:** Semantic search (e.g., paraphrases); advantages: captures intent; default for RAG.  
   - **Sparse:** Keyword matching; advantages: interpretable, fast; for exact terms like names.  
   - **Hybrid:** E-commerce; advantages: best of both (recall + precision); use in retrievers for balanced agents.  
   *Added Insight:* Fine-tune dense embeddings with LoRA for domain-specific RAG, boosting agent performance in niches like medicine.

### Vector Databases (and Indexing Types)
**Short Summary:** Vector DBs store and query embeddings efficiently, like a supercharged search engine for meanings.

1. **What is it?**  
   Specialized databases for high-dimensional vectors, supporting fast approximate nearest neighbor (ANN) searches.

2. **What are the types?** (Indexing)  
   - **Flat (Exact):** Brute-force scan.  
   - **HNSW (Hierarchical Navigable Small World):** Graph-based for speed.  
   - **IVF (Inverted File):** Clusters for partitioning.

3. **When to use each type?**  
   - **Flat:** Small datasets (<10k vectors); advantages: 100% accurate; prototyping RAG.  
   - **HNSW:** Large-scale real-time; advantages: low latency; core for production agents.  
   - **IVF:** Massive corpora; advantages: scalable; pair with PQ for compression in cloud setups.  
   *Added Insight:* Shard vector DBs horizontally for scaling, integrating with agent memory for persistent knowledge graphs.

### Retrievers (Similarity Search, BM25, Hybrid, Parent-Child, Multi-Query, Metadata Filtering)
**Short Summary:** Retrievers fetch relevant chunks from the index, the "search engine" of RAG.

1. **What is it?**  
   Algorithms to match queries to stored data, returning top-k candidates for generation.

2. **What are the types?**  
   - **Similarity Search:** Vector cosine similarity.  
   - **BM25:** Sparse keyword scoring.  
   - **Hybrid:** Weighted dense + sparse.  
   - **Parent-Child:** Retrieves child chunks, then parents for context.  
   - **Multi-Query:** Expands query into variants.  
   - **Metadata Filtering:** Pre-filters by tags (e.g., date).

3. **When to use each type?**  
   - **Similarity:** Conceptual matches; advantages: intuitive; for creative RAG.  
   - **BM25:** Lexical search; advantages: handles typos; legacy doc retrieval.  
   - **Hybrid:** Robust apps; advantages: high recall; standard in agents.  
   - **Parent-Child:** Hierarchical data; advantages: full context; PDFs in legal RAG.  
   - **Multi-Query:** Ambiguous queries; advantages: broader coverage; multi-hop agents.  
   - **Metadata:** Filtered views; advantages: efficient; e.g., user-specific in personalized bots.  
   *Added Insight:* Chain retrievers in sequential workflows for progressive refinement, mimicking human research.

### Rerankers (Cross Encoders, LLM Reranking)
**Short Summary:** Rerankers refine initial retrievals, boosting relevance like a quality filter.

1. **What is it?**  
   Models that score query-document pairs post-retrieval to reorder results for better precision.

2. **What are the types?**  
   - **Cross Encoders:** Jointly encode query+doc for deep scoring.  
   - **LLM Reranking:** Uses LLM to judge relevance.

3. **When to use each type?**  
   - **Cross Encoders:** High-accuracy needs; advantages: precise but slow; top-k=100 in e-discovery.  
   - **LLM Reranking:** Explainable; advantages: leverages LLM reasoning; for agentic verification.  
   *Added Insight:* LLM rerankers integrate with reflection patterns, self-improving over sessions via feedback.

### Context Compression
**Short Summary:** Compression shrinks retrieved context to fit windows, retaining key info without dilution.

1. **What is it?**  
   Techniques to summarize or extract salient parts from long contexts before LLM input.

2. **What are the types?**  
   - **LLM-Based:** Prompt LLM to condense.  
   - **Extractive:** Select sentences via heuristics.  
   - **Semantic:** Cluster and summarize vectors.

3. **When to use each type?**  
   - **LLM-Based:** Flexible; advantages: coherent; but costly—use sparingly in agents.  
   - **Extractive:** Speed-critical; advantages: fast; for real-time chat.  
   - **Semantic:** Dense docs; advantages: lossy but targeted; pair with embeddings.  
   *Added Insight:* Essential for long-context models, enabling agent loops without token overflow.

### Query Expansion
**Short Summary:** Expansion rewrites queries to capture synonyms/related terms, improving recall.

1. **What is it?**  
   Generating alternative query formulations (e.g., "AI ethics" → "machine learning morality") for broader retrieval.

2. **What are the types?**  
   - **Lexical:** Thesaurus-based.  
   - **LLM-Generated:** Hypothetical expansions.  
   - **Embedding-Based:** Nearest neighbors in vector space.

3. **When to use each type?**  
   - **Lexical:** Simple terms; advantages: lightweight; basic search.  
   - **LLM-Generated:** Nuanced; advantages: creative; for ambiguous agent queries.  
   - **Embedding-Based:** Semantic gaps; advantages: automatic; in multi-query retrievers.  
   *Added Insight:* In self-reflective RAG, agents expand based on prior failures, ascending accuracy over iterations.

### Multi-Hop Retrieval
**Short Summary:** Multi-hop chains multiple retrievals to answer questions needing intermediate steps, like detective work.

1. **What is it?**  
   Iterative retrieval where answers from one hop inform the next (e.g., "Who founded company X? Where is it based?").

2. **What are the types?**  
   - **Query Decomposition:** Breaks into sub-queries.  
   - **Iterative Retrieval:** Refines based on partial results.  
   - **Graph-Based:** Traverses knowledge graphs.

3. **When to use each type?**  
   - **Query Decomposition:** Complex QA; advantages: parallelizable; in planning agents.  
   - **Iterative:** Exploratory; advantages: adaptive; for research workflows.  
   - **Graph-Based:** Relational data; advantages: efficient paths; see Graph RAG.  
   *Added Insight:* Aligns with ReAct patterns, where agents "hop" via tool calls for grounded reasoning.

### Fusion Retrieval
**Short Summary:** Fusion merges results from multiple retrievers, combining strengths for superior hits.

1. **What is it?**  
   Aggregating and re-scoring outputs from diverse sources (e.g., vector + keyword) into a unified ranked list.

2. **What are the types?**  
   - **Reciprocal Rank Fusion (RRF):** Score blending without retraining.  
   - **Learned Fusion:** ML model to weigh sources.  
   - **Ensemble:** Simple averaging.

3. **When to use each type?**  
   - **RRF:** Quick integration; advantages: no training; hybrid setups.  
   - **Learned:** Tuned performance; advantages: optimized; production RAG.  
   - **Ensemble:** Prototyping; advantages: easy; for multi-modal fusion.  
   *Added Insight:* Boosts agent robustness by diversifying sources, reducing single-point failures.

### HyDE Retrieval
**Short Summary:** HyDE (Hypothetical Document Embeddings) generates fake docs from queries for better matching.

1. **What is it?**  
   LLM creates a hypothetical answer, embeds it, then retrieves similar real docs—bridging query-doc gaps.

2. **What are the types?**  
   - **Zero-Shot HyDE:** Direct hypothetical generation.  
   - **Few-Shot HyDE:** With example docs.  
   - **Iterative HyDE:** Refines hypotheses.

3. **When to use each type?**  
   - **Zero-Shot:** Sparse data; advantages: simple; for emerging topics.  
   - **Few-Shot:** Domain-specific; advantages: guided; in knowledge graphs.  
   - **Iterative:** Hard queries; advantages: precise; agentic loops.  
   *Added Insight:* Clever for cold-start RAG, where agents use HyDE to bootstrap weak indices.

---

## C. Advanced RAG

### Agentic RAG
**Short Summary:** Agentic RAG empowers LLMs with agency to orchestrate retrieval, deciding when/how to fetch data dynamically.

1. **What is it?**  
   RAG variant where an agent plans, retrieves, verifies, and generates, using tools for adaptive search.

2. **What are the types?**  
   - **Single-Agent:** One LLM handles all.  
   - **Multi-Agent:** Specialized roles (e.g., retriever agent).  
   - **Hierarchical:** Supervisor oversees sub-agents.

3. **When to use each type?**  
   - **Single-Agent:** Simple augmentation; advantages: lightweight; basic QA.  
   - **Multi-Agent:** Complex domains; advantages:分工; collaborative research.  
   - **Hierarchical:** Large-scale; advantages: scalable; enterprise knowledge bases.  
   *Added Insight:* Builds on ReAct—agents reflect on retrieval quality, self-optimizing for ascending performance.

### Self-Reflective RAG
**Short Summary:** Self-reflective RAG has the system critique and iterate on its own outputs, like a built-in editor.

1. **What is it?**  
   LLM evaluates generated responses (e.g., "Is this factual?"), triggering re-retrieval or refinement.

2. **What are the types?**  
   - **Output Reflection:** Post-generation check.  
   - **Process Reflection:** Mid-retrieval critique.  
   - **Feedback-Driven:** Uses user scores for loops.

3. **When to use each type?**  
   - **Output:** Hallucination-prone tasks; advantages: quick fixes; chat apps.  
   - **Process:** Multi-hop; advantages: early corrections; planning workflows.  
   - **Feedback-Driven:** Interactive; advantages: personalizes; long-term agents.  
   *Added Insight:* Integrates with memory—store reflections as episodic knowledge for evolving accuracy.

### Graph RAG
**Short Summary:** Graph RAG uses knowledge graphs for structured retrieval, connecting entities for richer context.

1. **What is it?**  
   Builds/retrieves from graphs (nodes=entities, edges=relations) to answer relational queries beyond flat vectors.

2. **What are the types?**  
   - **Entity-Centric:** Focuses on key nodes.  
   - **Path-Based:** Traverses connections.  
   - **Community Detection:** Clusters subgraphs.

3. **When to use each type?**  
   - **Entity-Centric:** Who/what questions; advantages: targeted; biomedical RAG.  
   - **Path-Based:** How/why; advantages: explanatory; supply chain analysis.  
   - **Community:** Broad overviews; advantages: summarizes; trend detection agents.  
   *Added Insight:* Complements vector search—hybrid for agents navigating "knowledge neighborhoods."

### Knowledge-Graph-Based RAG
**Short Summary:** KG-RAG leverages explicit graphs for retrieval, emphasizing relations over raw text similarity.

1. **What is it?**  
   Indexes knowledge as graphs, retrieves subgraphs, then generates using relational context.

2. **What are the types?**  
   - **Static KG:** Pre-built graphs.  
   - **Dynamic KG:** LLM-extracted on-the-fly.  
   - **Hybrid KG:** Graphs + embeddings.

3. **When to use each type?**  
   - **Static:** Stable domains (e.g., Wikipedia); advantages: fast; encyclopedic QA.  
   - **Dynamic:** Evolving data; advantages: adaptive; news summarization.  
   - **Hybrid:** Comprehensive; advantages: versatile; multi-agent collaboration.  
   *Added Insight:* Agents use KG for planning—e.g., traverse to subtask breakdown in workflows.

### Multimodal RAG (Images/Audio/Tables)
**Short Summary:** Multimodal RAG extends to non-text, retrieving/generating across modalities like vision-language models.

1. **What is it?**  
   Retrieves and fuses embeddings from images, audio, tables with text for holistic responses.

2. **What are the types?**  
   - **Vision RAG:** Image+text (e.g., CLIP embeddings).  
   - **Audio RAG:** Speech-to-text + transcripts.  
   - **Tabular RAG:** Structured data querying.

3. **When to use each type?**  
   - **Vision:** Visual search (e.g., product catalogs); advantages: descriptive; e-commerce agents.  
   - **Audio:** Podcasts; advantages: searchable transcripts; media analysis.  
   - **Tabular:** Reports; advantages: precise filters; finance dashboards.  
   *Added Insight:* Future-proof for agents—e.g., multimodal loops where image retrieval triggers audio transcription.

### LLM-as-a-Retriever
**Short Summary:** Uses LLMs directly for retrieval, bypassing traditional vector search for interpretive matching.

1. **What is it?**  
   Prompts LLM to rank or generate candidate docs from a corpus, leveraging reasoning over embeddings.

2. **What are the types?**  
   - **Zero-Shot Retrieval:** Direct ranking.  
   - **Few-Shot:** With example matches.  
   - **Chain-of-Retrieval:** Step-wise selection.

3. **When to use each type?**  
   - **Zero-Shot:** Small corpora; advantages: no indexing; quick prototypes.  
   - **Few-Shot:** Specialized; advantages: tuned; domain QA.  
   - **Chain:** Complex; advantages: reasoned; reflective agents.  
   *Added Insight:* Costly but interpretable—hybrid with vectors for cost-effective agent decisions.

### RAG Optimization Strategies
**Short Summary:** Strategies fine-tune RAG for speed, accuracy, and cost, like performance tuning for search engines.

1. **What is it?**  
   Techniques to enhance retrieval quality, reduce latency, and minimize compute.

2. **What are the types?**  
   - **Indexing Opts:** Better chunking/embeddings.  
   - **Query Opts:** Expansion/reranking.  
   - **Generation Opts:** Compression/guardrails.

3. **When to use each type?**  
   - **Indexing:** Build phase; advantages: upfront gains; large-scale deployment.  
   - **Query:** Runtime; advantages: adaptive; high-traffic apps.  
   - **Generation:** Post-retrieval; advantages: focused; hallucination control in agents.  
   *Added Insight:* A/B test in observability setups—agents can even optimize via self-reflection on metrics.

---

## D. Memory Concepts

### Short-Term Memory
**Short Summary:** Short-term memory holds recent conversation history, like working memory for immediate context.

1. **What is it?**  
   Temporary storage of the last N turns or tokens, enabling coherent multi-turn interactions.

2. **What are the types?**  
   - **Buffer Memory:** Simple FIFO queue.  
   - **Token-Limited:** Truncates to window size.  
   - **Summary Buffer:** Condenses history.

3. **When to use each type?**  
   - **Buffer:** Casual chats; advantages: easy; low overhead.  
   - **Token-Limited:** Long sessions; advantages: fits models; default in chains.  
   - **Summary:** Extended dialogues; advantages: scalable; agent continuity.  
   *Added Insight:* In ReAct agents, short-term tracks action-observations for loop stability.

### Long-Term Memory
**Short Summary:** Long-term persists info across sessions, like a notebook for recurring users.

1. **What is it?**  
   Durable storage (e.g., DB) for user data, retrieved on demand to personalize.

2. **What are the types?**  
   - **Key-Value Store:** Simple pairs.  
   - **Vector Memory:** Embeddings for semantic recall.  
   - **Graph Memory:** Relational links.

3. **When to use each type?**  
   - **Key-Value:** Preferences; advantages: fast lookup; user profiles.  
   - **Vector:** Vague recalls; advantages: flexible; RAG integration.  
   - **Graph:** Complex histories; advantages: interconnected; multi-session agents.  
   *Added Insight:* Checkpoint in workflows to save state, enabling resumable agent tasks.

### Summary Memory
**Short Summary:** Summarizes past interactions to compress history, retaining essence without bloat.

1. **What is it?**  
   LLM-generated abstracts of conversations, updated incrementally for efficient recall.

2. **What are the types?**  
   - **Conversation Summary:** Thread-level.  
   - **Entity Summary:** Key facts only.  
   - **Thematic:** Grouped by topics.

3. **When to use each type?**  
   - **Conversation:** Narratives; advantages: holistic; therapy bots.  
   - **Entity:** Fact-heavy; advantages: concise; CRM agents.  
   - **Thematic:** Diverse talks; advantages: organized; research assistants.  
   *Added Insight:* Ascending from short to long-term via periodic summaries, reducing token costs by 80%.

### Entity Memory
**Short Summary:** Tracks specific entities (people, places) extracted from chats, building a personal knowledge base.

1. **What is it?**  
   Stores and updates facts about named entities for consistent referencing.

2. **What are the types?**  
   - **Static Extraction:** One-time NER.  
   - **Dynamic:** Real-time updates.  
   - **Resolved:** Links synonyms (e.g., NYC = New York).

3. **When to use each type?**  
   - **Static:** Batch processing; advantages: simple; initial setups.  
   - **Dynamic:** Live chats; advantages: fresh; interactive agents.  
   - **Resolved:** Ambiguous; advantages: accurate; global users.  
   *Added Insight:* Feeds into KG memory for agent planning, e.g., recalling user prefs in recommendations.

### Episodic Memory
**Short Summary:** Stores event sequences from interactions, like a diary for "what happened when."

1. **What is it?**  
   Timestamped records of past episodes, retrieved for contextual storytelling.

2. **What are the types?**  
   - **Linear Logs:** Chronological.  
   - **Indexed:** By keywords/events.  
   - **Narrative:** Story-form summaries.

3. **When to use each type?**  
   - **Linear:** Simple recall; advantages: truthful; journaling apps.  
   - **Indexed:** Searchable; advantages: quick; task trackers.  
   - **Narrative:** Engaging; advantages: human-like; companion agents.  
   *Added Insight:* In action loops, episodic aids error recovery by replaying failures.

### Semantic Memory
**Short Summary:** Captures general knowledge and patterns learned from interactions, abstracting beyond specifics.

1. **What is it?**  
   Vector-stored concepts and relations, enabling inference on themes.

2. **What are the types?**  
   - **Factoid:** Isolated facts.  
   - **Associative:** Linked ideas.  
   - **Procedural:** How-to knowledge.

3. **When to use each type?**  
   - **Factoid:** Trivia; advantages: precise; quiz agents.  
   - **Associative:** Brainstorming; advantages: creative; ideation.  
   - **Procedural:** Tutorials; advantages: step-wise; skill-building bots.  
   *Added Insight:* Mirrors human cognition—agents use for generalization in new scenarios.

### Knowledge Graph Memory
**Short Summary:** Represents memory as a graph of entities and relations, for structured, queryable recall.

1. **What is it?**  
   Builds/updates a personal KG from interactions, traversed for insights.

2. **What are the types?**  
   - **User-Centric:** Personal facts.  
   - **Shared:** Collaborative graphs.  
   - **Domain-Specific:** Themed subgraphs.

3. **When to use each type?**  
   - **User-Centric:** Individual; advantages: private; personal assistants.  
   - **Shared:** Teams; advantages: collective; project management.  
   - **Domain:** Experts; advantages: deep; scientific agents.  
   *Added Insight:* Synergizes with Graph RAG—agents query for planning, e.g., relationship mapping in networking.

---

## E. Chain & Workflow Concepts (LangChain / LangGraph or Generic)

### LLMChain
**Short Summary:** LLMChain is a basic building block linking prompts to LLM calls, like a simple recipe.

1. **What is it?**  
   A sequence: input → prompt template → LLM → output parser.

2. **What are the types?**  
   - **Simple Chain:** Single LLM call.  
   - **Prompt Chain:** With variables.  
   - **Output Chain:** Parsed results.

3. **When to use each type?**  
   - **Simple:** One-off generations; advantages: minimal; text completion.  
   - **Prompt:** Dynamic; advantages: reusable; templated QA.  
   - **Output:** Structured; advantages: JSON-safe; API integrations.  
   *Added Insight:* Foundation for agents—extend with tools for action chains.

### RetrievalQA Chain
**Short Summary:** RetrievalQA combines RAG in a chain: retrieve → prompt with context → generate answer.

1. **What is it?**  
   End-to-end for question-answering over docs, grounding LLM in retrieved info.

2. **What are the types?**  
   - **Stuff:** All docs in one prompt.  
   - **Map-Reduce:** Summarize chunks then aggregate.  
   - **Refine:** Iterative improvement.

3. **When to use each type?**  
   - **Stuff:** Short contexts; advantages: direct; small datasets.  
   - **Map-Reduce:** Long docs; advantages: parallel; scalable RAG.  
   - **Refine:** Detailed; advantages: cumulative; analytical reports.  
   *Added Insight:* In LangGraph, visualize as nodes for debugging agent retrieval paths.

### Router Chain
**Short Summary:** Router directs inputs to specialized chains based on logic, like a switchboard.

1. **What is it?**  
   Classifies queries and routes to appropriate handlers (e.g., math → calculator chain).

2. **What are the types?**  
   - **LLM Router:** Model decides.  
   - **Rule-Based:** If-then rules.  
   - **Fallback:** Default chain.

3. **When to use each type?**  
   - **LLM Router:** Flexible; advantages: intelligent; multi-domain agents.  
   - **Rule-Based:** Predictable; advantages: fast; keyword routing.  
   - **Fallback:** Robust; advantages: safe; error-prone setups.  
   *Added Insight:* Key for multi-agent systems—routes subtasks ascending complexity.

### Sequential Chains
**Short Summary:** Sequential chains execute steps in order, passing outputs as inputs, like an assembly line.

1. **What is it?**  
   Linear workflow: Chain1 output → Chain2 input → ... → final.

2. **What are the types?**  
   - **Simple Sequential:** Fixed order.  
   - **Conditional:** Branches on conditions.  
   - **Parallelizable:** Non-dependent steps.

3. **When to use each type?**  
   - **Simple:** Pipelines (e.g., summarize then translate); advantages: straightforward; ETL processes.  
   - **Conditional:** Decision flows; advantages: adaptive; ReAct-like.  
   - **Parallel:** Independent tasks; advantages: faster; batch agents.  
   *Added Insight:* Use state management to track variables, enabling checkpointing for resumability.

### Tool Chains
**Short Summary:** Tool chains integrate external functions into sequences, empowering LLMs with real-world actions.

1. **What is it?**  
   Chains that invoke tools (e.g., search API) mid-flow, based on LLM decisions.

2. **What are the types?**  
   - **Bound Tools:** Pre-attached to LLM.  
   - **Dynamic:** Runtime selection.  
   - **Composed:** Tool outputs feed next chain.

3. **When to use each type?**  
   - **Bound:** Consistent; advantages: simple; fixed-tool agents.  
   - **Dynamic:** Versatile; advantages: selective; planning workflows.  
   - **Composed:** Complex; advantages: modular; RAG-tool hybrids.  
   *Added Insight:* Central to autonomous agents—error recovery via tool retries.

### Graph Workflows
**Short Summary:** Graph workflows model flows as nodes/edges, allowing cycles and parallelism beyond linear chains.

1. **What is it?**  
   Directed graphs where nodes are actions (e.g., LLM calls), edges define flow (LangGraph style).

2. **What are the types?**  
   - **DAG (Directed Acyclic Graph):** No loops, for pipelines.  
   - **Cyclic Graphs:** With feedback loops.  
   - **Stateful Graphs:** Persistent state across runs.

3. **When to use each type?**  
   - **DAG:** One-pass; advantages: predictable; data processing.  
   - **Cyclic:** Iterative; advantages: refining; reflective RAG.  
   - **Stateful:** Long-running; advantages: memoryful; persistent agents.  
   *Added Insight:* Ideal for multi-agent coordination—nodes as agents, edges as messages.

### Nodes and State Management
**Short Summary:** Nodes are executable units in graphs; state is shared data evolving through the workflow.

1. **What is it?**  
   Nodes: Functions/tools; State: Dict-like object passed between, updated immutably.

2. **What are the types?** (Nodes)  
   - **Action Nodes:** LLM/tools.  
   - **Decision Nodes:** Branching logic.  
   - **End Nodes:** Outputs.  
   (State: Simple dict, Persistent DB-backed.)

3. **When to use each type?**  
   - **Action:** Computations; advantages: core logic; tool calls.  
   - **Decision:** Routing; advantages: conditional; agent planning.  
   - **End:** Termination; advantages: clean; summaries.  
   *Added Insight:* Immutable state prevents bugs—key for scalable, debuggable agent systems.

### Checkpointing
**Short Summary:** Checkpointing saves workflow state at points, allowing pauses/resumes like save points in games.

1. **What is it?**  
   Periodic serialization of state to storage, for recovery or human-in-loop.

2. **What are the types?**  
   - **In-Memory:** Volatile, fast.  
   - **Persistent:** DB/file-based.  
   - **Versioned:** With history.

3. **When to use each type?**  
   - **In-Memory:** Short runs; advantages: quick; testing.  
   - **Persistent:** Production; advantages: reliable; long agents.  
   - **Versioned:** Auditing; advantages: traceable; compliance.  
   *Added Insight:* Enables error recovery in loops—agents rollback on failures.

---

## F. Embedding & Vector Search Concepts

### Dense vs Sparse Embeddings
**Short Summary:** Dense pack meaning into compact vectors; sparse use keyword weights—trade-offs in expressiveness vs. efficiency.

1. **What is it?**  
   Embeddings as vectors: dense (low-dim, full values) vs. sparse (high-dim, mostly zeros).

2. **What are the types?** (Beyond dense/sparse: See hybrid below)  
   - **Dense:** Neural-derived.  
   - **Sparse:** Count-based (e.g., bag-of-words).

3. **When to use each type?**  
   - **Dense:** Semantic tasks; advantages: nuanced similarity; RAG core.  
   - **Sparse:** Exact matches; advantages: lightweight; legacy search.  
   *Added Insight:* Agents favor dense for planning (e.g., goal similarity), sparse for filtering.

### Hybrid Embeddings
**Short Summary:** Hybrid merges dense/sparse for comprehensive representation, capturing both semantics and keywords.

1. **What is it?**  
   Combined vectors where scores from both are fused (e.g., weighted sum).

2. **What are the types?**  
   - **Late Fusion:** Score after separate retrievals.  
   - **Early Fusion:** Joint embedding space.  
   - **Learned:** Trained combiner.

3. **When to use each type?**  
   - **Late:** Modular; advantages: easy; quick hybrids.  
   - **Early:** Unified; advantages: optimized; advanced RAG.  
   - **Learned:** High-precision; advantages: tuned; production.  
   *Added Insight:* Boosts recall in noisy data—agents use for robust query expansion.

### Similarity Metrics (Cosine, Dot Product, Euclidean)
**Short Summary:** Metrics quantify vector closeness, guiding retrieval relevance.

1. **What is it?**  
   Mathematical distances: cosine (angle), dot (direction+magnitude), Euclidean (straight-line).

2. **What are the types?**  
   - **Cosine Similarity:** Normalized angle (0-1).  
   - **Dot Product:** Raw projection.  
   - **Euclidean Distance:** L2 norm (lower better).

3. **When to use each type?**  
   - **Cosine:** Direction-focused (e.g., text); advantages: scale-invariant; default for embeddings.  
   - **Dot:** Unnormalized; advantages: faster; when magnitude matters (e.g., importance).  
   - **Euclidean:** Geometric; advantages: intuitive; small datasets.  
   *Added Insight:* Normalize vectors for consistency—critical in agent memory for accurate recalls.

### ANN Search Algorithms (HNSW, IVF, PQ)
**Short Summary:** ANN approximates nearest neighbors fast for large-scale vector search, trading tiny accuracy for speed.

1. **What is it?**  
   Efficient indexing to find top-k similars without exhaustive checks.

2. **What are the types?**  
   - **HNSW:** Graph navigation.  
   - **IVF:** Cluster centroids + scan.  
   - **PQ (Product Quantization):** Compresses vectors.

3. **When to use each type?**  
   - **HNSW:** Real-time; advantages: high recall, log time; vector DB staple.  
   - **IVF:** Balanced; advantages: scalable; medium-large indices.  
   - **PQ:** Memory-constrained; advantages: 90% smaller; mobile agents.  
   *Added Insight:* Tune ef_search for precision-speed trade-off in dynamic RAG.

### Dimensionality Reduction
**Short Summary:** Reduces vector dims while preserving structure, easing computation without much info loss.

1. **What is it?**  
   Techniques like PCA to project high-dim embeddings to lower (e.g., 1536 → 128).

2. **What are the types?**  
   - **PCA (Linear):** Variance-based.  
   - **t-SNE:** Non-linear visualization.  
   - **UMAP:** Topology-preserving.

3. **When to use each type?**  
   - **PCA:** Speedups; advantages: fast, linear; preprocessing.  
   - **t-SNE:** Clustering viz; advantages: perceptual; analysis.  
   - **UMAP:** General reduction; advantages: scalable; RAG tuning.  
   *Added Insight:* Post-reduction, re-embed for agents to maintain quality in low-resource setups.

### Vector Normalization
**Short Summary:** Normalization scales vectors to unit length, ensuring fair similarity comparisons.

1. **What is it?**  
   Divides by L2 norm so ||v||=1, focusing on direction.

2. **What are the types?**  
   - **L1 (Manhattan):** Sum abs values.  
   - **L2 (Euclidean):** Sqrt sum squares.  
   - **Min-Max:** Bounds to [0,1].

3. **When to use each type?**  
   - **L1:** Sparse data; advantages: robust to outliers.  
   - **L2:** Dense; advantages: standard for cosine; embeddings default.  
   - **Min-Max:** Bounded; advantages: interpretable; custom metrics.  
   *Added Insight:* Always normalize before cosine—prevents magnitude biases in agent searches.

---

## G. Agent Concepts (LLM Agents)

### What is an AI Agent?
**Short Summary:** An AI agent is an autonomous entity that senses its environment, reasons, and acts to achieve goals, powered by LLMs.

1. **What is it?**  
   A system with perception (inputs), cognition (LLM), and action (tools), operating in loops to fulfill objectives.

2. **What are the types?**  
   - **Simple Reflex:** Input → output, no memory.  
   - **Model-Based:** Internal world model.  
   - **Goal-Based:** Plans toward ends.  
   - **Utility-Based:** Optimizes preferences.  
   - **Learning:** Adapts from experience.

3. **When to use each type?**  
   - **Simple Reflex:** Reactive tasks; advantages: fast; alarms.  
   - **Model-Based:** Predictable envs; advantages: simulates; games.  
   - **Goal-Based:** Directed; advantages: flexible; assistants.  
   - **Utility-Based:** Trade-offs; advantages: optimal; resource alloc.  
   - **Learning:** Evolving; advantages: improves; personalized.  
   *Added Insight:* LLM agents ascend from reflex to learning via memory integration.

### Tool-Using Agents
**Short Summary:** Tool-using agents extend LLMs by calling external APIs/tools, acting as "doers" not just "talkers."

1. **What is it?**  
   Agents that decide, invoke, and incorporate tool results in reasoning cycles.

2. **What are the types?**  
   - **Pre-Defined Tools:** Fixed set.  
   - **Dynamic Discovery:** Learns new tools.  
   - **Compositional:** Builds tool combos.

3. **When to use each type?**  
   - **Pre-Defined:** Controlled; advantages: safe; enterprise.  
   - **Dynamic:** Open; advantages: versatile; research.  
   - **Compositional:** Complex; advantages: creative; automation.  
   *Added Insight:* Tool selection via embeddings—matches query to tool descriptions.

### Planning Agents
**Short Summary:** Planning agents decompose goals into steps, forecasting actions for efficient execution.

1. **What is it?**  
   Use LLMs to generate plans (e.g., hierarchies, milestones) before acting.

2. **What are the types?**  
   - **Hierarchical:** High-level then details.  
   - **Linear:** Sequential steps.  
   - **Contingency:** With branches for risks.

3. **When to use each type?**  
   - **Hierarchical:** Big projects; advantages: manageable; software dev.  
   - **Linear:** Straightforward; advantages: simple; recipes.  
   - **Contingency:** Uncertain; advantages: resilient; travel planning.  
   *Added Insight:* CoT for plan generation, ToT for exploration in uncertain domains.

### ReAct Agents
**Short Summary:** ReAct interleaves Reasoning and Acting in a loop: think → act → observe → repeat.

1. **What is it?**  
   Framework for grounded decision-making, reducing errors by observing real feedback.

2. **What are the types?**  
   - **Basic ReAct:** Text-based.  
   - **Tool-ReAct:** With APIs.  
   - **Multi-Step ReAct:** Extended loops.

3. **When to use each type?**  
   - **Basic:** Simulations; advantages: interpretable; prototyping.  
   - **Tool:** Real-world; advantages: practical; web agents.  
   - **Multi-Step:** Puzzles; advantages: persistent; problem-solving.  
   *Added Insight:* Foundational pattern—extend with memory for stateful ReAct in long tasks.

### Autonomous Agents
**Short Summary:** Autonomous agents operate independently, self-managing goals and adaptations without constant supervision.

1. **What is it?**  
   Self-sustaining systems that set subgoals, learn, and recover, like digital employees.

2. **What are the types?**  
   - **Single-Task:** Focused autonomy.  
   - **Open-Ended:** General purpose.  
   - **Swarm:** Group autonomy.

3. **When to use each type?**  
   - **Single-Task:** Narrow; advantages: reliable; monitoring tools.  
   - **Open-Ended:** Versatile; advantages: broad; personal AI.  
   - **Swarm:** Collaborative; advantages: emergent; simulations.  
   *Added Insight:* Use checkpoints for safety—autonomy with human veto points.

### Multi-Agent Systems
**Short Summary:** Multi-agent involves teams of specialized agents collaborating, like a virtual organization.

1. **What is it?**  
   Agents communicate, delegate, and coordinate via messages or shared state.

2. **What are the types?**  
   - **Centralized:** One supervisor.  
   - **Decentralized:** Peer-to-peer.  
   - **Hierarchical:** Layers of command.

3. **When to use each type?**  
   - **Centralized:** Coordinated; advantages: oversight; project mgmt.  
   - **Decentralized:** Flexible; advantages: robust; brainstorming.  
   - **Hierarchical:** Scaled; advantages: efficient; org sims.  
   *Added Insight:* Role prompting for agents—e.g., debater vs. synthesizer in consensus.

### Tool Selection
**Short Summary:** Tool selection chooses optimal tools for tasks, like picking the right utensil.

1. **What is it?**  
   LLM or heuristic ranks tools by relevance to current state/goal.

2. **What are the types?**  
   - **Semantic Matching:** Embed tool descs.  
   - **Rule-Based:** Preconditions.  
   - **LLM-Judged:** Prompted choice.

3. **When to use each type?**  
   - **Semantic:** Large toolsets; advantages: scalable; dynamic envs.  
   - **Rule-Based:** Deterministic; advantages: predictable; safety-critical.  
   - **LLM-Judged:** Nuanced; advantages: reasoned; complex planning.  
   *Added Insight:* Few-shot examples tune selection, reducing misfires in loops.

### Planning & Subtask Breakdown
**Short Summary:** Breaks high-level goals into actionable subtasks, enabling divide-and-conquer.

1. **What is it?**  
   LLM generates a task tree or list, assigns priorities, and tracks progress.

2. **What are the types?**  
   - **Decomposition:** Top-down split.  
   - **Milestone:** Phased with checks.  
   - **Dynamic:** Replans on feedback.

3. **When to use each type?**  
   - **Decomposition:** Structured; advantages: clear; writing aids.  
   - **Milestone:** Monitored; advantages: verifiable; projects.  
   - **Dynamic:** Adaptive; advantages: resilient; real-time.  
   *Added Insight:* Graph workflows visualize breakdowns for agent transparency.

### Action–Observation Loops
**Short Summary:** Loops where agents act, observe outcomes, and adjust, core to iterative improvement.

1. **What is it?**  
   Cycle: Plan action → Execute → Perceive result → Update belief → Repeat.

2. **What are the types?**  
   - **Closed-Loop:** Full feedback.  
   - **Open-Loop:** No observation.  
   - **Predictive:** Anticipates outcomes.

3. **When to use each type?**  
   - **Closed:** Interactive; advantages: corrective; ReAct staple.  
   - **Open:** Batch; advantages: simple; non-feedback tasks.  
   - **Predictive:** Fast; advantages: proactive; simulations.  
   *Added Insight:* Memory buffers observations, ascending agent intelligence over time.

### Error Recovery
**Short Summary:** Mechanisms to detect and fix failures, keeping agents resilient like fault-tolerant software.

1. **What is it?**  
   Strategies to handle exceptions (e.g., tool errors) via retries, fallbacks, or replanning.

2. **What are the types?**  
   - **Retry Logic:** Exponential backoff.  
   - **Fallback Tools:** Alternatives.  
   - **Reflection:** LLM diagnoses.

3. **When to use each type?**  
   - **Retry:** Transient; advantages: simple; API calls.  
   - **Fallback:** Diverse; advantages: robust; multi-tool.  
   - **Reflection:** Complex; advantages: learning; advanced agents.  
   *Added Insight:* Log errors in episodic memory for pattern-based prevention.

---

## H. Model Training Concepts

### Fine-Tuning
**Short Summary:** Fine-tuning adapts pre-trained LLMs to specific tasks by further training on custom data.

1. **What is it?**  
   Updates model weights on domain data, improving performance while retaining general knowledge.

2. **What are the types?**  
   - **Full Fine-Tuning:** All parameters.  
   - **Parameter-Efficient (PEFT):** Subsets only.  
   - **Instruction Tuning:** On prompt-response pairs.

3. **When to use each type?**  
   - **Full:** High customization; advantages: optimal; but resource-heavy—small teams avoid.  
   - **PEFT:** Resource-limited; advantages: fast, low VRAM; LoRA default.  
   - **Instruction:** Chat alignment; advantages: versatile; agent behaviors.  
   *Added Insight:* Post-RAG, fine-tune on retrieved pairs for grounded generation.

### LoRA / QLoRA
**Short Summary:** LoRA adds low-rank adapters for efficient tuning; QLoRA quantizes for even less memory.

1. **What is it?**  
   LoRA: Train small matrices injected into layers; QLoRA: 4-bit quantized base model.

2. **What are the types?**  
   - **LoRA:** Standard adapters.  
   - **QLoRA:** Quantized variant.  
   - **DoRA:** Decomposed for better generalization.

3. **When to use each type?**  
   - **LoRA:** General PEFT; advantages: 0.1% params tuned; consumer GPUs.  
   - **QLoRA:** Memory-tight; advantages: 1GB VRAM; mobile/edge agents.  
   - **DoRA:** Advanced; advantages: magnitude-aware; research.  
   *Added Insight:* Tune embeddings separately with LoRA for custom RAG retrievers.

### Prompt Tuning
**Short Summary:** Prompt tuning optimizes soft prompts (learnable vectors) instead of model weights, ultra-efficient.

1. **What is it?**  
   Trains prefix tokens added to inputs, keeping the LLM frozen.

2. **What are the types?**  
   - **Soft Prompts:** Continuous embeddings.  
   - **Prefix Tuning:** Layer-specific.  
   - **P-Tuning:** Mixed discrete/continuous.

3. **When to use each type?**  
   - **Soft:** Simple tasks; advantages: tiny footprint; quick experiments.  
   - **Prefix:** Deeper adaptation; advantages: targeted; mid-sized models.  
   - **P-Tuning:** Hybrid; advantages: flexible; multilingual.  
   *Added Insight:* Ideal for agent role prompts—tune per persona without full retrain.

### Knowledge Distillation
**Short Summary:** Distillation transfers knowledge from a large "teacher" model to a smaller "student," for deployment efficiency.

1. **What is it?**  
   Student mimics teacher's soft predictions on data, compressing size/speed.

2. **What are the types?**  
   - **Offline:** Teacher fixed.  
   - **Online:** Both train together.  
   - **Self-Distillation:** Model teaches itself.

3. **When to use each type?**  
   - **Offline:** Production; advantages: stable; edge devices.  
   - **Online:** Co-evolving; advantages: synergistic; continual learning.  
   - **Self:** Solo; advantages: no extra model; agent fine-tuning.  
   *Added Insight:* Distill RAG-tuned teachers for lightweight agent brains.

### Quantization
**Short Summary:** Quantization reduces precision (e.g., FP32 → INT8) to shrink models, trading minor accuracy for speed/memory.

1. **What is it?**  
   Maps weights/activations to lower-bit formats, enabling faster inference.

2. **What are the types?**  
   - **Post-Training (PTQ):** After training.  
   - **Quantization-Aware Training (QAT):** During training.  
   - **Binary/Ternary:** Extreme low-bit.

3. **When to use each type?**  
   - **PTQ:** Quick; advantages: no retrain; baselines.  
   - **QAT:** Accurate; advantages: calibrated; high-perf.  
   - **Binary:** Ultra-light; advantages: 32x smaller; embedded agents.  
   *Added Insight:* QLoRA combines with quantization for fine-tuning on laptops.

---

## I. System Design Concepts

### Caching (Embedding Cache, Semantic Cache, Response Cache)
**Short Summary:** Caching stores pre-computed results to avoid recomputation, speeding up repeated operations.

1. **What is it?**  
   Temporary storage for embeddings, similar queries, or full responses with TTL/eviction.

2. **What are the types?**  
   - **Embedding Cache:** Vector pre-computes.  
   - **Semantic Cache:** Clusters similar inputs.  
   - **Response Cache:** Exact output hits.

3. **When to use each type?**  
   - **Embedding:** Indexing; advantages: build-time save; RAG pipelines.  
   - **Semantic:** Fuzzy matches; advantages: 50% hit rate boost; chat apps.  
   - **Response:** Identical queries; advantages: instant; FAQs.  
   *Added Insight:* Agents cache tool results in short-term memory for loop efficiency.

### Scaling (Horizontal, Vector DB Sharding)
**Short Summary:** Scaling distributes load across resources; sharding partitions vector DBs for parallelism.

1. **What is it?**  
   Horizontal: Add instances; Sharding: Split data by keys (e.g., hash).

2. **What are the types?**  
   - **Horizontal:** Replicas for read.  
   - **Vertical:** Bigger machines.  
   - **Sharding:** Data partitioning.

3. **When to use each type?**  
   - **Horizontal:** High traffic; advantages: fault-tolerant; cloud agents.  
   - **Vertical:** Compute-bound; advantages: simple; monoliths.  
   - **Sharding:** Massive DBs; advantages: linear scale; global RAG.  
   *Added Insight:* Auto-scale based on queue length for bursty agent workloads.

### Latency Optimization
**Short Summary:** Techniques to minimize response time, from model choices to async processing.

1. **What is it?**  
   Reducing end-to-end delay via efficient components and parallelism.

2. **What are the types?**  
   - **Model Opts:** Smaller/faster LLMs.  
   - **Pipeline Parallel:** Async stages.  
   - **Caching/Prefetch:** Proactive loads.

3. **When to use each type?**  
   - **Model:** Real-time; advantages: inherent speed; mobile.  
   - **Pipeline:** Chains; advantages: overlap; workflows.  
   - **Caching:** Repeated; advantages: sub-ms; interactive.  
   *Added Insight:* Profile with observability—target <1s for agent loops.

### Observability
**Short Summary:** Observability monitors systems via logs, metrics, traces for debugging and insights.

1. **What is it?**  
   Tools to understand internals: what happened (logs), how (traces), why (metrics).

2. **What are the types?**  
   - **Logging:** Events.  
   - **Metrics:** Counters/gauges.  
   - **Tracing:** Distributed flows.

3. **When to use each type?**  
   - **Logging:** Errors; advantages: searchable; post-mortems.  
   - **Metrics:** Performance; advantages: alerts; SLAs.  
   - **Tracing:** Chains; advantages: bottlenecks; agent graphs.  
   *Added Insight:* Trace ReAct steps for hallucination root causes.

### Rate Limiting
**Short Summary:** Rate limiting caps requests to prevent overload, ensuring fair usage and stability.

1. **What is it?**  
   Throttles API calls (e.g., 100/min per user) with queues or tokens.

2. **What are the types?**  
   - **Fixed Window:** Per time slot.  
   - **Sliding Window:** Rolling.  
   - **Token Bucket:** Bursts allowed.

3. **When to use each type?**  
   - **Fixed:** Simple; advantages: easy; basic APIs.  
   - **Sliding:** Smoother; advantages: fairer; user-facing.  
   - **Token Bucket:** Variable load; advantages: flexible; agents.  
   *Added Insight:* Per-agent limits prevent abuse in multi-user systems.

### Guardrails & Safety
**Short Summary:** Guardrails enforce policies to block harmful/erroneous outputs, promoting safe AI.

1. **What is it?**  
   Checks for toxicity, bias, PII via filters or LLMs.

2. **What are the types?**  
   - **Content Filters:** Keyword/blocklists.  
   - **LLM Moderation:** Generated judgments.  
   - **Circuit Breakers:** Halt on risks.

3. **When to use each type?**  
   - **Content:** Quick; advantages: cheap; initial defense.  
   - **LLM:** Nuanced; advantages: contextual; advanced safety.  
   - **Circuit:** Critical; advantages: preventive; production.  
   *Added Insight:* Embed in system prompts—agents self-guard via reflection.

### Prompt Injection Protection
**Short Summary:** Protects against malicious prompts tricking LLMs (e.g., "Ignore rules"), like input sanitization.

1. **What is it?**  
   Detects/isolates injections via delimiters, validation, or sandboxing.

2. **What are the types?**  
   - **Delimiters:** Separate user/system (e.g., XML tags).  
   - **Validation:** Regex/heuristics.  
   - **Sandbox:** Isolated execution.

3. **When to use each type?**  
   - **Delimiters:** Simple; advantages: lightweight; chat UIs.  
   - **Validation:** Proactive; advantages: blocks; APIs.  
   - **Sandbox:** High-risk; advantages: contained; untrusted inputs.  
   *Added Insight:* In RAG, validate retrieved context—agents reject tainted tools.

## J. Agent Patterns

This new section expands on agent architectures, focusing on reusable patterns for building intelligent, adaptive AI systems. Patterns are presented in ascending complexity: from simple loops (ReAct) to collaborative/multi-system designs. Each includes a short summary, definition, types (where applicable), usage scenarios, and added insights tying back to LLM/RAG/memory concepts for holistic integration.

### 1. ReAct Pattern (Reasoning + Action Loop)
**Short Summary:** ReAct interleaves explicit reasoning traces with actions and observations, enabling grounded, iterative problem-solving like a thoughtful experimenter.

1. **What is it? (Definition)**  
   A framework where the agent alternates between generating a rationale (reason), selecting/executing an action (e.g., tool call), and incorporating observations to refine the next step, reducing hallucinations through feedback.

2. **What are the types?**  
   - **Text-Based ReAct:** Pure language reasoning/actions.  
   - **Tool-Integrated ReAct:** With external APIs/tools.  
   - **Multi-Step ReAct:** Extended loops with planning.

3. **When to use each type?**  
   - **Text-Based:** Simulations or low-tool environments (e.g., puzzle-solving); advantages: lightweight, interpretable; best for prototyping reasoning agents.  
   - **Tool-Integrated:** Real-world tasks (e.g., web search + summarize); advantages: practical extensibility; core for RAG-enhanced QA where retrieval is an action.  
   - **Multi-Step:** Complex workflows (e.g., debugging code); advantages: persistent state; use with memory to avoid repetition in long sessions.  
   *Added Insight:* Foundational for ascending agent complexity—pair with Chain-of-Thought for deeper rationales, evolving into self-reflective loops in production.

### 2. Toolformer Pattern (LLM Predicts When to Call Tools)
**Short Summary:** Toolformer trains LLMs to insert special tokens indicating tool needs, making tool use a natural part of generation like inline citations.

1. **What is it? (Definition)**  
   An approach where the model is fine-tuned to predict and embed tool calls (e.g., calculator, API) directly in its output sequence, deciding "when" and "how" based on context.

2. **What are the types?**  
   - **Supervised Toolformer:** Trained on annotated data with tool markers.  
   - **Zero-Shot Toolformer:** Emergent via prompting.  
   - **Multi-Tool:** Handles diverse tools in one pass.

3. **When to use each type?**  
   - **Supervised:** Precise domains (e.g., math-heavy apps); advantages: high accuracy post-tuning; ideal for fine-tuned agents in finance.  
   - **Zero-Shot:** Rapid deployment; advantages: no data needed; best for general assistants with few tools.  
   - **Multi-Tool:** Versatile tasks; advantages: reduces sequential calls; integrate with RAG for dynamic tool selection like "retrieve then translate."  
   *Added Insight:* Enhances tool-calling in workflows—use LoRA for efficient training, bridging to memory-augmented patterns for context-aware predictions.

### 3. Plan-and-Execute Pattern (Planner Model + Executor Model)
**Short Summary:** Separates high-level planning from low-level execution, like a strategist delegating to a doer, for modular and scalable task handling.

1. **What is it? (Definition)**  
   A two-agent setup: a planner decomposes goals into steps, then an executor carries them out, with optional feedback loops for adjustments.

2. **What are the types?**  
   - **Single-Model:** One LLM for both roles.  
   - **Multi-Model:** Specialized LLMs (e.g., GPT-4 planner, smaller executor).  
   - **Hierarchical:** Multi-level planning.

3. **When to use each type?**  
   - **Single-Model:** Simple tasks (e.g., recipe following); advantages: low overhead; quick prototypes.  
   - **Multi-Model:** Resource-optimized; advantages: cost-effective execution; in scaled systems with rate limits.  
   - **Hierarchical:** Large projects (e.g., software dev); advantages: detailed breakdowns; pair with graph workflows for visualization.  
   *Added Insight:* Ascends to multi-agent by adding critics—use episodic memory to store past plans for learning.

### 4. AutoGPT-Style Autonomous Agent Pattern (Goal → Continuous Loop → Tool Use)
**Short Summary:** AutoGPT-like agents pursue open-ended goals via self-directed loops of thought, action, and critique, acting as independent "entrepreneurs."

1. **What is it? (Definition)**  
   An agent that takes a high-level goal, breaks it into subtasks, executes via tools in a loop, self-critiques progress, and iterates until completion or failure.

2. **What are the types?**  
   - **Goal-Driven:** Fixed objective loops.  
   - **Exploratory:** Open-ended discovery.  
   - **Self-Improving:** With built-in reflection.

3. **When to use each type?**  
   - **Goal-Driven:** Defined projects (e.g., "research market trends"); advantages: focused; business automation.  
   - **Exploratory:** Ideation (e.g., "brainstorm inventions"); advantages: creative divergence; RAG for grounding ideas.  
   - **Self-Improving:** Long-term (e.g., personal assistant); advantages: adaptive; integrate semantic memory for pattern recognition.  
   *Added Insight:* Risk of infinite loops—add guardrails and checkpointing; evolves from ReAct by adding autonomy.

### 5. BabyAGI Pattern (Task Creation + Task Execution + Task Prioritization)
**Short Summary:** BabyAGI simulates AGI through a cycle of generating new tasks, executing priorities, and vector-storing results, like a productive to-do list on steroids.

1. **What is it? (Definition)**  
   A loop: LLM creates tasks from goals, prioritizes via embeddings/similarity, executes top ones, and stores outcomes to inform future creation.

2. **What are the types?**  
   - **Vector-Prioritized:** Embedding-based ranking.  
   - **Heuristic-Prioritized:** Rule-based (e.g., urgency).  
   - **LLM-Prioritized:** Prompted scoring.

3. **When to use each type?**  
   - **Vector:** Semantic tasks (e.g., research pipelines); advantages: relevance-focused; ties to RAG for task retrieval.  
   - **Heuristic:** Time-sensitive; advantages: fast, deterministic; daily planners.  
   - **LLM:** Nuanced; advantages: flexible; but costly—use for creative prioritization.  
   *Added Insight:* Builds on memory concepts—use knowledge graphs for task relations, ascending to multi-agent for delegation.

### 6. Chain-of-Thought Agent Pattern (Step-by-Step Reasoning Before Action)
**Short Summary:** Extends CoT to agents by mandating verbose reasoning traces before any action, fostering transparency and better decisions.

1. **What is it? (Definition)**  
   Agents prompted to "think aloud" step-by-step prior to tool calls or outputs, decomposing problems explicitly for improved accuracy.

2. **What are the types?**  
   - **Standard CoT Agent:** Basic step prompts.  
   - **Self-Consistency CoT:** Multiple traces, vote best.  
   - **Decomposed CoT:** Sub-problems per step.

3. **When to use each type?**  
   - **Standard:** Logical tasks (e.g., troubleshooting); advantages: simple boost; entry for ReAct.  
   - **Self-Consistency:** Uncertain domains; advantages: robust; multi-hop RAG verification.  
   - **Decomposed:** Complex (e.g., strategy games); advantages: modular; plan-and-execute hybrid.  
   *Added Insight:* Enhances observability—log traces for debugging; pairs with Tree-of-Thoughts for branching.

### 7. Tree-of-Thoughts Pattern (Explore Multiple Reasoning Branches)
**Short Summary:** ToT agents explore a tree of possible reasoning paths, evaluating and pruning like a decision tree for optimal outcomes.

1. **What is it? (Definition)**  
   Generates multiple thought branches from a prompt, scores them (e.g., via LLM or value function), and expands promising ones to solve problems breadth-first.

2. **What are the types?**  
   - **Breadth-First ToT:** All branches at once.  
   - **Depth-First ToT:** Deep dive per branch.  
   - **Monte Carlo ToT:** Sampling subsets.

3. **When to use each type?**  
   - **Breadth-First:** Creative search (e.g., writing alternatives); advantages: diverse; ideation agents.  
   - **Depth-First:** Optimization; advantages: efficient depth; puzzle solvers.  
   - **Monte Carlo:** Resource-limited; advantages: approximate; scalable simulations.  
   *Added Insight:* Integrates with graph workflows—nodes as branches; use RAG to ground evaluations.

### 8. Reflexion Pattern (Agent Self-Corrects Its Mistakes)
**Short Summary:** Reflexion enables agents to learn from errors by generating verbal feedback on past trajectories, iteratively improving without external labels.

1. **What is it? (Definition)**  
   After a failed action, the agent reflects (e.g., "What went wrong?"), extracts lessons, and incorporates them into future prompts for self-improvement.

2. **What are the types?**  
   - **Trajectory-Based:** Reviews full histories.  
   - **Outcome-Based:** Focuses on final results.  
   - **Peer-Reflexion:** Simulated multi-agent feedback.

3. **When to use each type?**  
   - **Trajectory:** Detailed debugging (e.g., code agents); advantages: holistic; long-loop tasks.  
   - **Outcome:** Quick fixes; advantages: lightweight; error-prone tools.  
   - **Peer:** Collaborative; advantages: diverse views; multi-agent extension.  
   *Added Insight:* Leverages episodic memory for storing reflections—ascending to lifelong learning.

### 9. Multi-Agent Collaboration Pattern (Different Agents Specialize: Researcher, Planner, Coder, Critic)
**Short Summary:** Teams of specialized agents debate, divide labor, and synthesize, mimicking human teams for superior collective intelligence.

1. **What is it? (Definition)**  
   Assign roles (e.g., researcher retrieves, planner sequences, coder implements, critic evaluates) with message-passing for joint goal pursuit.

2. **What are the types?**  
   - **Debate-Style:** Iterative arguments.  
   - **Workflow-Style:** Sequential handoffs.  
   - **Swarm-Style:** Emergent coordination.

3. **When to use each type?**  
   - **Debate:** Consensus needs (e.g., policy analysis); advantages: balanced; reduces bias.  
   - **Workflow:** Linear projects; advantages: efficient; RAG-planner-critic chain.  
   - **Swarm:** Dynamic; advantages: scalable; simulation environments.  
   *Added Insight:* Role prompting per agent—use orchestrator for traffic; ties to graph RAG for shared knowledge.

### 10. Tool-Orchestrator Pattern (An Agent That Decides Which Tool Chain or Workflow to Follow)
**Short Summary:** An orchestrator agent routes tasks to pre-built tool chains or workflows, like a smart dispatcher for modular execution.

1. **What is it? (Definition)**  
   A meta-agent that analyzes queries, selects/mixes tool chains (e.g., RAG chain vs. calculator), and monitors progress.

2. **What are the types?**  
   - **Rule-Based Orchestrator:** If-then routing.  
   - **LLM-Based:** Prompted decisions.  
   - **Learned:** Fine-tuned classifier.

3. **When to use each type?**  
   - **Rule-Based:** Predictable; advantages: fast; simple apps.  
   - **LLM-Based:** Flexible; advantages: contextual; hybrid RAG/tools.  
   - **Learned:** High-volume; advantages: optimized; production scaling.  
   *Added Insight:* Extends router chains—use embeddings for workflow similarity in dynamic envs.

### 11. Memory-Augmented Agent Pattern (Agents with Episodic, Semantic, or Vector Memory)
**Short Summary:** Infuses agents with persistent memory stores, enabling recall, learning, and personalization beyond stateless interactions.

1. **What is it? (Definition)**  
   Agents query/update memory modules (e.g., vector DB for semantics) during loops to inform actions with historical context.

2. **What are the types?**  
   - **Episodic-Augmented:** Event logs.  
   - **Semantic-Augmented:** Abstract knowledge.  
   - **Vector-Augmented:** Embedding-based recall.

3. **When to use each type?**  
   - **Episodic:** Narrative continuity (e.g., therapy bots); advantages: temporal; multi-turn chats.  
   - **Semantic:** Generalization; advantages: compact; cross-task learning.  
   - **Vector:** Fuzzy search; advantages: scalable; RAG-integrated retrieval.  
   *Added Insight:* Hybrid memories for full cognition—checkpoint in loops for resilience.

### 12. Guardrail-Driven Agent Pattern (Agents Operating Under Safety Constraints)
**Short Summary:** Embeds ethical/safety checks into agent loops, ensuring actions align with policies like a compliant operator.

1. **What is it? (Definition)**  
   Agents with inline validations (e.g., toxicity filters, permission checks) that halt or reroute unsafe paths.

2. **What are the types?**  
   - **Pre-Action Guardrails:** Plan-time checks.  
   - **Post-Action:** Outcome reviews.  
   - **Continuous:** Real-time monitoring.

3. **When to use each type?**  
   - **Pre-Action:** Preventive (e.g., data privacy); advantages: efficient; regulated industries.  
   - **Post-Action:** Adaptive; advantages: contextual; error recovery.  
   - **Continuous:** High-risk; advantages: vigilant; autonomous systems.  
   *Added Insight:* LLM-as-guardrail for nuance—integrate with reflexion for self-enforced evolution.

### 13. Orchestrator–Worker Pattern (Coordinator Agent Assigns Tasks to Worker Agents)
**Short Summary:** A central orchestrator decomposes and delegates to worker specialists, optimizing for parallelism and expertise.

1. **What is it? (Definition)**  
   Orchestrator plans/assigns subtasks to workers (e.g., via APIs), aggregates results, and iterates if needed.

2. **What are the types?**  
   - **Synchronous:** Sequential delegation.  
   - **Asynchronous:** Parallel workers.  
   - **Dynamic:** Reassigns mid-process.

3. **When to use each type?**  
   - **Synchronous:** Dependent tasks; advantages: ordered; simple coordination.  
   - **Asynchronous:** Independent; advantages: speed; batch processing.  
   - **Dynamic:** Unpredictable; advantages: flexible; adaptive research.  
   *Added Insight:* Scales multi-agent—use state management for shared progress tracking.

### 14. Retrieval-Augmented Agent Pattern (Agent Uses RAG Iteratively to Improve Answers)
**Short Summary:** Agents weave RAG into decision loops, retrieving/grounding at key steps for fact-checked, evolving responses.

1. **What is it? (Definition)**  
   Combines agentic planning with iterative retrieval (e.g., query → retrieve → reason → re-retrieve if uncertain).

2. **What are the types?**  
   - **Single-Retrieval:** One-shot augmentation.  
   - **Multi-Hop:** Chained retrievals.  
   - **Self-Querying:** Agent generates sub-queries.

3. **When to use each type?**  
   - **Single:** Basic QA; advantages: simple; fast grounding.  
   - **Multi-Hop:** Complex facts; advantages: deep; investigative agents.  
   - **Self-Querying:** Autonomous; advantages: targeted; knowledge-intensive tasks.  
   *Added Insight:* Agentic RAG variant—use reflexion on retrieval quality for optimization.

---

## K. Model Training Concepts

This section covers techniques to customize and optimize LLMs, from parameter-efficient methods to architectural innovations. Presented in ascending efficiency: full methods first, then PEFT, distillation, and advanced structures.

### Fine-Tuning
**Short Summary:** Fine-tuning refines pre-trained models on task-specific data, unlocking domain expertise while preserving base capabilities.

1. **What is it?**  
   Continued training on labeled data to adjust weights, aligning the model to new distributions or formats.

2. **What are the types?**  
   - **Full Fine-Tuning:** Updates all parameters.  
   - **Task-Specific:** Single domain.  
   - **Continued Pre-Training:** Unsupervised extension.

3. **When to use each type?**  
   - **Full:** Deep customization (e.g., medical QA); advantages: maximal adaptation; but VRAM-heavy.  
   - **Task-Specific:** Narrow apps; advantages: focused gains; chat fine-tuning.  
   - **Continued:** Data augmentation; advantages: broadens knowledge; RAG alternatives.  
   *Added Insight:* Start with PEFT variants to avoid catastrophic forgetting—essential for agent role specialization.

### LoRA (Low-Rank Adaptation)
**Short Summary:** LoRA injects trainable low-rank matrices into layers, enabling efficient fine-tuning with minimal parameters.

1. **What is it?**  
   Decomposes weight updates as low-rank factors (A, B), freezing the base model for ~0.1% trainable params.

2. **What are the types?**  
   - **Standard LoRA:** Forward pass only.  
   - **LoRA-FA (Full Attention):** Includes attention matrices.  
   - **DoRA:** Decomposes magnitude/direction.

3. **When to use each type?**  
   - **Standard:** General tasks; advantages: simple, fast; consumer hardware.  
   - **LoRA-FA:** Sequence models; advantages: attention-tuned; translation agents.  
   - **DoRA:** Better generalization; advantages: stable; advanced PEFT.  
   *Added Insight:* Ideal for multi-agent fine-tuning—train per role without full retrains.

### QLoRA (Quantized LoRA)
**Short Summary:** QLoRA combines LoRA with 4-bit quantization, slashing memory for fine-tuning large models on single GPUs.

1. **What is it?**  
   Quantizes base model to NF4/FP4, applies LoRA adapters, and uses double-quant for optimizer states.

2. **What are the types?**  
   - **4-Bit QLoRA:** Base quantization level.  
   - **Paged QLoRA:** Offloads to CPU.  
   - **Mixed-Precision:** Hybrid bits.

3. **When to use each type?**  
   - **4-Bit:** Standard efficiency; advantages: 70% memory save; Llama fine-tuning.  
   - **Paged:** VRAM overflow; advantages: seamless; large batches.  
   - **Mixed:** Balanced accuracy; advantages: tunable; production prototypes.  
   *Added Insight:* Democratizes agent training—quantize for edge deployment in memory-augmented patterns.

### Prompt Tuning
**Short Summary:** Optimizes continuous "soft" prompt vectors prepended to inputs, freezing the model for ultra-low-cost adaptation.

1. **What is it?**  
   Learns dense embeddings as task prefixes, akin to finding optimal words without touching weights.

2. **What are the types?**  
   - **Basic Prompt Tuning:** Global soft tokens.  
   - **AdaPrompt:** Adaptive per layer/input.  
   - **Multitask:** Shared across tasks.

3. **When to use each type?**  
   - **Basic:** Single tasks; advantages: <0.01% params; quick tests.  
   - **AdaPrompt:** Varied inputs; advantages: dynamic; few-shot agents.  
   - **Multitask:** Shared domains; advantages: transferable; workflow tuning.  
   *Added Insight:* Suits dynamic prompting in ReAct—tune for tool-calling phrases.

### Prefix Tuning
**Short Summary:** Prefix tuning learns input prefixes for each transformer layer, enabling deeper, layer-wise adaptation.

1. **What is it?**  
   Inserts trainable prefix keys/values into attention layers, guiding activations without full updates.

2. **What are the types?**  
   - **Shallow Prefix:** Early layers only.  
   - **Deep Prefix:** All layers.  
   - **Prompt-Prefix Hybrid:** Combines both.

3. **When to use each type?**  
   - **Shallow:** Surface tasks; advantages: efficient; classification.  
   - **Deep:** Generative; advantages: expressive; text completion agents.  
   - **Hybrid:** Versatile; advantages: balanced; multi-pattern support.  
   *Added Insight:* Enhances CoT agents—prefix for reasoning scaffolds.

### P-Tuning v2
**Short Summary:** P-Tuning v2 improves prompt tuning with continuous prompts at multiple positions (soft + hard tokens), boosting few-shot performance.

1. **What is it?**  
   Optimizes a mix of learnable embeddings and discrete tokens inserted throughout the input sequence.

2. **What are the types?**  
   - **v1 (Basic):** Single prompt span.  
   - **v2 (Multi-Pos):** Distributed insertions.  
   - **PPT (Prompt Pre-Training):** Pre-train prompts.

3. **When to use each type?**  
   - **v1:** Simple; advantages: baseline; zero/few-shot.  
   - **v2:** Complex parsing; advantages: 10-20% gains; structured outputs.  
   - **PPT:** Low-data; advantages: transferable; agent initialization.  
   *Added Insight:* For multilingual agents—tune prompts per language in hybrid setups.

### Knowledge Distillation
**Short Summary:** Distillation trains a compact "student" to mimic a larger "teacher" model's outputs, compressing knowledge for efficiency.

1. **What is it?**  
   Student learns from teacher's soft logits/probabilities, often with temperature-scaled KL divergence loss.

2. **What are the types?**  
   - **Offline:** Fixed teacher.  
   - **Online:** Co-training.  
   - **Task-Specific:** On labeled data only.

3. **When to use each type?**  
   - **Offline:** Deployment; advantages: stable; edge agents.  
   - **Online:** Evolving pairs; advantages: mutual improvement; continual learning.  
   - **Task-Specific:** Narrow; advantages: precise; toolformer distillation.  
   *Added Insight:* Distill RAG-aware teachers for lightweight retrieval agents.

### Quantization (INT8/4/NF4)
**Short Summary:** Quantization maps high-precision weights to lower bits (e.g., INT8=8-bit integers, NF4=4-bit normals), accelerating inference.

1. **What is it?**  
   Reduces numerical precision via scaling/clipping, with calibration to minimize accuracy drop.

2. **What are the types?**  
   - **INT8:** Symmetric integers.  
   - **INT4:** Ultra-low for weights.  
   - **NF4:** Normalized floats for activations.

3. **When to use each type?**  
   - **INT8:** Balanced speed/accuracy; advantages: 4x faster; server inference.  
   - **INT4:** Extreme compression; advantages: mobile; quantized LoRA.  
   - **NF4:** Sensitive models; advantages: low perplexity loss; GPTQ method.  
   *Added Insight:* Post-training for quick wins—vital for scaling multi-agent fleets.

### Mixture-of-Experts (MoE)
**Short Summary:** MoE scales models by routing inputs to specialized "expert" sub-networks, activating only a subset per token for efficiency.

1. **What is it?**  
   A router selects top-k experts per layer/token, combining their outputs sparsely.

2. **What are the types?**  
   - **Dense MoE:** All experts trained.  
   - **Sparse MoE:** Load-balanced routing.  
   - **Switch Transformers:** Hard top-1 routing.

3. **When to use each type?**  
   - **Dense:** General; advantages: flexible; base training.  
   - **Sparse:** Large-scale; advantages: 10x params at same compute; Mixtral models.  
   - **Switch:** Simple; advantages: fast routing; cost-optimized agents.  
   *Added Insight:* For multi-role agents—experts as "roles" routed by orchestrators.

---

## L. System Design Concepts

Focuses on production-ready architectures for LLM systems, from caching to governance. Organized ascending scale: local opts to enterprise-wide.

### Caching
**Short Summary:** Caching pre-stores computations to cut latency/costs, tailored to prompts, embeddings, semantics, or responses.

1. **What is it?**  
   Key-value stores with TTL for reusing results, keyed by hashes or vectors.

2. **What are the types?**  
   - **Prompt Cache:** KV pairs in transformers.  
   - **Embedding Cache:** Pre-computed vectors.  
   - **Semantic Cache:** Fuzzy query matching.  
   - **Response Cache:** Full outputs.

3. **When to use each type?**  
   - **Prompt:** Repeated prefixes (e.g., system roles); advantages: 50-90% speed-up; long-context agents.  
   - **Embedding:** Indexing; advantages: build-time; RAG pipelines.  
   - **Semantic:** Similar queries; advantages: 30% hit rate; chat apps.  
   - **Response:** Identical inputs; advantages: instant; FAQs.  
   *Added Insight:* Layered caching in workflows—semantic first, exact fallback.

### Scaling & Load Balancing
**Short Summary:** Scaling distributes workload; load balancing routes requests evenly for high availability.

1. **What is it?**  
   Horizontal replication with routers (e.g., round-robin, least-connections) across instances.

2. **What are the types?**  
   - **Horizontal Scaling:** Add nodes.  
   - **Vertical:** Beefier hardware.  
   - **Auto-Scaling:** Dynamic based on load.

3. **When to use each type?**  
   - **Horizontal:** Traffic spikes; advantages: resilient; cloud agents.  
   - **Vertical:** Compute-bound; advantages: simple; single-node prototypes.  
   - **Auto:** Variable; advantages: cost-efficient; production multi-agent.  
   *Added Insight:* Balance by token load—prioritize long-context requests.

### Vector DB Sharding
**Short Summary:** Sharding partitions vector indices across servers for parallel queries on massive datasets.

1. **What is it?**  
   Divides data by hash/range, with query routing to relevant shards.

2. **What are the types?**  
   - **Hash-Based:** Consistent hashing.  
   - **Range-Based:** Sorted partitions.  
   - **Replicated:** For fault tolerance.

3. **When to use each type?**  
   - **Hash:** Even distribution; advantages: scalable inserts; dynamic RAG.  
   - **Range:** Sequential data; advantages: efficient scans; time-series memory.  
   - **Replicated:** High-avail; advantages: redundancy; enterprise agents.  
   *Added Insight:* Shard by user for privacy in memory-augmented systems.

### Latency Optimization
**Short Summary:** Targets sub-second responses via async, batching, and hardware tweaks.

1. **What is it?**  
   Pipeline overlaps (e.g., prefetch embeddings) and opts like speculative decoding.

2. **What are the types?**  
   - **Prefetching:** Anticipate needs.  
   - **Batching:** Group requests.  
   - **Speculative:** Draft then verify.

3. **When to use each type?**  
   - **Prefetching:** Predictable flows; advantages: hides I/O; RAG chains.  
   - **Batching:** High-throughput; advantages: GPU utilization; inference servers.  
   - **Speculative:** Generative; advantages: 2x speed; interactive agents.  
   *Added Insight:* Monitor percentiles—aim <200ms for loop-based patterns like ReAct.

### Observability (Monitoring)
**Short Summary:** Tracks system health via metrics, logs, and traces for proactive debugging.

1. **What is it?**  
   Tools like Prometheus for metrics, Jaeger for traces, ELK for logs.

2. **What are the types?**  
   - **Metrics:** Quant (e.g., latency).  
   - **Logs:** Events.  
   - **Traces:** End-to-end flows.

3. **When to use each type?**  
   - **Metrics:** SLAs; advantages: alerting; scaling decisions.  
   - **Logs:** Debugging; advantages: searchable; error analysis.  
   - **Traces:** Distributed; advantages: bottlenecks; agent workflows.  
   *Added Insight:* Trace agent trajectories—spot reflexion failures.

### Rate Limiting
**Short Summary:** Caps API usage to prevent abuse and ensure fairness.

1. **What is it?**  
   Token buckets or leaky buckets enforcing quotas per user/IP.

2. **What are the types?**  
   - **Fixed Window:** Slot-based.  
   - **Sliding Window:** Continuous.  
   - **Adaptive:** Load-aware.

3. **When to use each type?**  
   - **Fixed:** Simple; advantages: easy audit; free tiers.  
   - **Sliding:** Granular; advantages: smoother; user-facing.  
   - **Adaptive:** Bursty; advantages: resilient; multi-tenant agents.  
   *Added Insight:* Per-pattern limits—e.g., throttle ToT branches.

### Guardrails & Safety
**Short Summary:** Enforces ethical bounds via filters and policies.

1. **What is it?**  
   Multi-layer checks for harm, bias, accuracy.

2. **What are the types?**  
   - **Rule-Based:** Keywords.  
   - **ML-Based:** Classifiers.  
   - **LLM-Based:** Prompted judgments.

3. **When to use each type?**  
   - **Rule:** Fast blocks; advantages: cheap; PII redaction.  
   - **ML:** Nuanced; advantages: scalable; toxicity detection.  
   - **LLM:** Contextual; advantages: explainable; guardrail agents.  
   *Added Insight:* Embed in orchestrators—safety as a worker role.

### Prompt Injection Protection
**Short Summary:** Defends against adversarial prompts exploiting LLMs.

1. **What is it?**  
   Sanitizes inputs with delimiters, parsers, or sandboxes.

2. **What are the types?**  
   - **Delimiters:** Tag isolation.  
   - **Parsing:** Structured validation.  
   - **Runtime:** Execution monitoring.

3. **When to use each type?**  
   - **Delimiters:** Basic; advantages: lightweight; chat UIs.  
   - **Parsing:** JSON/tools; advantages: strict; function calling.  
   - **Runtime:** Advanced; advantages: catches evasions; production.  
   *Added Insight:* Test with red-teaming—critical for autonomous patterns.

### Data Governance
**Short Summary:** Manages data lifecycle for compliance, quality, and ethics in AI pipelines.

1. **What is it?**  
   Policies for collection, storage, access, and auditing (e.g., GDPR alignment).

2. **What are the types?**  
   - **Lineage Tracking:** Data flows.  
   - **Quality Gates:** Validation.  
   - **Access Controls:** RBAC.

3. **When to use each type?**  
   - **Lineage:** Debugging; advantages: traceability; RAG sources.  
   - **Quality:** Ingestion; advantages: clean data; embedding fidelity.  
   - **Access:** Secure; advantages: compliant; multi-user agents.  
   *Added Insight:* Govern memory stores—audit episodic for privacy.

### Model Evaluation Pipelines
**Short Summary:** Automated suites to benchmark models on metrics like BLEU, ROUGE, or custom agent success rates.

1. **What is it?**  
   CI/CD-like flows for testing fine-tunes, A/B comparisons, and drift detection.

2. **What are the types?**  
   - **Offline Eval:** Static datasets.  
   - **Online A/B:** Live traffic.  
   - **Simulation:** Agent envs.

3. **When to use each type?**  
   - **Offline:** Pre-deploy; advantages: fast; hallucination scores.  
   - **Online:** Iterative; advantages: real feedback; user satisfaction.  
   - **Simulation:** Complex; advantages: safe testing; ReAct loops.  
   *Added Insight:* Include pattern-specific evals—e.g., branch coverage for ToT.