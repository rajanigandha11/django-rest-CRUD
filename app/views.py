from django.shortcuts import render

import io 
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def student_app(request):
    if request.method == 'GET':
        # Use query parameters instead of parsing request body for GET request
        id = request.GET.get('id', None)
        
        if id is not None:
            try:
                stu = Student.objects.get(id=id)
                serializer = StudentSerializer(stu)
                json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(json_data, content_type='application/json')
            except Student.DoesNotExist:
                return HttpResponse(json.dumps({'error': 'Student not found'}), content_type='application/json', status=404)
        else:
            return HttpResponse(json.dumps({'error': 'ID parameter is required'}), content_type='application/json', status=400)

    if request.method == 'POST':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)
        
        if serializer.is_valid():
            serializer.save()
            res = {'msg': 'Data created'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json', status=201)  # Created status

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json', status=400)


    if request.method == 'PUT':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id=pythondata.get('id')
        stu=Student.objects.get(id=id)
        serializer=StudentSerializer(stu,data=pythondata,partial=True)
        if serializer.is_valid():
            serializer.save()
            res ={'msg':'data updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json',status=201)
        json_data =JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json',status=400)

    if request.method == 'DELETE':
        json_data=request.body
        stream=io.BytesIO(json_data)
        pythondata=JSONParser().parse(stream)
        id=pythondata.get('id')
        stu=Student.objects.get(id=id)
        stu.delete()
        res ={'msg':'data deleted'}
        json_data = JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json',status=201)
        json_data =JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json',status=400)





