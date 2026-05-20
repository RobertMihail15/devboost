from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Freelancer, ClientProfile, Lead, BlogPost, Campaign

SKILL_CHOICES = ['Frontend', 'Backend', 'Design', 'DevOps', 'Other']
PLATFORM_CHOICES = ['LinkedIn', 'Twitter / X', 'Instagram', 'Facebook', 'TikTok']
CATEGORY_CHOICES = ['Lead Generation', 'Branding', 'SEO', 'Business', 'Career', 'Tech']
INDUSTRY_CHOICES = ['Startup', 'Agenție', 'Corporație', 'ONG', 'Persoană fizică', 'Altele']
PLATFORM_ICONS = {'LinkedIn': '💼', 'Twitter / X': '🐦', 'Instagram': '📸', 'Facebook': '📘', 'TikTok': '🎵'}
CATEGORY_ICONS = {'Lead Generation': '🎯', 'Branding': '🌟', 'SEO': '🔍', 'Business': '💰', 'Career': '🚀', 'Tech': '⚙️'}

def is_admin(u): return u.is_authenticated and u.is_staff

def get_user_role(user):
    """Returns 'admin', 'freelancer', 'client', or None."""
    if not user.is_authenticated: return None
    if user.is_staff: return 'admin'
    if hasattr(user, 'freelancer_profile'): return 'freelancer'
    if hasattr(user, 'client_profile'): return 'client'
    return None

# ── Public ────────────────────────────────────────────────────────────

def home(request):
    freelancers = Freelancer.objects.all()[:6]
    return render(request, 'core/home.html', {
        'freelancers': freelancers,
        'total_freelancers': Freelancer.objects.count(),
        'total_clients': ClientProfile.objects.count(),
        'total_leads': Lead.objects.count(),
    })

def freelancers_list(request):
    skill_filter = request.GET.get('skill', '')
    qs = Freelancer.objects.all()
    if skill_filter:
        qs = qs.filter(skill=skill_filter)
    return render(request, 'core/freelancers.html', {
        'freelancers': qs,
        'skills': SKILL_CHOICES,
        'active_skill': skill_filter,
    })

def freelancer_detail(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    return render(request, 'core/freelancer_detail.html', {'freelancer': freelancer})

def contact_freelancer(request, freelancer_id):
    freelancer = get_object_or_404(Freelancer, id=freelancer_id)
    role = get_user_role(request.user)
    error = None

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if not message:
            error = 'Mesajul este obligatoriu.'
        else:
            client_profile = None
            sender_name = ''
            sender_email = ''

            if role == 'client':
                client_profile = request.user.client_profile
            elif role == 'freelancer' or role == 'admin':
                # Freelancers/admins shouldn't contact, but allow as fallback
                sender_name = f"{request.user.first_name} {request.user.last_name}".strip()
                sender_email = request.user.email
            else:
                # Guest
                sender_name = request.POST.get('sender_name', '').strip()
                sender_email = request.POST.get('sender_email', '').strip()
                if not all([sender_name, sender_email]):
                    error = 'Numele și emailul sunt obligatorii.'

            if not error:
                Lead.objects.create(
                    client=client_profile,
                    freelancer=freelancer,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    message=message,
                )
                return render(request, 'core/contact.html', {
                    'freelancer': freelancer, 'success': True,
                    'role': role,
                })

    prefill = {}
    if role == 'client':
        cp = request.user.client_profile
        prefill = {'name': cp.full_name, 'email': request.user.email}
    elif role in ('freelancer', 'admin'):
        prefill = {'name': f"{request.user.first_name} {request.user.last_name}".strip(), 'email': request.user.email}

    return render(request, 'core/contact.html', {
        'freelancer': freelancer, 'success': False,
        'error': error, 'prefill': prefill, 'role': role,
    })

# ── Blog ──────────────────────────────────────────────────────────────

def blog(request):
    return render(request, 'core/blog.html', {
        'posts': BlogPost.objects.all(),
        'category_icons': CATEGORY_ICONS,
        'can_manage': is_admin(request.user),
    })

def blog_post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'core/blog_post.html', {
        'post': post, 'category_icons': CATEGORY_ICONS,
        'can_manage': is_admin(request.user),
    })

