import sys
import argparse
import random
import os
from engine.game import GameEngine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--content", type=str, default="src/content")
    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
        
    engine = GameEngine(content_dir=args.content)
    engine.say("Welcome to the Whispering Wilds. Type 'help' for commands.")
    engine.look()
    
    while True:
        try:
            cmd = input("> ").strip()
            if not engine.process_input(cmd):
                break
        except EOFError:
            engine.say("Farewell.")
            break
        except KeyboardInterrupt:
            print("")
            engine.say("Farewell.")
            break

if __name__ == "__main__":
    main()
