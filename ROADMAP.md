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


  - [ ] Add configuration for edit in inference PGN 
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
  - [ ] Add LangChainModel (HuggingFaceHub remote, need to be dynamic)
  

- [ ] Model: (abstract)
  - [ ] ModelCloud:
    - [ ] Add OpenAIModel
    - [ ] Add MistralModel
    - [ ] Add LangChainModel (HuggingFaceHub remote)
    
  - [ ] ModelLocal:
    - [ ] Add TransformerModel (huggingface)
    - [ ] Add LangChainModel (local, can only do chatbot prediction)
  
- [ ] Add ConfigRun
- [ ] Add ConfigPGN

- [ ] Add `find_model` for return the good Model class (OpenAI, Mistral) (browse static models like OpenAI, Mistral, try local, else load LangChain remote)
- [ ] Change repr of Output and CounterResult for set property attributes
- [ ] Merge Output and CounterResult

- [ ] Add 'postprocess' system for edit annotation of PGN or add variation before inference
  - [ ] Retry inference with different PGN metadata, add to Counter for 'most_common' move
  - [ ] Add annotation symbol to PGN before inference (for white, black, all moves, X previous move)
  - [ ] Add annotation comment to PGN before inference (for white, black, all moves, X previous move)