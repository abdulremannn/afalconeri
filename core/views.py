from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import DroneSystem, Capability, ContactInfo
import json


# ── Helpers ──────────────────────────────────────────────────
def _systems_data_from_db():
    systems = DroneSystem.objects.all()
    result = []
    for s in systems:
        result.append({
            'id': s.system_id,
            'name': s.name,
            'designation': s.designation,
            'class': s.system_class,
            'tagline': s.tagline,
            'description': s.description,
            'status': s.status,
            'specs': s.get_specs(),
            'features': s.get_features(),
            'image': s.image.url if s.image else None,
        })
    return result


def _caps_data_from_db():
    caps = Capability.objects.all()
    result = []
    for c in caps:
        result.append({
            'id': c.cap_id,
            'number': c.number,
            'title': c.title,
            'subtitle': c.subtitle,
            'description': c.description,
            'items': c.get_items(),
        })
    return result


def _default_systems():
    return [
        {
            'id': 'falcon-x1', 'name': 'Falcon X1', 'designation': 'Surveillance Platform',
            'class': 'RECONNAISSANCE', 'tagline': 'Eyes Above the Horizon',
            'description': 'Long-endurance multi-sensor surveillance drone engineered for persistent ISR operations. Equipped with EO/IR payloads and real-time data-link for continuous battlefield awareness.',
            'specs': [
                {'label': 'Max Altitude', 'value': '4,500 m'}, {'label': 'Endurance', 'value': '18 hrs'},
                {'label': 'Range', 'value': '120 km'}, {'label': 'Payload', 'value': '6 kg'},
                {'label': 'Wing Span', 'value': '3.2 m'}, {'label': 'MTOW', 'value': '22 kg'},
            ],
            'features': ['EO/IR Multi-Sensor', 'AES-256 Encrypted Link', 'Anti-Jamming Suite', 'Autonomous Navigation', 'GCS Compatible'],
            'status': 'OPERATIONAL',
        },
        {
            'id': 'falcon-x2', 'name': 'Falcon X2', 'designation': 'Tactical UAV',
            'class': 'TACTICAL STRIKE', 'tagline': 'Precision. Speed. Lethality.',
            'description': 'High-speed tactical UAV designed for time-critical strike missions. Features modular payload architecture supporting kinetic and electronic warfare packages.',
            'specs': [
                {'label': 'Max Speed', 'value': '280 km/h'}, {'label': 'Endurance', 'value': '6 hrs'},
                {'label': 'Range', 'value': '200 km'}, {'label': 'Payload', 'value': '12 kg'},
                {'label': 'Length', 'value': '2.8 m'}, {'label': 'MTOW', 'value': '35 kg'},
            ],
            'features': ['Modular Strike Payload', 'Multi-Spectral Targeting', 'Satcom Datalink', 'Low Acoustic Signature', 'Encrypted C2'],
            'status': 'DEVELOPMENT',
        },
        {
            'id': 'falcon-l3', 'name': 'Falcon L3', 'designation': 'Loitering Munition',
            'class': 'LOITERING MUNITION', 'tagline': 'Persistent Threat. Decisive Strike.',
            'description': 'Tube-launched loitering munition with autonomous target identification and terminal guidance against hardened targets.',
            'specs': [
                {'label': 'Loiter Time', 'value': '90 min'}, {'label': 'Range', 'value': '40 km'},
                {'label': 'Warhead', 'value': '3.5 kg'}, {'label': 'Launch System', 'value': 'Tube'},
                {'label': 'Guidance', 'value': 'AI + GPS'}, {'label': 'MTOW', 'value': '14 kg'},
            ],
            'features': ['AI Target Recognition', 'Abort & Re-engage', 'Minimal RF Signature', 'Day/Night Capable', 'Single Operator'],
            'status': 'PROTOTYPE',
        },
        {
            'id': 'civil-recon', 'name': 'CR-100', 'designation': 'Civil Surveillance',
            'class': 'CIVIL OPERATIONS', 'tagline': 'Securing Infrastructure at Scale',
            'description': 'Certified civil surveillance platform for border monitoring, critical infrastructure protection, and law enforcement operations.',
            'specs': [
                {'label': 'Max Altitude', 'value': '3,000 m'}, {'label': 'Endurance', 'value': '12 hrs'},
                {'label': 'Coverage', 'value': '80 km²/hr'}, {'label': 'Payload', 'value': '4 kg'},
                {'label': 'Certifications', 'value': 'EASA/FAA'}, {'label': 'MTOW', 'value': '18 kg'},
            ],
            'features': ['Civil Airspace Certified', 'ADS-B Compliant', 'LTE/5G Connectivity', 'Cloud Analytics', 'Operator Training'],
            'status': 'OPERATIONAL',
        },
    ]


