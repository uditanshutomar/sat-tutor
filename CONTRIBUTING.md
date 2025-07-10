# Contributing to SAT Tutor

Thank you for your interest in contributing to the SAT Tutor project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Search existing issues** to see if your problem has already been reported
2. **Check the documentation** to see if your question is answered there
3. **Provide detailed information** including:
   - Operating system and version
   - Python version
   - GPU type and drivers (if relevant)
   - Complete error messages
   - Steps to reproduce the issue

### Suggesting Features

When suggesting new features:

1. **Describe the problem** you're trying to solve
2. **Explain why** this feature would be useful
3. **Provide examples** of how it would work
4. **Consider implementation** complexity and impact

### Code Contributions

#### Setting Up Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/sat-tutor.git
   cd sat-tutor
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

#### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** following the coding standards below
3. **Write tests** for new functionality
4. **Run tests** locally:
   ```bash
   pytest
   ```
5. **Check code quality**:
   ```bash
   black .
   flake8 .
   mypy .
   ```
6. **Commit your changes** with a descriptive message:
   ```bash
   git commit -m "Add feature: brief description"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request** on GitHub

## 📝 Coding Standards

### Python Code Style

- **Follow PEP 8** for code formatting
- **Use type hints** for function parameters and return values
- **Write docstrings** for all public functions and classes
- **Keep functions small** and focused on a single responsibility
- **Use meaningful variable names**

### Code Formatting

We use **Black** for code formatting. Run it before committing:

```bash
black .
```

### Linting

We use **flake8** for linting. Fix any issues before submitting:

```bash
flake8 .
```

### Type Checking

We use **mypy** for type checking:

```bash
mypy . --ignore-missing-imports
```

### Testing

- **Write unit tests** for new functionality
- **Maintain test coverage** above 80%
- **Use descriptive test names** that explain what is being tested
- **Test both success and failure cases**

Example test structure:

```python
def test_semantic_augmenter_initialization():
    """Test that SemanticAugmenter initializes correctly."""
    augmenter = SemanticAugmenter(use_groq=False, model_name="gpt2")
    assert augmenter.model_name == "gpt2"
    assert augmenter.use_groq == False
```

## 🏗️ Project Structure

```
sat-tutor/
├── sat_tutor.py              # Main application
├── knowledge_graph.py        # Knowledge graph management
├── semantic_augmenter.py     # AI model integration
├── graph_rag.py             # Graph-based RAG system
├── tests/                   # Test files
├── docs/                    # Documentation
├── examples/                # Example scripts
└── requirements.txt         # Dependencies
```

## 🔧 Development Tools

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
pip install pre-commit
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_semantic_augmenter.py

# Run with verbose output
pytest -v
```

### Building Documentation

```bash
# Install documentation dependencies
pip install sphinx sphinx-rtd-theme

# Build documentation
cd docs
make html
```

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH**
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Creating a Release

1. **Update version** in `setup.py` and `__init__.py`
2. **Update CHANGELOG.md** with new features and fixes
3. **Create a release branch**:
   ```bash
   git checkout -b release/v1.0.0
   ```
4. **Test thoroughly** on different platforms
5. **Create a Pull Request** for the release
6. **Tag the release** on GitHub after merging

## 📚 Documentation

### Writing Documentation

- **Keep documentation up to date** with code changes
- **Use clear, concise language**
- **Include code examples**
- **Add diagrams** for complex concepts
- **Document API changes** in the changelog

### Documentation Structure

```
docs/
├── api/              # API documentation
├── guides/           # User guides
├── tutorials/        # Step-by-step tutorials
└── development/      # Developer documentation
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**:
   - Operating system and version
   - Python version
   - GPU type and drivers
   - Installed packages (`pip freeze`)

2. **Error information**:
   - Complete error traceback
   - Steps to reproduce
   - Expected vs actual behavior

3. **Additional context**:
   - What you were trying to do
   - Any recent changes to your system
   - Related issues or discussions

## 💡 Feature Requests

When requesting features:

1. **Describe the use case** clearly
2. **Explain the benefits** to users
3. **Consider alternatives** that might already exist
4. **Think about implementation** complexity
5. **Provide examples** of similar features in other projects

## 🎯 Areas for Contribution

We welcome contributions in these areas:

- **Performance improvements** for GPU acceleration
- **New model integrations** (local and cloud)
- **Enhanced knowledge graph** functionality
- **Better error handling** and user feedback
- **Documentation improvements**
- **Test coverage** expansion
- **UI/UX improvements** (if applicable)

## 📞 Getting Help

If you need help contributing:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Join our discussions** on GitHub
4. **Ask questions** in issues or discussions

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

Thank you for contributing to SAT Tutor! 🎉 