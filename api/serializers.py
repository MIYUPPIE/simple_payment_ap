# api/serializers.py
from rest_framework import serializers
from .models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['name', 'email', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'name', 'email', 'amount', 'status', 'reference', 'created_at']
        read_only_fields = ['id', 'status', 'reference', 'created_at']