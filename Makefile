# **************************************************************************** #
#                                                                              #
#    Makefile                                                                  #
#                                                                              #
#    Computorv2 - Advanced Mathematical Interpreter                            #
#    42 School Project                                                         #
#                                                                              #
# **************************************************************************** #

# Python interpreter
PYTHON		= python3

# Main entry point
NAME		= computorv2
MAIN		= main.py

# Source directories
SRC_DIR		= src
MODULES		= utils math_types lexer parser formatter evaluator simplifier solver

# Colors
GREEN		= \033[0;32m
YELLOW		= \033[0;33m
CYAN		= \033[0;36m
RED			= \033[0;31m
RESET		= \033[0m

# **************************************************************************** #
#                                 RULES                                        #
# **************************************************************************** #

# Default: run the interpreter
all: run

# Run the interactive REPL
run:
	@echo "$(GREEN)Starting Computorv2...$(RESET)"
	@$(PYTHON) $(MAIN)

# Run with a single expression
eval:
	@if [ -z "$(EXPR)" ]; then \
		echo "$(RED)Usage: make eval EXPR=\"2+3\"$(RESET)"; \
	else \
		$(PYTHON) $(MAIN) "$(EXPR)"; \
	fi

# Show help
help:
	@$(PYTHON) $(MAIN) --help

# **************************************************************************** #
#                                 TESTS                                        #
# **************************************************************************** #

# Run all tests
test: test-basic test-complex test-matrix test-functions test-equations test-builtins
	@echo "$(GREEN)All tests completed!$(RESET)"

# Basic arithmetic tests
test-basic:
	@echo "$(CYAN)=== Basic Arithmetic Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
tests = [('2 + 3', '5'), ('2 * 3 + 4', '10'), ('2^10', '1024'), ('17 % 5', '2'), ('10 / 4', '2.5')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr} = {exp}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# Complex number tests
test-complex:
	@echo "$(CYAN)=== Complex Number Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
tests = [('i^2', '-1'), ('i^4', '1'), ('(3+2*i) + (1+4*i)', '4 + 6i')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr} = {exp}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# Matrix tests
test-matrix:
	@echo "$(CYAN)=== Matrix Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
c.process('M = [[1,2];[3,4]]'); \
tests = [('det(M)', '-2'), ('det([[1,0];[0,1]])', '1')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr} = {exp}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# Function tests
test-functions:
	@echo "$(CYAN)=== Function Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
c.process('f(x) = x^2 + 1'); \
c.process('g(x) = 2*x'); \
tests = [('f(3) = ?', '10'), ('g(5) = ?', '10'), ('f(g(x)) = ?', '4 * x^2 + 1')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# Equation solving tests
test-equations:
	@echo "$(CYAN)=== Equation Solving Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
tests = [('2*x + 4 = 0 ?', 'x = -2'), ('x^2 - 4 = 0 ?', 'x = 2'), ('x^2 + 1 = 0 ?', 'i')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# Built-in functions tests
test-builtins:
	@echo "$(CYAN)=== Built-in Functions Tests ===$(RESET)"
	@$(PYTHON) -c "from main import Computor; import io; from contextlib import redirect_stdout; \
c = Computor(); c.running = False; \
tests = [('sqrt(16)', '4'), ('sqrt(-4)', '2i'), ('abs(-5)', '5'), ('sin(0)', '0'), ('cos(0)', '1'), ('exp(0)', '1'), ('log(1)', '0')]; \
passed = 0; \
exec('''for expr, exp in tests:\n    f = io.StringIO()\n    with redirect_stdout(f): c.process(expr)\n    out = f.getvalue().strip()\n    if exp in out:\n        print(f\"✓ {expr} = {exp}\")\n        passed += 1\n    else:\n        print(f\"✗ {expr} expected {exp}, got {out}\")'''); \
print(f'Passed: {passed}/{len(tests)}')"

# **************************************************************************** #
#                              CLEANING                                        #
# **************************************************************************** #

# Remove Python cache files
clean:
	@echo "$(YELLOW)Cleaning cache files...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "$(GREEN)Cache cleaned!$(RESET)"

# Remove cache and history
fclean: clean
	@echo "$(YELLOW)Removing history file...$(RESET)"
	@rm -f ~/.computorv2_history 2>/dev/null || true
	@echo "$(GREEN)Full clean completed!$(RESET)"

# Rebuild (clean + run)
re: fclean run

# **************************************************************************** #
#                              UTILITIES                                       #
# **************************************************************************** #

# Check Python version
check:
	@echo "$(CYAN)Checking environment...$(RESET)"
	@$(PYTHON) --version
	@echo "$(GREEN)Python OK$(RESET)"

# Count lines of code
count:
	@echo "$(CYAN)Lines of code:$(RESET)"
	@find . -name "*.py" -not -path "./__pycache__/*" | xargs wc -l | tail -1

# List all modules
modules:
	@echo "$(CYAN)Project modules:$(RESET)"
	@for mod in $(MODULES); do \
		echo "  - $(SRC_DIR)/$$mod"; \
	done

# Show project structure
structure:
	@echo "$(CYAN)Project structure:$(RESET)"
	@find . -type f -name "*.py" -not -path "./__pycache__/*" | sort | sed 's|^./||'

# Interactive demo
demo:
	@echo "$(GREEN)=== Computorv2 Demo ===$(RESET)"
	@echo ""
	@echo "$(CYAN)Basic arithmetic:$(RESET)"
	@$(PYTHON) $(MAIN) "2 + 3 * 4"
	@$(PYTHON) $(MAIN) "2^10"
	@echo ""
	@echo "$(CYAN)Complex numbers:$(RESET)"
	@$(PYTHON) $(MAIN) "i^2"
	@$(PYTHON) $(MAIN) "(3 + 2*i)^2"
	@echo ""
	@echo "$(CYAN)Built-in functions:$(RESET)"
	@$(PYTHON) $(MAIN) "sqrt(16)"
	@$(PYTHON) $(MAIN) "sqrt(-4)"
	@$(PYTHON) $(MAIN) "abs(3 + 4*i)"
	@echo ""
	@echo "$(CYAN)Matrix operations:$(RESET)"
	@$(PYTHON) $(MAIN) "det([[1,2];[3,4]])"
	@echo ""
	@echo "$(GREEN)Run 'make run' for interactive mode$(RESET)"

# **************************************************************************** #
#                              PHONY TARGETS                                   #
# **************************************************************************** #

.PHONY: all run eval help test test-basic test-complex test-matrix test-functions \
        test-equations test-builtins clean fclean re check count modules structure demo