@login_required(login_url='/login/')
def blog_add(request):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    error = None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        body = request.POST.get('body', '').strip()
        category = request.POST.get('category', '').strip()
        if not all([title, excerpt, body]):
            error = 'Titlul, rezumatul și conținutul sunt obligatorii.'
        else:
            post = BlogPost.objects.create(title=title, excerpt=excerpt, body=body, category=category or 'General')
            return redirect('blog_post', post_id=post.id)
    return render(request, 'core/blog_form.html', {'action': 'Adaugă', 'categories': CATEGORY_CHOICES, 'error': error})

@login_required(login_url='/login/')
def blog_edit(request, post_id):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    post = get_object_or_404(BlogPost, id=post_id)
    error = None
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        excerpt = request.POST.get('excerpt', '').strip()
        body = request.POST.get('body', '').strip()
        category = request.POST.get('category', '').strip()
        if not all([title, excerpt, body]):
            error = 'Titlul, rezumatul și conținutul sunt obligatorii.'
        else:
            post.title = title; post.excerpt = excerpt; post.body = body
            post.category = category or post.category; post.save()
            return redirect('blog_post', post_id=post.id)
    return render(request, 'core/blog_form.html', {'action': 'Editează', 'post': post, 'categories': CATEGORY_CHOICES, 'error': error})

@login_required(login_url='/login/')
def blog_delete(request, post_id):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        post.delete(); return redirect('blog')
    return render(request, 'core/confirm_delete.html', {'item_name': post.title, 'cancel_url': f'/blog/{post_id}/'})

# ── Campaigns ─────────────────────────────────────────────────────────

def campaigns(request):
    return render(request, 'core/campaigns.html', {
        'posts': Campaign.objects.all(), 'can_manage': is_admin(request.user),
    })

@login_required(login_url='/login/')
def campaign_add(request):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    error = None
    if request.method == 'POST':
        platform = request.POST.get('platform', '').strip()
        text = request.POST.get('text', '').strip()
        likes = request.POST.get('likes', '0').strip()
        comments = request.POST.get('comments', '0').strip()
        if not all([platform, text]): error = 'Platforma și textul sunt obligatorii.'
        else:
            Campaign.objects.create(platform=platform, text=text,
                likes=int(likes) if likes.isdigit() else 0,
                comments=int(comments) if comments.isdigit() else 0)
            return redirect('campaigns')
    return render(request, 'core/campaign_form.html', {'action': 'Adaugă', 'platforms': PLATFORM_CHOICES, 'platform_icons': PLATFORM_ICONS, 'error': error})

@login_required(login_url='/login/')
def campaign_edit(request, campaign_id):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    campaign = get_object_or_404(Campaign, id=campaign_id)
    error = None
    if request.method == 'POST':
        platform = request.POST.get('platform', '').strip()
        text = request.POST.get('text', '').strip()
        likes = request.POST.get('likes', '0').strip()
        comments = request.POST.get('comments', '0').strip()
        if not all([platform, text]): error = 'Platforma și textul sunt obligatorii.'
        else:
            campaign.platform = platform; campaign.text = text
            campaign.likes = int(likes) if likes.isdigit() else campaign.likes
            campaign.comments = int(comments) if comments.isdigit() else campaign.comments
            campaign.save(); return redirect('campaigns')
    return render(request, 'core/campaign_form.html', {'action': 'Editează', 'campaign': campaign, 'platforms': PLATFORM_CHOICES, 'platform_icons': PLATFORM_ICONS, 'error': error})

@login_required(login_url='/login/')
def campaign_delete(request, campaign_id):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.method == 'POST':
        campaign.delete(); return redirect('campaigns')
    return render(request, 'core/confirm_delete.html', {'item_name': f'Campanie {campaign.platform}', 'cancel_url': '/campaigns/'})

# ── Auth ──────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated: return redirect('home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get('next') or request.GET.get('next') or 'home')
        error = 'Email sau parolă incorecte.'
    return render(request, 'core/login.html', {'error': error})

def logout_view(request):
    logout(request); return redirect('home')

