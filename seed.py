import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devboost.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Freelancer, ClientProfile, Lead, BlogPost, Campaign

print("🧹 Curățare date vechi...")
Lead.objects.all().delete()
Freelancer.objects.all().delete()
ClientProfile.objects.all().delete()
User.objects.filter(is_staff=False).delete()

# ── Freelancers ──────────────────────────────────────────────────────
freelancers_data = [
    {"email": "alex@demo.com",    "first": "Alex",    "last": "Popescu",    "skill": "Frontend", "desc": "React & Vue specialist cu 5+ ani experiență în interfețe SaaS. Pasionat de cod curat și design pixel-perfect.", "exp": 5},
    {"email": "maria@demo.com",   "first": "Maria",   "last": "Ionescu",    "skill": "Backend",  "desc": "Expert Python & Django. A construit API-uri pentru fintech și e-commerce la scară. Obsedat de performanță.", "exp": 7},
    {"email": "radu@demo.com",    "first": "Radu",    "last": "Constantin", "skill": "Design",   "desc": "Designer UI/UX care unește designul cu codul. Figma power user, ochi puternic pentru branding.", "exp": 4},
    {"email": "elena@demo.com",   "first": "Elena",   "last": "Dumitrescu", "skill": "DevOps",   "desc": "Specialist AWS & Kubernetes. Automatizează tot, nu strică nimic. Pipeline-urile CI/CD sunt arta ei.", "exp": 6},
    {"email": "mihai@demo.com",   "first": "Mihai",   "last": "Georgescu",  "skill": "Frontend", "desc": "Developer TypeScript & Next.js. Construiește aplicații web rapide și accesibile. Contributor open source.", "exp": 3},
    {"email": "andreea@demo.com", "first": "Andreea", "last": "Stan",       "skill": "Backend",  "desc": "Expert Node.js & PostgreSQL. Arhitectură microservicii, REST și GraphQL APIs.", "exp": 5},
]
freelancer_objects = []
for f in freelancers_data:
    user = User.objects.create_user(username=f['email'], email=f['email'], password='demo123', first_name=f['first'], last_name=f['last'])
    fl = Freelancer.objects.create(user=user, full_name=f"{f['first']} {f['last']}", skill=f['skill'], description=f['desc'], experience_years=f['exp'])
    freelancer_objects.append(fl)
print(f"✅ {len(freelancers_data)} freelanceri creați (parola: demo123)")

# ── Clienți ──────────────────────────────────────────────────────────
clients_data = [
    {"email": "client1@demo.com", "first": "Bogdan", "last": "Munteanu", "company": "StartupX SRL", "industry": "Startup"},
    {"email": "client2@demo.com", "first": "Ioana",  "last": "Radu",     "company": "Acme Agency",  "industry": "Agenție"},
]
client_objects = []
for c in clients_data:
    user = User.objects.create_user(username=c['email'], email=c['email'], password='demo123', first_name=c['first'], last_name=c['last'])
    cp = ClientProfile.objects.create(user=user, full_name=f"{c['first']} {c['last']}", company=c['company'], industry=c['industry'])
    client_objects.append(cp)
print(f"✅ {len(clients_data)} clienți creați (parola: demo123)")

# ── Admin ────────────────────────────────────────────────────────────
if not User.objects.filter(username='admin@devboost.com').exists():
    User.objects.create_superuser(username='admin@devboost.com', email='admin@devboost.com', password='admin123', first_name='Admin', last_name='DevBoost')
    print("✅ Admin creat: admin@devboost.com / admin123")
else:
    print("ℹ️  Admin există deja")

# ── Leads demo ───────────────────────────────────────────────────────
if freelancer_objects and client_objects:
    Lead.objects.create(client=client_objects[0], freelancer=freelancer_objects[0], message="Salut Alex, am un proiect de e-commerce în React și aș vrea să discutăm. Buget estimat 3000 EUR, termen 2 luni.")
    Lead.objects.create(client=client_objects[0], freelancer=freelancer_objects[1], message="Bună Maria, am nevoie de un API REST în Django pentru o aplicație de gestiune internă. Suntem o echipă mică, startup SaaS.")
    Lead.objects.create(client=client_objects[1], freelancer=freelancer_objects[2], message="Radu, căutăm un designer pentru rebranding complet — logo, design system, Figma. Ești disponibil în iulie?")
    print("✅ 3 leads demo create")

# ── Blog & Campaigns ─────────────────────────────────────────────────
BlogPost.objects.all().delete()
blog_data = [
    {"title": "How to Get Your First Freelance Client", "excerpt": "Landing your first client is the hardest step. Here are proven strategies to break into the freelance market.", "body": "Start by building a strong portfolio with personal or open-source projects. Reach out to your existing network, join freelance platforms, and always ask satisfied clients for referrals.", "category": "Lead Generation"},
    {"title": "Why Personal Branding Matters for Developers", "excerpt": "In a crowded market, your personal brand is what sets you apart.", "body": "Personal branding is not just for marketers. Your GitHub profile, blog posts, conference talks all contribute to how clients perceive you.", "category": "Branding"},
    {"title": "SEO Tips for IT Freelancers", "excerpt": "Make sure clients can find you online with these SEO fundamentals.", "body": "Use relevant keywords in your LinkedIn headline, portfolio descriptions, and blog posts. Create a personal website with a clear niche.", "category": "SEO"},
    {"title": "Setting Your Freelance Rates Confidently", "excerpt": "Undercharging is one of the most common mistakes freelancers make.", "body": "Research market rates for your skill. Add a premium for your expertise and specialization. Never apologize for your rates.", "category": "Business"},
]
for b in blog_data: BlogPost.objects.create(**b)
print(f"✅ {len(blog_data)} articole blog create")

Campaign.objects.all().delete()
campaigns_data = [
    {"platform": "LinkedIn",    "text": "Join DevBoost and get clients faster 🚀 Over 500 freelancers have already built their digital presence with us.", "likes": 142, "comments": 23},
    {"platform": "Twitter / X", "text": "New freelancers joined DevBoost today 🎉 Frontend devs, backend wizards, UI/UX designers — all growing their careers. #FreelanceIT", "likes": 87, "comments": 11},
    {"platform": "Instagram",   "text": "Boost your IT career with DevBoost ⚡ We give freelancers the tools and clients they need to thrive.", "likes": 203, "comments": 34},
]
for c in campaigns_data: Campaign.objects.create(**c)
print(f"✅ {len(campaigns_data)} campanii create")

print("\n🚀 Seed complet! Credentiale:")
print("   🔐 Admin:      admin@devboost.com  / admin123")
print("   💼 Freelancer: alex@demo.com       / demo123")
print("   💼 Freelancer: maria@demo.com      / demo123  (și restul @demo.com)")
print("   🔍 Client:     client1@demo.com    / demo123")
print("   🔍 Client:     client2@demo.com    / demo123")
