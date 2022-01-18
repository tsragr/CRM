from rest_framework import serializers

from .models import Company, Office, Worker, Profile, UserSkill, UserLanguage


class CompanyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'about', 'is_active', 'created_at')


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'amount_offices', 'created_at', 'updated_at')


class CompanyDetailSerializer(serializers.ModelSerializer):
    offices = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model = Company
        fields = ('name', 'about', 'offices', 'created_at',)


class OfficeSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)

    url_company = serializers.HyperlinkedRelatedField(source='company', view_name='company-detail',
                                                      read_only=True)

    class Meta:
        model = Office
        fields = ('name', 'location', 'created_at', 'updated_at', 'company', 'url_company')

    def get_location(self, obj):
        return obj.location.name


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'patronymic')


class WorkersSerializer(serializers.ModelSerializer):
    worker_info = ProfileSerializer(source='employer', read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'worker_info', 'position']
        read_only = True


class OfficesCompanySerializer(serializers.ModelSerializer):
    workers = WorkersSerializer(many=True, )
    location = serializers.SerializerMethodField()

    class Meta:
        model = Office
        fields = ('name', 'workers', 'amount_workers', 'location')

    def get_location(self, obj):
        return obj.location.name


class CreateOfficeCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('name', 'location')
