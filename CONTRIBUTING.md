# Contributing to Nexa Search

First off, thank you for considering contributing to Nexa Search! 🎉

It's people like you that make Nexa Search such a great tool. We welcome contributions from everyone, whether you're fixing a typo or implementing a major feature.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Testing](#testing)

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

---

## 🤝 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**Great bug reports include:**
- Clear, descriptive title
- Exact steps to reproduce the problem
- Expected behavior vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, browser)
- Error messages or logs

**Example:**
```markdown
**Bug:** Search fails with KeyError on specific queries

**Steps to Reproduce:**
1. Enter query: "quantum computing papers 2024"
2. Press Enter
3. Error appears

**Expected:** Results displayed
**Actual:** KeyError: 'output'

**Environment:**
- OS: macOS 14.2
- Python: 3.11.5
- Browser: Chrome 120

**Error Log:**
[Paste error here]
```

### 💡 Suggesting Features

We love feature ideas! Before suggesting, check if it's already been proposed.

**Great feature requests include:**
- Clear use case (why is this needed?)
- Expected behavior (what should it do?)
- Mockups or examples (if applicable)
- Willingness to help implement

**Example:**
```markdown
**Feature:** Add Google Scholar search tool

**Use Case:** 
Researchers need access to peer-reviewed papers beyond arXiv

**Proposed Implementation:**
- Add GoogleScholarTool to agent_engine.py
- Use serpapi or scholarly library
- Display citation counts in results

**I can help with:**
- [ ] Research implementation approach
- [x] Testing
- [ ] Documentation
```

### 📝 Improving Documentation

Documentation improvements are always welcome!

**Examples:**
- Fix typos or unclear explanations
- Add examples or tutorials
- Translate to other languages
- Create video guides

### 🔧 Code Contributions

See [Development Setup](#development-setup) below.

---

## 💻 Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/nexa-search.git
cd nexa-search
```

### 2. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install in editable mode
pip install -e .

# Install dev dependencies
pip install -r requirements.txt
pip install black flake8 pytest  # Optional: for code quality
```

### 4. Set Up Environment

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 5. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 6. Make Your Changes

Edit files, add features, fix bugs...

### 7. Test Locally

```bash
streamlit run app.py
# Test your changes thoroughly
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated (README, docstrings, etc.)
- [ ] No console.log or debug print statements left
- [ ] Tested locally and works as expected
- [ ] No merge conflicts with main branch

### Submitting

1. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

2. **Open Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   How was this tested?
   
   ## Screenshots (if applicable)
   [Add screenshots]
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-reviewed code
   - [ ] Commented complex code
   - [ ] Updated documentation
   - [ ] No new warnings
   - [ ] Tested locally
   ```

### Review Process

- Maintainers will review within 1-7 days
- Address feedback in new commits
- Once approved, we'll merge!

---

## 🎨 Coding Standards

### Python Style

We follow **PEP 8** with some flexibility.

**Use Black for formatting (recommended):**
```bash
pip install black
black app.py agent_engine.py
```

**Key Points:**
- 4 spaces for indentation (no tabs)
- Max line length: 88 characters (Black default)
- Use descriptive variable names
- Add docstrings for functions
- Type hints encouraged

**Example:**
```python
def search_query(query: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Execute a search query using the agent.
    
    Args:
        query: User's search query
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary containing answer and sources
        
    Raises:
        ValueError: If query is empty
    """
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Implementation here
    return result
```

### JavaScript/CSS

- Use 2 spaces for indentation
- Semicolons required
- Single quotes for strings
- ES6+ features welcome

### Documentation

- Use Markdown for all docs
- Keep lines under 80 characters
- Use proper heading hierarchy
- Include code examples
- Link to related docs

---

## 📝 Commit Guidelines

### Format

```
type(scope): subject

body (optional)

footer (optional)
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

**Good Commits:**
```
feat(search): add Google Scholar integration

- Added GoogleScholarTool to agent_engine
- Updated UI to show Scholar results
- Added configuration in .env.example

Closes #123
```

```
fix(ui): resolve mobile layout overflow

Fixed horizontal scroll issue on mobile devices
by adjusting search box padding and max-width.

Fixes #456
```

**Bad Commits:**
```
Update stuff
Fixed bug
WIP
asdfasdf
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor" not "Moves cursor")
- Start with lowercase (after type)
- Don't end with period
- Keep subject under 50 characters
- Wrap body at 72 characters

---

## 🧪 Testing

### Manual Testing

Test all changes manually before submitting:

```bash
# Run the app
streamlit run app.py

# Test different queries
# Test error cases
# Test edge cases
# Test on mobile (browser dev tools)
```

### Future: Automated Tests

We plan to add pytest tests. Help us get there!

**Example test structure:**
```python
# tests/test_agent.py
def test_search_returns_result():
    result = run_search("test query")
    assert result['success'] == True
    assert 'answer' in result
    assert len(result['sources']) > 0
```

---

## 📂 Project Structure

```
nexa-search/
├── app.py                 # Main Streamlit app (UI)
├── agent_engine.py        # LangChain agent logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── README.md             # Main documentation
├── CONTRIBUTING.md       # This file
├── CHANGELOG.md          # Version history
└── docs/                 # Additional docs
    ├── SETUP.md
    ├── DEPLOYMENT.md
    └── COMPARISON.md
```

### Where to Make Changes

- **UI changes:** `app.py` (CSS in load_css function)
- **Search logic:** `agent_engine.py`
- **New tools:** `agent_engine.py` (_initialize_tools method)
- **Documentation:** Respective .md files
- **Dependencies:** `requirements.txt`

---

## 🎯 Good First Issues

Looking for something to work on? Check issues labeled `good first issue`:

**Examples:**
- Add dark/light theme toggle
- Improve error messages
- Add keyboard shortcuts
- Create video tutorial
- Translate README to other languages
- Add more example queries
- Improve mobile CSS

---

## 💬 Communication

- **Questions?** Open a [Discussion](https://github.com/yourusername/nexa-search/discussions)
- **Found a bug?** Open an [Issue](https://github.com/yourusername/nexa-search/issues)
- **Have an idea?** Start a [Discussion](https://github.com/yourusername/nexa-search/discussions)
- **Want to chat?** Comment on existing issues/PRs

---

## 🙏 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in CHANGELOG.md

Major contributors may become maintainers!

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## ❓ Questions?

Don't hesitate to ask! We're here to help.

- **GitHub Discussions:** General questions
- **GitHub Issues:** Bug reports
- **Pull Requests:** Code reviews

**Remember:** There are no dumb questions. We were all beginners once!

---

## 🎉 Thank You!

Your contributions make Nexa Search better for everyone.

**Happy coding! 🚀**