def _default_caps():
    return [
        {'id':'aerospace','number':'01','title':'Aerospace Engineering','subtitle':'Structural & Aerodynamic Design','description':'Full-cycle aerospace engineering from conceptual design through flight certification.','items':['Composite Airframe Design','CFD & FEA Simulation','Propulsion Integration','Flight Test & Certification','Thermal Management']},
        {'id':'ai-targeting','number':'02','title':'AI-Powered Targeting','subtitle':'Machine Vision & Target Acquisition','description':'Proprietary neural network architectures for real-time target classification and tracking.','items':['Multi-Class Object Detection','Track-Before-Detect','Human-Machine Teaming','Edge AI Processing','Low-Latency Inference']},
        {'id':'autonomous-nav','number':'03','title':'Autonomous Navigation','subtitle':'GPS-Denied Operations','description':'Advanced navigation combining INS, visual odometry, terrain mapping, and AI path planning.','items':['INS/VIO Fusion','Terrain Following','Obstacle Avoidance','Swarm Coordination','GPS-Denied Ops']},
        {'id':'defense-electronics','number':'04','title':'Defense Electronics','subtitle':'EW & Signal Intelligence','description':'Integrated electronic warfare suites and hardened avionics for contested RF environments.','items':['Electronic Warfare Payloads','SIGINT Collection','RF Countermeasures','Hardened Avionics','TEMPEST Standards']},
        {'id':'communications','number':'05','title':'Secure Communications','subtitle':'Encrypted C2 Infrastructure','description':'End-to-end encrypted C2 infrastructure with frequency-hopping and mesh networking.','items':['AES-256 Encryption','FHSS Datalinks','Satcom Integration','Mesh Networking','Zero-Trust Architecture']},
    ]


def _default_contact():
    return {
        'headquarters': 'AFalconeri Technologies HQ — Islamabad, Pakistan',
        'postal': 'P.O. Box 1000, Islamabad, Pakistan',
        'secure_comms': 'Encrypted communications available upon clearance verification.',
        'inquiries_email': 'inquiries@afalconeri.com',
        'disclaimer': 'All defense product inquiries are subject to jurisdiction verification and applicable export control regulations including ITAR and EAR. Unauthorized access to restricted technical information is prohibited.',
    }


# ── Public Views ─────────────────────────────────────────────
def home(request):
    try:
        if DroneSystem.objects.exists():
            systems_data = _systems_data_from_db()
        else:
            systems_data = _default_systems()
    except Exception:
        systems_data = _default_systems()
    return render(request, 'core/home.html', {'page': 'home', 'systems': systems_data})


def systems(request):
    try:
        if DroneSystem.objects.exists():
            systems_data = _systems_data_from_db()
        else:
            systems_data = _default_systems()
    except Exception:
        systems_data = _default_systems()
    return render(request, 'core/systems.html', {'page': 'systems', 'systems': systems_data})


def capabilities(request):
    try:
        if Capability.objects.exists():
            caps_data = _caps_data_from_db()
        else:
            caps_data = _default_caps()
    except Exception:
        caps_data = _default_caps()
    return render(request, 'core/capabilities.html', {'page': 'capabilities', 'capabilities': caps_data})


def about(request):
    return render(request, 'core/about.html', {'page': 'about'})


def contact(request):
    success = False
    form = ContactForm()
    try:
        info = ContactInfo.objects.first()
        contact_info = {
            'headquarters': info.headquarters,
            'postal': info.postal,
            'secure_comms': info.secure_comms,
            'inquiries_email': info.inquiries_email,
            'disclaimer': info.disclaimer,
        } if info else _default_contact()
    except Exception:
        contact_info = _default_contact()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"AFT Contact: {cd.get('subject', 'New Inquiry')} — {cd.get('name', '')}"
            message = f"""
NEW CONTACT FORM SUBMISSION
===========================
Name:         {cd.get('name', '')}
Organization: {cd.get('organization', '')}
Email:        {cd.get('email', '')}
Country:      {cd.get('country', '')}
Subject:      {cd.get('subject', '')}
Inquiry Type: {cd.get('inquiry_type', '')}

MESSAGE:
{cd.get('message', '')}
===========================
Submitted via AFalconeri Technologies website.
"""
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email error: {e}")
            success = True
            form = ContactForm()

    return render(request, 'core/contact.html', {
        'page': 'contact', 'form': form,
        'success': success, 'contact_info': contact_info,
    })


