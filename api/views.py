# api/views.py
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentResponseSerializer
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf_receipt(payment_obj):
    """Generate a PDF receipt with payment details (no image)."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add payment details
    p.drawString(100, 750, f"Receipt for {payment_obj.name}")
    p.drawString(100, 730, f"Payment ID: {payment_obj.id}")
    p.drawString(100, 710, f"Amount: ${payment_obj.amount}")
    p.drawString(100, 690, f"Status: {payment_obj.status}")
    p.drawString(100, 670, f"Date: {payment_obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    p.drawString(100, 650, "Thank you for your transaction!")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentResponseSerializer

    def create(self, request, *args, **kwargs):
        """Create a new payment and send a creation email with PDF receipt."""
        serializer = PaymentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment_obj = serializer.save()

            # Generate PDF receipt
            pdf_buffer = generate_pdf_receipt(payment_obj)

            # Send email with PDF attachment
            email = EmailMessage(
                subject='Payment Created',
                body=f'Hello {payment_obj.name},\n\nYour payment of ${payment_obj.amount} has been created and is being processed.\n\nSee attached receipt.\n\nThank you!',
                from_email=settings.EMAIL_HOST_USER,
                to=[payment_obj.email],
            )
            email.attach(f'receipt_{payment_obj.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            return Response({
                "message": "Payment created. Use 'complete', 'return', or 'cancel' actions.",
                "payment_id": str(payment_obj.id)
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_payment(self, request, pk=None):
        """Complete the payment and send a completion email with PDF receipt."""
        try:
            payment_obj = self.get_object()
            if payment_obj.status != 'pending':
                return Response({"message": f"Payment is already {payment_obj.status}"}, status=status.HTTP_400_BAD_REQUEST)

            payment_obj.status = 'completed'
            payment_obj.save()

            # Generate PDF receipt
            pdf_buffer = generate_pdf_receipt(payment_obj)

            # Send email with PDF attachment
            email = EmailMessage(
                subject='Payment Successful',
                body=f'Hello {payment_obj.name},\n\nYour payment of ${payment_obj.amount} has been successfully processed.\n\nSee attached receipt.\n\nThank you!',
                from_email=settings.EMAIL_HOST_USER,
                to=[payment_obj.email],
            )
            email.attach(f'receipt_{payment_obj.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            serializer = PaymentResponseSerializer(payment_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='return')
    def return_payment(self, request, pk=None):
        """Return (confirm) the payment and send a return email with PDF receipt."""
        try:
            payment_obj = self.get_object()
            if payment_obj.status != 'pending':
                return Response({"message": f"Payment is already {payment_obj.status}"}, status=status.HTTP_400_BAD_REQUEST)

            payment_obj.status = 'returned'
            payment_obj.save()

            # Generate PDF receipt
            pdf_buffer = generate_pdf_receipt(payment_obj)

            # Send email with PDF attachment
            email = EmailMessage(
                subject='Payment Returned',
                body=f'Hello {payment_obj.name},\n\nYour payment of ${payment_obj.amount} has been returned and processed successfully.\n\nSee attached receipt.\n\nThank you!',
                from_email=settings.EMAIL_HOST_USER,
                to=[payment_obj.email],
            )
            email.attach(f'receipt_{payment_obj.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            serializer = PaymentResponseSerializer(payment_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_payment(self, request, pk=None):
        """Cancel the payment and send a cancellation email with PDF receipt."""
        try:
            payment_obj = self.get_object()
            if payment_obj.status != 'pending':
                return Response({"message": f"Payment is already {payment_obj.status}"}, status=status.HTTP_400_BAD_REQUEST)

            payment_obj.status = 'canceled'
            payment_obj.save()

            # Generate PDF receipt
            pdf_buffer = generate_pdf_receipt(payment_obj)

            # Send email with PDF attachment
            email = EmailMessage(
                subject='Payment Canceled',
                body=f'Hello {payment_obj.name},\n\nYour payment of ${payment_obj.amount} has been canceled.\n\nSee attached receipt.\n\nIf this was a mistake, please try again. Thank you!',
                from_email=settings.EMAIL_HOST_USER,
                to=[payment_obj.email],
            )
            email.attach(f'receipt_{payment_obj.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send(fail_silently=False)

            serializer = PaymentResponseSerializer(payment_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)