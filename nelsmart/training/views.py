from django.shortcuts import render, redirect
from .forms import ApplicationForm
from django.core.mail import EmailMessage
from .models import TrainingContent
import urllib.parse

def apply_training(request):
    form = ApplicationForm()

    # ✅ Get video from admin
    video = TrainingContent.objects.filter(is_active=True).first()

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()

            # ---------- EMAIL ----------
            try:
                email = EmailMessage(
                    'Training Application Received',
                    f'Thank you {application.name} for applying to NELSMART ELECTRONIC training program.',
                    to=[application.email],
                )
                email.send()
            except Exception as e:
                print("Email error:", e)

            # ---------- WHATSAPP ----------
            message = f"""
Hello, I want to apply for NELSMART Training:

Name: {application.name}
Email: {application.email}
Phone: {application.phone}
"""

            encoded_message = urllib.parse.quote(message)

            whatsapp_number = "237675940002"

            whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_message}"

            return redirect(whatsapp_url)

    return render(request, 'training/apply.html', {
        'form': form,
        'video': video
    })