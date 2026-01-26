from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DoctorAvailability
from .serializers import DoctorAvailabilitySerializer
from users.models import CustomUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_availability(request):
    """Doctor creates an availability slot"""
    if not request.user.is_doctor():
        return Response({'error': 'Only doctors can create availability slots'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = DoctorAvailabilitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(doctor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_availability(request):
    """Doctor lists their own availability slots"""
    if not request.user.is_doctor():
        return Response({'error': 'Only doctors can view availability slots'}, status=status.HTTP_403_FORBIDDEN)
    
    slots = DoctorAvailability.objects.filter(doctor=request.user)
    serializer = DoctorAvailabilitySerializer(slots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_available_doctors(request):
    """Patient views available doctors and their slots"""
    if not request.user.is_patient():
        return Response({'error': 'Only patients can view available doctors'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get only future, unbooked slots
    today = timezone.now().date()
    slots = DoctorAvailability.objects.filter(
        date__gte=today,
        is_booked=False
    ).select_related('doctor')
    
    serializer = DoctorAvailabilitySerializer(slots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_availability(request, doctor_id):
    """Get availability slots for a specific doctor"""
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
    
    # Get only future, unbooked slots
    today = timezone.now().date()
    slots = DoctorAvailability.objects.filter(
        doctor=doctor,
        date__gte=today,
        is_booked=False
    )
    
    serializer = DoctorAvailabilitySerializer(slots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_availability(request, slot_id):
    """Get, update, or delete an availability slot"""
    slot = get_object_or_404(DoctorAvailability, id=slot_id)
    
    # Only the doctor who created the slot can manage it
    if slot.doctor != request.user:
        return Response({'error': 'You can only manage your own availability slots'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        serializer = DoctorAvailabilitySerializer(slot)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        # Can't update if already booked
        if slot.is_booked:
            return Response({'error': 'Cannot update a booked slot'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = DoctorAvailabilitySerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Can't delete if already booked
        if slot.is_booked:
            return Response({'error': 'Cannot delete a booked slot'}, status=status.HTTP_400_BAD_REQUEST)
        
        slot.delete()
        return Response({'message': 'Availability slot deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_doctors(request):
    """Get list of all doctors"""
    doctors = CustomUser.objects.filter(role='doctor')
    from users.serializers import UserSerializer
    serializer = UserSerializer(doctors, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
