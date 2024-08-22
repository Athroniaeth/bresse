# ROADMAP

## Core

Create `core-bressed` package who allow to use this chess engine with the following features:
- [ ] Add prediction move from not finished PGN (% next move)
  - [ ] Input ConfigRun
    - temperature
    - presence_penalty
    - frequency_penalty
    - max_tokens
    - top_p
    - top_k
    - n
    - stop
    - logit_bias
    - logprobs
      - return_prompt
...

  - [ ] Return ResultInference 
    - number request
    - inputs tokens
    - outputs tokens
    - avg outputs tokens
    - cost ($ default can choose)
    - number request for 1$ ($ default can choose)


  - [ ] Add configuration for PGN 
    - event_name
    - site
    - date
    - round
    - white_player
    - black_player
    - result
    - variant
    - time_control
    - ECO
    - opening
    - termination

- [ ] Allow to add annotation to PGN before prediction of move (any color, previous move, stockfish evaluation, comment, symbol)

## Classes
- [ ] ModelIdentifier: (abstract)...
  - [ ] Add OpenAIModel
  - [ ] Add MistralModel
  - [ ] Add LangChainModel (remote)
  

- [ ] Model: (abstract)
  - [ ] ModelCloud:
    - [ ] Add OpenAIModel
    - [ ] Add MistralModel
    - [ ] Add LangChainModel (remote)
    
  - [ ] ModelLocal:
    - [ ] Add TransformerModel (huggingface)
    - [ ] Add LangChainModel (local, can only do chatbot prediction)
  
- [ ] Add ConfigRun
- [ ] Add ConfigPGN