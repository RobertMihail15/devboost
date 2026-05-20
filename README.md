# ⚡ DevBoost – Freelance IT Career Platform

O platformă de digital marketing pentru freelanceri IT, cu landing page modern, lead generation, blog, social media campaigns și analytics dashboard.

## 🚀 Setup rapid (3 pași)

```bash
# 1. Instalează dependențele și configurează baza de date
bash setup.sh

# 2. Pornește serverul
python manage.py runserver

# 3. Deschide în browser
# http://127.0.0.1:8000
```

## 📄 Pagini disponibile

| URL | Descriere |
|-----|-----------|
| `/` | Home / Landing Page |
| `/signup/` | Formular de signup (Lead Capture) |
| `/freelancers/` | Lista freelanceri cu filtrare |
| `/blog/` | Blog cu articole content marketing |
| `/campaigns/` | Social Media Campaign Posts |
| `/admin-view/` | Dashboard cu leads & analytics |
| `/api/freelancers/` | JSON API – lista freelanceri |
| `/api/leads/` | JSON API – lista leads |
| `/admin/` | Django Admin Panel |

## 🏗️ Structura proiectului

```
devboost/
├── devboost/          # Configurare Django
│   ├── settings.py
│   └── urls.py
├── core/              # Aplicația principală
│   ├── models.py      # Freelancer + Lead models
│   ├── views.py       # Toate view-urile
│   ├── urls.py        # URL routing
│   ├── templates/     # HTML templates
│   └── static/        # CSS
├── seed.py            # Date de test
├── requirements.txt
└── setup.sh
```

## 📢 Componente Digital Marketing incluse

- **SEO**: Title tags, meta descriptions, keywords pe toate paginile
- **Lead Generation**: Formular signup care salvează în DB
- **Content Marketing**: Blog cu 4 articole despre freelancing
- **Social Media**: Pagina Campaigns cu 3 postări simulate (LinkedIn, Twitter, Instagram)
- **Email Marketing**: Mesaj de confirmare după signup
- **Analytics**: Dashboard cu număr total leads și freelanceri
- **Marketing Funnel**: Visitor → Signup → Lead
