#!/usr/bin/env python3
"""
Computorv2 - Advanced Mathematical Interpreter

A command-line calculator supporting:
- Rational and complex numbers
- Matrices
- Polynomial functions
- Equation solving (degree 0, 1, 2)
- Built-in math functions (sin, cos, sqrt, etc.)

Usage:
    python main.py           # Interactive REPL
    python main.py "2+3"     # Evaluate single expression
    python main.py -h        # Show help

42 School Project
"""

import sys
import signal

try:
    import readline  # Enable arrow keys and history in input
except ImportError:
    pass  # readline not available on all platforms

from src.lexer import LexerError
from src.parser import parse, ParserError
from src.evaluator import Evaluator, Context, EvaluatorError
from src.simplifier import simplify_equation
from src.solver import solve, format_solution, SolverError
from src.formatter import format_value


def signal_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) and SIGQUIT (Ctrl+backslash) for clean exit."""
    print("\nGoodbye!")
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGQUIT, signal_handler)  # Ctrl+\


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


def colorize(text: str, color: str) -> str:
    """Apply color to text if terminal supports it."""
    if sys.stdout.isatty():
        return f"{color}{text}{Colors.RESET}"
    return text


class Computor:
    """
    Main Computorv2 interpreter class.
    
    Manages the REPL loop and command processing.
    """
    
    def __init__(self):
        self.context = Context()
        self.evaluator = Evaluator(self.context)
        self.running = True
        self.history = []
    
    def run(self):
        """Run the interactive REPL."""
        self.print_banner()
        
        while self.running:
            try:
                line = input(colorize("> ", Colors.GREEN)).strip()
                
                if not line:
                    continue
                
                self.history.append(line)
                self.process(line)
                
            except EOFError:
                # Ctrl+D
                print("\nGoodbye!")
                self.running = False
    
    def process(self, line: str):
        """Process a single input line."""
        # Handle commands (start with !)
        if line.startswith('!'):
            self.handle_command(line[1:].strip())
            return
        
        try:
            ast = parse(line)
            result = self.evaluator.evaluate(ast)
            
            if result.is_equation:
                self.handle_equation(result)
            else:
                self.handle_value(result)
        
        except LexerError as e:
            self.print_error(f"Lexer error: {e}")
        except ParserError as e:
            self.print_error(f"Syntax error: {e}")
        except EvaluatorError as e:
            self.print_error(f"Evaluation error: {e}")
        except SolverError as e:
            self.print_error(f"Solver error: {e}")
        except Exception as e:
            self.print_error(f"Error: {e}")
    
    def handle_value(self, result):
        """Handle a computed value result."""
        if result.value is not None:
            formatted = format_value(result.value)
            print(colorize(f"  = {formatted}", Colors.CYAN))
    
    def handle_equation(self, result):
        """Handle an equation to solve."""
        left, right = result.equation_data
        
        try:
            equation = simplify_equation(left, right)
            solution = solve(equation)
            print(colorize(format_solution(solution), Colors.CYAN))
        except SolverError as e:
            self.print_error(f"Cannot solve: {e}")
    
    def handle_command(self, cmd: str):
        """Handle built-in commands (prefixed with !)."""
        parts = cmd.split()
        if not parts:
            return
        
        command = parts[0].lower()
        args = parts[1:]
        
        if command in ('quit', 'exit', 'q'):
            self.running = False
            print("Goodbye!")
        
        elif command in ('help', 'h', '?'):
            self.print_help()
        
        elif command in ('vars', 'variables'):
            self.list_variables()
        
        elif command in ('funcs', 'functions'):
            self.list_functions()
        
        elif command in ('builtins', 'builtin'):
            self.list_builtins()
        
        elif command == 'clear':
            self.context.clear()
            print("Context cleared.")
        
        elif command == 'history':
            self.show_history()
        
        elif command in ('del', 'delete'):
            if args:
                self.delete_item(args[0])
            else:
                print("Usage: !del <name>")
        
        else:
            self.print_error(f"Unknown command: {command}")
            print("Type !help for available commands.")
    
    def list_variables(self):
        """List all defined variables."""
        variables = self.context.list_variables()
        if not variables:
            print("No variables defined.")
            return
        
        print(colorize("Variables:", Colors.BOLD))
        for name, value in variables:
            print(f"  {name} = {format_value(value)}")
    
    def list_functions(self):
        """List all defined functions."""
        functions = self.context.list_functions()
        if not functions:
            print("No functions defined.")
            return
        
        print(colorize("Functions:", Colors.BOLD))
        for name, func in functions:
            print(f"  {func}")
    
    def list_builtins(self):
        """List all built-in functions."""
        from src.evaluator.builtins import BUILTIN_FUNCTIONS
        
        print(colorize("Built-in Functions:", Colors.BOLD))
        for name, func in BUILTIN_FUNCTIONS.items():
            print(f"  {name}(x)  - {func.description}")
    
    def delete_item(self, name: str):
        """Delete a variable or function."""
        name_lower = name.lower()
        if self.context.has_variable(name_lower):
            self.context.delete_variable(name_lower)
            print(f"Deleted variable: {name}")
        elif self.context.has_function(name_lower):
            self.context.delete_function(name_lower)
            print(f"Deleted function: {name}")
        else:
            self.print_error(f"'{name}' not found")
    
    def show_history(self):
        """Show command history."""
        if not self.history:
            print("No history.")
            return
        
        print(colorize("History:", Colors.BOLD))
        for i, cmd in enumerate(self.history[-20:], 1):
            print(f"  {i}. {cmd}")
    
    def print_error(self, message: str):
        """Print an error message."""
        print(colorize(f"Error: {message}", Colors.RED))
    
    def print_banner(self):
        """Print welcome banner."""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                      COMPUTORV2                           ║
║              Advanced Mathematical Interpreter            ║
╠═══════════════════════════════════════════════════════════╣
║  Supports: Rationals, Complex, Matrices, Polynomials      ║
║  Type !help for commands, !quit to exit                   ║
╚═══════════════════════════════════════════════════════════╝
"""
        print(colorize(banner, Colors.MAGENTA))
    
    def print_help(self):
        """Print help message."""
        help_text = """
COMPUTORV2 HELP
===============

EXPRESSIONS:
  42                    Number literal
  3.14                  Decimal number
  2 + 3 * 4             Arithmetic (+ - * / % ^)
  2^10                  Power
  i                     Imaginary unit
  3 + 2*i               Complex number
  [[1,2];[3,4]]         Matrix (2x2)
  A ** B                Matrix multiplication

BUILT-IN FUNCTIONS:
  sqrt(x)               Square root (works with negative numbers)
  abs(x)                Absolute value / modulus for complex
  sin(x), cos(x), tan(x)   Trigonometric functions
  exp(x)                Exponential (e^x)
  log(x), ln(x)         Natural logarithm

MATRIX FUNCTIONS:
  det(M)                Determinant of matrix
  inv(M)                Inverse of matrix
  transpose(M)          Transpose of matrix

ASSIGNMENTS:
  x = 5                 Assign variable
  f(x) = x^2 + 1        Define function
  A = [[1,2];[3,4]]     Assign matrix

QUERIES:
  x = ?                 Show variable value
  f(2) = ?              Evaluate function
  2 + 3 = ?             Evaluate expression

EQUATIONS (solve):
  x + 2 = 0 ?           Linear equation
  x^2 - 4 = 0 ?         Quadratic equation
  f(x) = 0 ?            Solve function = 0

COMMANDS:
  !help                 Show this help
  !vars                 List variables
  !funcs                List functions
  !builtins             List built-in functions
  !del <name>           Delete variable/function
  !clear                Clear all definitions
  !history              Show command history
  !quit                 Exit program

EXAMPLES:
  > sqrt(16)
  > abs(-5 + 3*i)
  > sin(3.14159)
  > f(x) = x^2 - 5*x + 6
  > f(x) = 0 ?
"""
        print(help_text)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ('-h', '--help'):
            print(__doc__)
            print("Commands: Type !help in the REPL for detailed help.")
            sys.exit(0)
        elif arg in ('-v', '--version'):
            print("Computorv2 v1.0 - 42 School Project")
            sys.exit(0)
        else:
            # Evaluate single expression
            computor = Computor()
            computor.process(arg)
            sys.exit(0)
    
    # Start interactive REPL
    computor = Computor()
    computor.run()


if __name__ == '__main__':
    main()