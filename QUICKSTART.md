# 🚀 Quick Start Guide

Get Rise Together up and running in 5 minutes!

## ⚡ Super Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/risetogethercommunity/rise-together-web.git
cd rise-together-web

# 2. Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

🎉 **Done!** Open http://127.0.0.1:8000 in your browser!

---

## 📚 What's Next?

### Access Admin Panel
1. Go to http://127.0.0.1:8000/admin
2. Login with your superuser credentials
3. Start adding content (blogs, projects, activities)

### Add Sample Data
```bash
# Load fixtures (if available)
python manage.py loaddata sample_data.json
```

### Customize
- Edit templates in `templates/`
- Modify styles in `static/css/`
- Add features in respective apps

---

## 🎯 Common Tasks

### Create a New Blog Post
1. Login to admin panel
2. Navigate to "Blogs" → "Add Blog"
3. Fill in title, content, author
4. Save and view on homepage

### Add a Project
1. Admin panel → "Projects" → "Add Project"
2. Enter project details
3. Add technology tags
4. Save and showcase!

### Manage Users
1. Admin → "Users"
2. View, edit, or delete users
3. Assign permissions

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Use a different port
python manage.py runserver 8080
```

### Issue: Module not found
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

---

## 📖 Learn More

- [Full Documentation](README.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Deployment Guide](DEPLOYMENT.md)

---

**Happy Coding! 💻✨**
