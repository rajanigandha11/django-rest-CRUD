from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'city']

def create(self,validated_data):
	return Student.object.create(**validated_data)

def update(self,instance,validated_data):
	print(instance.name)
	istance.name = validated_data.get('name',instance.name)
	print(instance.name)
	istance.roll = validated_data.get('roll',instance.roll)
	istance.city = validated_data.get('city',instance.city)
	instance.save()
	return instance