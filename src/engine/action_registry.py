from typing import Callable, Dict, List, Tuple

class ActionContext:
    """Passed to every action handler to give them access to the game state."""
    def __init__(self, game):
        self.game = game
        self.handled = False
        self.consume_turn = False

class ActionRegistry:
    def __init__(self):
        self.handlers: Dict[str, Callable[[ActionContext, List[str]], None]] = {}
        self.aliases: Dict[str, str] = {}
        
    def register(self, command: str, handler: Callable, aliases: List[str] = None):
        self.handlers[command] = handler
        if aliases:
            for alias in aliases:
                self.aliases[alias] = command
                
    def dispatch(self, game, input_string: str) -> bool:
        parts = input_string.strip().split()
        if not parts:
            return False
            
        raw_cmd, args = parts[0].lower(), parts[1:]
        
        # Resolve aliases like 'n' -> 'move north' or 'go' -> 'move'
        cmd = self.aliases.get(raw_cmd, raw_cmd)
        
        handler = self.handlers.get(cmd)
        if not handler:
            print("Unknown command. Try 'help'.")
            return False
            
        context = ActionContext(game)
        
        try:
            handler(context, args)
        except Exception as e:
            game.say(f"Error executing action: {e}")
            raise # Re-raise for testability and hard-failing in dev
            
        if context.consume_turn:
            game.tick()
            
        return True
