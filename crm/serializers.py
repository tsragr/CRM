from rest_framework import serializers

from .models import Company, Office, Worker, Profile, UserSkill, UserLanguage


class CompanyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'about', 'is_active', 'created_at')

    def create(self, validated_data):
        company = Company.objects.create(**validated_data)
        Cooperation.objects.create(company=company)
        return company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'amount_offices', 'created_at', 'updated_at')


class CompanyDetailSerializer(serializers.ModelSerializer):
    offices = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ('name', 'about', 'offices', 'created_at',)


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('name',)


class OfficesCompanySerializer(serializers.ModelSerializer):
    workers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Office
        fields = ('workers', 'amount_workers')