def signup(request):
    if request.user.is_authenticated: return redirect('profile')
    error = None
    # role comes from step 1 (GET param) or hidden field in POST
    role = request.POST.get('role') or request.GET.get('role', '')  # 'freelancer' or 'client'

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not role:
            error = 'Selectează tipul de cont.'
        elif not all([full_name, email, password]):
            error = 'Toate câmpurile obligatorii trebuie completate.'
        elif password != password2:
            error = 'Parolele nu coincid.'
        elif len(password) < 6:
            error = 'Parola trebuie să aibă cel puțin 6 caractere.'
        elif User.objects.filter(username=email).exists():
            error = 'Există deja un cont cu acest email.'
        else:
            parts = full_name.split()
            user = User.objects.create_user(
                username=email, email=email, password=password,
                first_name=parts[0],
                last_name=' '.join(parts[1:]) if len(parts) > 1 else '',
            )
            if role == 'freelancer':
                skill = request.POST.get('skill', 'Other').strip()
                description = request.POST.get('description', '').strip()
                experience_years = request.POST.get('experience_years', '1').strip()
                Freelancer.objects.create(
                    user=user, full_name=full_name, skill=skill,
                    description=description or f'Freelancer specializat în {skill}.',
                    experience_years=int(experience_years) if experience_years.isdigit() else 1,
                )
            else:  # client
                company = request.POST.get('company', '').strip()
                industry = request.POST.get('industry', '').strip()
                description = request.POST.get('description', '').strip()
                ClientProfile.objects.create(
                    user=user, full_name=full_name,
                    company=company, industry=industry, description=description,
                )
            login(request, user)
            return render(request, 'core/signup.html', {'success': True, 'name': full_name, 'role': role})

    return render(request, 'core/signup.html', {
        'success': False, 'error': error, 'role': role,
        'skills': SKILL_CHOICES, 'industries': INDUSTRY_CHOICES,
    })

# ── Profile ───────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    role = get_user_role(user)
    freelancer = getattr(user, 'freelancer_profile', None)
    client = getattr(user, 'client_profile', None)
    saved = False
    error = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        if not full_name:
            error = 'Numele este obligatoriu.'
        else:
            parts = full_name.split()
            user.first_name = parts[0]
            user.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
            user.save()
            if freelancer:
                freelancer.full_name = full_name
                skill = request.POST.get('skill', '').strip()
                if skill: freelancer.skill = skill
                freelancer.description = request.POST.get('description', '').strip()
                exp = request.POST.get('experience_years', '').strip()
                if exp.isdigit(): freelancer.experience_years = int(exp)
                freelancer.save()
            elif client:
                client.full_name = full_name
                client.company = request.POST.get('company', '').strip()
                client.industry = request.POST.get('industry', '').strip()
                client.description = request.POST.get('description', '').strip()
                client.save()
            saved = True

    received_messages = None
    sent_messages = None
    if freelancer:
        received_messages = Lead.objects.filter(freelancer=freelancer).select_related('client').order_by('-created_at')
    elif client:
        sent_messages = Lead.objects.filter(client=client).select_related('freelancer').order_by('-created_at')

    return render(request, 'core/profile.html', {
        'role': role, 'freelancer': freelancer, 'client': client,
        'skills': SKILL_CHOICES, 'industries': INDUSTRY_CHOICES,
        'saved': saved, 'error': error,
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })

# ── Admin ─────────────────────────────────────────────────────────────

@login_required(login_url='/login/')
def admin_view(request):
    if not request.user.is_staff: return render(request, 'core/403.html', status=403)
    leads = Lead.objects.all().select_related('client', 'freelancer').order_by('-created_at')
    return render(request, 'core/admin_view.html', {
        'leads': leads,
        'freelancers': Freelancer.objects.all(),
        'clients': ClientProfile.objects.all(),
        'blog_posts': BlogPost.objects.all(),
        'campaign_posts': Campaign.objects.all(),
    })

# ── API ───────────────────────────────────────────────────────────────

def api_freelancers(request):
    data = list(Freelancer.objects.values('id', 'full_name', 'skill', 'description', 'experience_years'))
    return JsonResponse({'freelancers': data})

def api_leads(request):
    if not request.user.is_staff: return JsonResponse({'error': 'Unauthorized'}, status=401)
    leads = Lead.objects.select_related('client', 'freelancer').all()
    data = [{
        'id': l.id, 'sender': l.get_sender_name(), 'email': l.get_sender_email(),
        'freelancer': str(l.freelancer), 'message': l.message, 'created_at': str(l.created_at),
    } for l in leads]
    return JsonResponse({'leads': data})
