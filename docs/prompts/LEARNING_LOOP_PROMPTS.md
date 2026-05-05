# Learning Loop Prompts

Use these prompts when you want another AI system or collaborator to understand the repository as a governed learning system.

## Learning Loop Architecture Prompt

You are reviewing this repository as a governed semantic system that may become a living learning system over time.

Explain whether the learning loop is explicit, implicit, or missing.

Focus on:
- how retrieval feedback works
- how proposal promotion works
- how evaluation and gold questions fit into system improvement
- the difference between feedback, inference, proposal, and promoted baseline
- why the system avoids unsafe self-modification
- how the canonical spine and validation model constrain learning
- whether the learning loop should be treated as cross-cutting architecture or as an explicit ninth layer

Your output should include:
1. current learning-loop posture
2. strongest existing learning-loop components
3. what is still missing
4. why governed learning is safer than autonomous self-rewriting
5. how this could become a living knowledge system without semantic drift

## Learning Loop Reuse Prompt

You are evaluating whether the learning-loop design in this repository could be reused elsewhere.

Explain:
- which parts are generic
- which parts depend on the repo's canonical spine and governance posture
- what would need to be adapted for another organization
- how to preserve safe promotion logic and validation alignment

## Learning Loop Improvement Prompt

You are proposing improvements to the repository's governed learning-loop model.

You must preserve:
- canonical spine first
- validation-aligned growth
- provenance visibility
- trust boundary separation
- reviewable promotion logic
- clear separation between feedback, inference, proposal, and baseline

You may suggest:
- new learning-loop metrics
- steward review queues
- signal classification patterns
- better learning-loop documentation
- safer AI-assisted proposal generation

You must not suggest:
- silent self-rewriting
- direct promotion from AI output to canonical baseline
- collapsing asserted, inferred, and quarantine material into one layer

## Questions To Ask About This System

- How does this system learn from retrieval failures or ambiguity?
- How are new signals turned into governed improvements?
- What is the difference between feedback, inference, proposal, and promoted baseline?
- How does the architecture avoid unsafe self-modification?
- How can this become a living knowledge system without semantic drift?
- Should the learning loop be described as a ninth layer or as a cross-cutting recursive pattern?
- How should the 8-layer DNA address model interact with learning and adaptation logic?
