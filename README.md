# Rise Together Web
<p class="center">
<img width="300" height="300" alt="riselogo" src="https://github.com/user-attachments/assets/7a65749a-7821-4594-bd87-f4de8da71426" />
</p>
Rise Together is a tech learning community where we grow through collaboration. With tracks in frontend, backend (Django), and AI/ML,  Learn, build, and rise—together. 🌱💻✨

## Features

## Installation & Setup

---

### Prerequisites

- Python 3.11  
- Git  
- Virtual Environment (venv)  
- Django (installed via pip)  

---

### Steps to Run the Project

#### 1. Clone the Repository

```bash
https://github.com/risetogethercommunity/rise-together-web.git
cd [project]
```

#### 2. Set Up Virtual Environment

```bash
python -m venv venv
```

#### 2. Activate the Virtual Environment
- **Windows**
```bash
venv\Scripts\activate
```

- **Mac/Linux**
```bash
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Run the Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.