# ══════════════════════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════════════════════

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('core:admin_dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('core:admin_dashboard')
        else:
            error = 'Invalid credentials or insufficient permissions.'
    return render(request, 'core/admin/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('core:home')


@login_required(login_url='/command/login/')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    try:
        systems_count = DroneSystem.objects.count()
        caps_count = Capability.objects.count()
        has_contact = ContactInfo.objects.exists()
    except Exception:
        systems_count = caps_count = 0
        has_contact = False
    return render(request, 'core/admin/dashboard.html', {
        'systems_count': systems_count,
        'caps_count': caps_count,
        'has_contact': has_contact,
        'user': request.user,
    })


@login_required(login_url='/command/login/')
def admin_systems(request):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    # Seed defaults if empty
    if not DroneSystem.objects.exists():
        for i, s in enumerate(_default_systems()):
            DroneSystem.objects.create(
                order=i, system_id=s['id'], name=s['name'],
                designation=s['designation'], system_class=s['class'],
                tagline=s['tagline'], description=s['description'],
                status=s['status'],
                specs_json=json.dumps(s['specs']),
                features_json=json.dumps(s['features']),
            )
    systems = DroneSystem.objects.all()
    return render(request, 'core/admin/systems.html', {'systems': systems})


@login_required(login_url='/command/login/')
def admin_system_edit(request, system_id):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    system = get_object_or_404(DroneSystem, id=system_id)

    if request.method == 'POST':
        system.name        = request.POST.get('name', system.name).strip()
        system.designation = request.POST.get('designation', system.designation).strip()
        system.system_class= request.POST.get('system_class', system.system_class).strip()
        system.tagline     = request.POST.get('tagline', system.tagline).strip()
        system.description = request.POST.get('description', system.description).strip()
        system.status      = request.POST.get('status', system.status)

        # Handle image upload
        if request.FILES.get('image'):
            system.image = request.FILES['image']

        # Parse specs — 6 rows of label/value pairs
        specs = []
        for i in range(1, 7):
            lbl = request.POST.get(f'spec_label_{i}', '').strip()
            val = request.POST.get(f'spec_value_{i}', '').strip()
            if lbl and val:
                specs.append({'label': lbl, 'value': val})
        system.specs_json = json.dumps(specs)

        # Parse features — comma separated
        feat_raw = request.POST.get('features', '')
        features = [f.strip() for f in feat_raw.split(',') if f.strip()]
        system.features_json = json.dumps(features)

        system.save()
        messages.success(request, f'{system.name} updated successfully.')
        return redirect('core:admin_systems')

    specs = system.get_specs()
    # Pad to 6 rows
    while len(specs) < 6:
        specs.append({'label': '', 'value': ''})
    features_str = ', '.join(system.get_features())
    return render(request, 'core/admin/system_edit.html', {
        'system': system, 'specs': specs, 'features_str': features_str,
    })


@login_required(login_url='/command/login/')
def admin_capabilities(request):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    if not Capability.objects.exists():
        for i, c in enumerate(_default_caps()):
            Capability.objects.create(
                order=i, cap_id=c['id'], number=c['number'],
                title=c['title'], subtitle=c['subtitle'],
                description=c['description'],
                items_json=json.dumps(c['items']),
            )
    caps = Capability.objects.all()
    return render(request, 'core/admin/capabilities.html', {'caps': caps})


@login_required(login_url='/command/login/')
def admin_capability_edit(request, cap_id):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    cap = get_object_or_404(Capability, id=cap_id)

    if request.method == 'POST':
        cap.title       = request.POST.get('title', cap.title).strip()
        cap.subtitle    = request.POST.get('subtitle', cap.subtitle).strip()
        cap.description = request.POST.get('description', cap.description).strip()
        items_raw = request.POST.get('items', '')
        items = [i.strip() for i in items_raw.split('\n') if i.strip()]
        cap.items_json = json.dumps(items)
        cap.save()
        messages.success(request, f'{cap.title} updated successfully.')
        return redirect('core:admin_capabilities')

    items_str = '\n'.join(cap.get_items())
    return render(request, 'core/admin/capability_edit.html', {
        'cap': cap, 'items_str': items_str,
    })


@login_required(login_url='/command/login/')
def admin_contact(request):
    if not request.user.is_staff:
        return redirect('core:admin_login')
    try:
        info = ContactInfo.objects.first()
        if not info:
            d = _default_contact()
            info = ContactInfo.objects.create(**d)
    except Exception:
        info = None

    if request.method == 'POST' and info:
        info.headquarters    = request.POST.get('headquarters', '').strip()
        info.postal          = request.POST.get('postal', '').strip()
        info.secure_comms    = request.POST.get('secure_comms', '').strip()
        info.inquiries_email = request.POST.get('inquiries_email', '').strip()
        info.disclaimer      = request.POST.get('disclaimer', '').strip()
        info.save()
        messages.success(request, 'Contact information updated successfully.')
        return redirect('core:admin_contact')

    return render(request, 'core/admin/contact.html', {'info': info})