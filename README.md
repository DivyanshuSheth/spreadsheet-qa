# spreadsheet-qa
Question Answering over Spreadsheets

# Literature Review

## Spreadsheet QA
Connected papers graph built from paper #1:
https://www.connectedpapers.com/main/dea212a431e6cae3a3e66657d6cbbd3b7c55925f/Multimodal-Table-Understanding/graph

1. Multimodal Table Understanding | Table-LLaVA model, MMTab dataset: https://arxiv.org/pdf/2406.08100 (Blog: https://www.aimodels.fyi/papers/arxiv/multimodal-table-understanding)
2. LLM, MLLM evaluation over tables + prompting techniques: https://arxiv.org/pdf/2402.12424
3. SheetAgent -- Planner, Informer, & Retriever + SheetRM benchmark: https://arxiv.org/pdf/2403.03636
4. Image-of-thought prompting for improved visual reasoning: https://arxiv.org/pdf/2405.13872
5. TextCoT -- Zoom in for improved multimodal reasoning: https://arxiv.org/pdf/2404.09797
6. Vision language models for spreadsheet understanding: https://arxiv.org/pdf/2405.16234
7. Multimodal reasoning with multimodal knowledge graphs: https://aclanthology.org/2024.acl-long.579.pdf

## Context Retrieval
1. Inter-chunk interactions for enhanced retrieval: https://arxiv.org/pdf/2408.02907v1

## Prompting
1. ExpertPrompting: https://arxiv.org/pdf/2305.14688
2. (from #2 in Spreadsheet QA above): https://arxiv.org/pdf/2402.12424
    - ExpertPrompting helps
    - CoT prompting helps
    - Row-coloring tables helps for some models, doesn't for others
    - Highlighting relevant cells helps
3. 

## Sheet Copilot
https://github.com/BraveGroup/SheetCopilot -- can be called upon (similar to function calling) in the process of producing an answer to a query, for a subtask

## Ideas
1. Zoom into stuff in spreadsheet image (like a pie chart image, for example), and then answer questions based on that (based on the paper https://arxiv.org/pdf/2404.09797)
2. Something like ViperGPT (https://viper.cs.columbia.edu/) for code generation and execution -- similar to planner from paper #3 above
3. Options to provide when prompting LLM: 1 - answer present, confident. 2 - incomplete context. 3 - irrelevant context.
    - to combine: 
4. Long-term goal: use image-of-thought rationales from Table-Llava but use reinforcement learning for the rationales (from AI feedback, like what they did for the o1 model)


## Final solution
1. Use Model from paper #1 (Table-LLaVA)
2. Use prompting techniques from paper #2
3. Use agents to plan, inform, and retrieve (if possible). Or maybe a code generation engine only, called when needed
4. Use image-of-thought prompting
