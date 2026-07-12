from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Patient, Appointment, Payment
from .serializers import PatientSerializer, AppointmentSerializer, PaymentSerializer

from django.shortcuts import redirect

def index(request):
    return redirect('/index.html')

@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = Patient.objects.get(email=email, password=password)
        serializer = PatientSerializer(user)
        return Response({"success": True, "user": serializer.data})
    except Patient.DoesNotExist:
        return Response({"success": False, "message": "Invalid credentials"})

@api_view(['POST', 'GET'])
def appointment(request):
    if request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Appointment booked successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

@api_view(['POST', 'GET'])
def process_payment(request):
    if request.method == 'POST':
        cardholder_name = request.data.get('cardholder_name')
        card_number = request.data.get('card_number')
        
        # Simple mock validation
        if not cardholder_name or not card_number or len(card_number) < 4:
            return Response({"error": "Invalid payment details"}, status=status.HTTP_400_BAD_REQUEST)
            
        card_last_four = card_number[-4:]
        
        payment = Payment.objects.create(
            cardholder_name=cardholder_name,
            card_last_four=card_last_four,
            amount=150.00, # Fixed mock amount
            status='Success'
        )
        serializer = PaymentSerializer(payment)
        return Response({"message": "Payment Successful", "payment": serializer.data}, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

