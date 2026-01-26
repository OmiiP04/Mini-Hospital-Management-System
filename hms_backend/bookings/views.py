from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer
from availability.models import DoctorAvailability
from users.models import CustomUser

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Patient creates a booking"""
    if not request.user.is_patient():
        return Response({'error': 'Only patients can create bookings'}, status=status.HTTP_403_FORBIDDEN)
    
    slot_id = request.data.get('availability_slot')
    doctor_id = request.data.get('doctor')
    notes = request.data.get('notes', '')
    
    # Get the slot
    slot = get_object_or_404(DoctorAvailability, id=slot_id)
    
    # Verify the doctor
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')
    
    if slot.doctor != doctor:
        return Response({'error': 'The slot does not belong to the selected doctor'}, status=status.HTTP_400_BAD_REQUEST)
    
    if slot.is_booked:
        return Response({'error': 'This slot is already booked'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            booking = Booking.objects.create(
                patient=request.user,
                doctor=doctor,
                availability_slot=slot,
                notes=notes,
                status='confirmed'
            )
            
            # Try to create Google Calendar events
            from calendar_integration.utils import create_calendar_event
            try:
                event_id = create_calendar_event(booking)
                booking.google_event_id = event_id
                booking.save()
            except Exception as e:
                print(f"Calendar event creation failed: {str(e)}")
            
            # Call serverless email service
            from bookings.utils import send_booking_confirmation_email
            try:
                send_booking_confirmation_email(booking)
            except Exception as e:
                print(f"Email notification failed: {str(e)}")
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_bookings(request):
    """List bookings for the current user"""
    if request.user.is_patient():
        bookings = Booking.objects.filter(patient=request.user)
    elif request.user.is_doctor():
        bookings = Booking.objects.filter(doctor=request.user)
    else:
        return Response({'error': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking(request, booking_id):
    """Get details of a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user is involved in the booking
    if booking.patient != request.user and booking.doctor != request.user:
        return Response({'error': 'You are not authorized to view this booking'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = BookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Only patient or doctor can cancel
    if booking.patient != request.user and booking.doctor != request.user:
        return Response({'error': 'You are not authorized to cancel this booking'}, status=status.HTTP_403_FORBIDDEN)
    
    if booking.status == 'cancelled':
        return Response({'error': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            booking.cancel()
            
            # Cancel Google Calendar event if exists
            if booking.google_event_id:
                from calendar_integration.utils import delete_calendar_event
                try:
                    delete_calendar_event(booking)
                except Exception as e:
                    print(f"Calendar event deletion failed: {str(e)}")
            
            # Send cancellation email
            from bookings.utils import send_booking_cancellation_email
            try:
                send_booking_cancellation_email(booking)
            except Exception as e:
                print(f"Cancellation email failed: {str(e)}")
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_bookings(request, doctor_id):
    """Doctor views their bookings"""
    if not request.user.is_doctor() or request.user.id != doctor_id:
        return Response({'error': 'You can only view your own bookings'}, status=status.HTTP_403_FORBIDDEN)
    
    bookings = Booking.objects.filter(doctor_id=doctor_id)
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
