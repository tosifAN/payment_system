from django.shortcuts import render
import json
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from payments.models import Payment
from django.contrib.auth.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        if request.user:
            user = request.user
            user = User.objects.first()
            print("i am user {user}")
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        try:
            data = json.loads(request.body)
            amount = int(data.get('amount'))
            description = 'Payment for services or goods'  # Description for export transactions

            # Create a Stripe PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
                description=description,
                  shipping={
                    'name': "tosif",
                    'address': {
                        'line1': "strange",
                        'city': 'City Name',  # Replace with actual city
                        'state': 'State Name',  # Replace with actual state
                        'country': 'India',  # Replace with actual country code
                        'postal_code': '12345'  # Replace with actual postal code
                    }
                }
            )

            # Debugging information
            print(f"Creating payment with amount: {amount / 100}, stripe_payment_intent: {payment_intent['id']}")

            # Save the payment information to the database
            payment = Payment.objects.create(
                user=user,
                amount=amount / 100,  # Convert cents to dollars
                status='pending',
                stripe_payment_intent=payment_intent['id']
            )

            print(f"Payment saved: {payment}")

            if payment_intent['status'] == 'succeeded':
                payment.status = 'completed'
                payment.save()

            # Return clientSecret for frontend to use
            return JsonResponse({
                'clientSecret': payment_intent['client_secret']
            })

        except Exception as e:
            # Log the exception details
            print(f"Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def payment_form(request):
    return render(request, 'payments/payment_form.html', {
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def home(request):
     return render(request, 'payments/index.html')