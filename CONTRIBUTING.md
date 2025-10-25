# Contributing to Rise Together

First off, thank you for considering contributing to Rise Together! It's people like you that make Rise Together such a great community platform.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to contact@risetogether.tech.

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details** (OS, browser, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **Include mockups or examples if applicable**

### Your First Code Contribution

Unsure where to begin? You can start by looking through these issues:

- **Good First Issue** - issues that are good for newcomers
- **Help Wanted** - issues that need assistance

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the style guidelines
5. Issue that pull request!

## 💻 Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/rise-together-web.git
   cd rise-together-web
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🔄 Pull Request Process

1. **Update the README.md** with details of changes if applicable
2. **Update the documentation** with any new features
3. **Follow the coding standards** outlined below
4. **Ensure all tests pass** before submitting
5. **Update the CHANGELOG.md** if applicable
6. **Reference any related issues** in the PR description
7. **Wait for review** from maintainers

### PR Title Format

Use conventional commit format:
- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `style: Format code`
- `refactor: Refactor component`
- `test: Add tests`
- `chore: Update dependencies`

## 📝 Style Guidelines

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Maximum line length: 88 characters (Black formatter)

Example:
```python
def calculate_reading_time(content: str) -> int:
    """
    Calculate the estimated reading time for content.
    
    Args:
        content (str): The text content to analyze
        
    Returns:
        int: Estimated reading time in minutes
    """
    words = len(content.split())
    return max(1, words // 200)
```

### Django Best Practices

- Use class-based views where appropriate
- Keep views thin, models fat
- Use Django's built-in features (forms, auth, etc.)
- Follow Django naming conventions
- Use Django's ORM efficiently

### HTML/CSS Guidelines

- Use semantic HTML5 elements
- Follow TailwindCSS utility classes
- Keep custom CSS minimal
- Ensure responsive design
- Use meaningful class names

### JavaScript Guidelines

- Use ES6+ features
- Write clear, commented code
- Avoid jQuery (use vanilla JS)
- Keep functions pure when possible
- Handle errors gracefully

### Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
feat: Add user notification system

- Implement real-time notifications
- Add notification preferences
- Create notification model and views

Closes #123
```

## 🧪 Testing

Always add tests for new features:

```python
from django.test import TestCase
from .models import Blog

class BlogTestCase(TestCase):
    def setUp(self):
        Blog.objects.create(title="Test Blog", content="Test content")
    
    def test_blog_creation(self):
        blog = Blog.objects.get(title="Test Blog")
        self.assertEqual(blog.content, "Test content")
```

Run tests with:
```bash
python manage.py test
```

## 📚 Documentation

- Update documentation for any changed functionality
- Add docstrings to new functions and classes
- Update README.md if adding new features
- Add comments for complex logic

## 🌟 Recognition

Contributors will be recognized in:
- README.md acknowledgments section
- Our website's contributors page
- Release notes

## 💬 Community

Join our community channels:

- **Discord**: [Join our server](https://discord.gg/risetogether)
- **Twitter**: [@risetogether](https://twitter.com/risetogether)
- **Email**: contact@risetogether.tech

## ❓ Questions?

Feel free to reach out if you have any questions. We're here to help!

---

**Thank you for contributing to Rise Together! 🚀**
