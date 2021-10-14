from rest_framework import serializers

from .models import Company, Cooperation, Office, Worker, Profile, UserSkill, UserLanguage


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
        fields = ('name', 'amount_offices', 'amount_workers', 'created_at', 'updated_at')


class CompanyDetailSerializer(serializers.ModelSerializer):
    offices = serializers.StringRelatedField(many=True)
    workers = serializers.StringRelatedField(many=True)
    get_cooperation = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = ('name', 'about', 'offices', 'workers', 'created_at', 'get_cooperation')


class CooperationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cooperation
        fields = "__all__"
