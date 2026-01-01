# Contributing to LinkedIn Profile Optimization Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

We welcome feature suggestions! Please open an issue describing:
- The enhancement you'd like to see
- Why it would be valuable
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and single-purpose
- Write clear, descriptive variable names

### Testing

Before submitting a PR:
- Ensure the app runs without errors
- Test all modified functionality
- Verify the UI looks good on different screen sizes
- Check that API calls work as expected

## Development Setup

```bash
# Clone the repo
git clone https://github.com/stackconsult/LinkedIn-Profile-Optimization-Agent-.git
cd LinkedIn-Profile-Optimization-Agent-

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OpenAI API key to .env

# Run the app
streamlit run app.py
```

## Areas We'd Love Help With

- Adding support for more profile sections (Skills, Experience, etc.)
- Implementing profile completeness scoring
- Adding multi-language support
- Improving the UI/UX
- Writing tests
- Documentation improvements
- Performance optimizations

## Questions?

Feel free to open an issue for any questions about contributing!

## Code of Conduct

Please be respectful and constructive in all interactions. We're here to build something great together!
