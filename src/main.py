import sys
import argparse
import random
import os
from engine.game import GameEngine

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    engine = GameEngine(content_dir=os.path.join(base_dir, "content"))
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
