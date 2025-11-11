#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Main function
main() {
    print_info "🚀 Starting biteRide with uv..."
    
    # Check if uv is installed
    if ! command_exists uv; then
        print_error "uv is not installed. Please install uv first:"
        echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        print_warning "Virtual environment not found. Creating..."
        uv venv
        
        if [ $? -ne 0 ]; then
            print_error "Failed to create virtual environment"
            exit 1
        fi
        
        print_info "Installing dependencies..."
        source .venv/bin/activate
        uv pip install -e .
        
        if [ $? -ne 0 ]; then
            print_error "Failed to install dependencies"
            exit 1
        fi
        
        print_success "Virtual environment created and dependencies installed"
    else
        print_info "Activating existing virtual environment..."
        source .venv/bin/activate
    fi
    
    # Check if app directory exists
    if [ ! -d "app" ]; then
        print_error "app directory not found. Are you in the correct directory?"
        exit 1
    fi
    
    # Start FastAPI using Uvicorn
    print_success "Starting FastAPI app..."
    print_info "📱 API will be available at: http://localhost:8000"
    print_info "📚 Documentation at: http://localhost:8000/docs"
    echo
    
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Run main function
main "$@"