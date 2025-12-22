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

# Executable name and main file
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

# Default: create executable
all: $(NAME)

# Create the executable
$(NAME): $(MAIN)
	@echo "$(CYAN)Creating executable '$(NAME)'...$(RESET)"
	@cp $(MAIN) $(NAME)
	@chmod +x $(NAME)
	@echo "$(GREEN)Executable '$(NAME)' created!$(RESET)"
	@echo "$(YELLOW)Run with: ./$(NAME)$(RESET)"

# Run the interactive REPL
run: $(NAME)
	@echo "$(GREEN)Starting Computorv2...$(RESET)"
	@./$(NAME)

# Run with a single expression
eval: $(NAME)
	@if [ -z "$(EXPR)" ]; then \
		echo "$(RED)Usage: make eval EXPR=\"2+3\"$(RESET)"; \
	else \
		./$(NAME) "$(EXPR)"; \
	fi

# Show help
help: $(NAME)
	@./$(NAME) --help

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

# Remove cache, executable, and history
fclean: clean
	@echo "$(YELLOW)Removing executable...$(RESET)"
	@rm -f $(NAME) 2>/dev/null || true
	@echo "$(YELLOW)Removing history file...$(RESET)"
	@rm -f ~/.computorv2_history 2>/dev/null || true
	@echo "$(GREEN)Full clean completed!$(RESET)"

# Rebuild (clean + build)
re: fclean all

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
demo: $(NAME)
	@echo "$(GREEN)=== Computorv2 Demo ===$(RESET)"
	@echo ""
	@echo "$(CYAN)Basic arithmetic:$(RESET)"
	@./$(NAME) "2 + 3 * 4"
	@./$(NAME) "2^10"
	@echo ""
	@echo "$(CYAN)Complex numbers:$(RESET)"
	@./$(NAME) "i^2"
	@./$(NAME) "(3 + 2*i)^2"
	@echo ""
	@echo "$(CYAN)Built-in functions:$(RESET)"
	@./$(NAME) "sqrt(16)"
	@./$(NAME) "sqrt(-4)"
	@./$(NAME) "abs(3 + 4*i)"
	@echo ""
	@echo "$(CYAN)Matrix operations:$(RESET)"
	@./$(NAME) "det([[1,2];[3,4]])"
	@echo ""
	@echo "$(GREEN)Run './$(NAME)' for interactive mode$(RESET)"

# Install to /usr/local/bin (requires sudo)
install: $(NAME)
	@echo "$(CYAN)Installing $(NAME) to /usr/local/bin...$(RESET)"
	@sudo cp $(NAME) /usr/local/bin/$(NAME)
	@sudo chmod +x /usr/local/bin/$(NAME)
	@echo "$(GREEN)Installed! Run '$(NAME)' from anywhere.$(RESET)"

# Uninstall from /usr/local/bin
uninstall:
	@echo "$(YELLOW)Uninstalling $(NAME)...$(RESET)"
	@sudo rm -f /usr/local/bin/$(NAME)
	@echo "$(GREEN)Uninstalled!$(RESET)"

# **************************************************************************** #
#                              PHONY TARGETS                                   #
# **************************************************************************** #

.PHONY: all run eval help test test-basic test-complex test-matrix test-functions \
        test-equations test-builtins clean fclean re check count modules structure \
        demo install uninstall