# ROADMAP

## Core

Create `core-bresse` package who allow to use this chess engine with the following features:

- [ ] Allow to add annotation to PGN before prediction of move (any color, previous move, stockfish evaluation, comment, symbol) 

- [X] Model: (abstract)
  - [X] ModelCloud:
    - [ ] Add LangChainModel (HuggingFaceHub remote)
    
  - [ ] ModelLocal:
    - [ ] Add TransformerModel (huggingface)
    - [ ] Add LangChainModel (local, can only do chatbot prediction)

- [ ] Add 'postprocess' system for edit annotation of PGN or add variation before inference
  - [ ] Retry inference with different PGN metadata, add to Counter for 'most_common' move
  - [ ] Add annotation symbol to PGN before inference (for white, black, all moves, X previous move)
  - [ ] Add annotation comment to PGN before inference (for white, black, all moves, X previous move)

- [ ] Replace all 'reference' variable by 'value' variable for all functions (create functions if python-chess don't have)