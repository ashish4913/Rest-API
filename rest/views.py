from django.shortcuts import render
from .models import user
from .serializers import userserializer
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
# Create your views here. """

# this is function based views

@csrf_exempt
def test(request):

    if request.method=='GET': #this is get api
        u=user.objects.all() #now we have to seralize this query set
        serializer=userserializer(u,many=True) # many =True because this is query set it may have many objects 
        return JsonResponse(serializer.data,safe=False) #safe =False because serialized is list of dictionary it contain many objects

    elif request.method=='POST':
        data=JSONParser().parse(request)
        u=userserializer(data=data)
        if u.is_valid():
            u.save()
            return JsonResponse(u.data,status=201)
        else:
            return JsonResponse(u.errors,status=400)
@csrf_exempt
def test_details(request,id):

    try:
        u=user.objects.get(id=id)
    except Exception as e:
        return JsonResponse({'error':'user not found'},status=404)

    if request.method=='GET': #this is get api
       
        serializer=userserializer(u) # many =True because this is query set it may have many objects 
        return JsonResponse(serializer.data,safe=True) #safe =True because serialized is list of dictionary it contain single objects

    elif request.method=='PUT':
        data=JSONParser().parse(request)
        s=userserializer(u,data=data)
        if s.is_valid():
            s.save()
            return JsonResponse(s.data,status=201)
        else:
            return JsonResponse(s.errors,status=400)

    elif request.method=='Delete':
        u.delete()
        return JsonResponse({'msg':'user deleted sucessfully'},status=200)





# class based views generic api
class testclass(APIView):
    def get(self,request):
        u=user.objects.all() #now we have to seralize this query set
        serializer=userserializer(u,many=True) # many =True because this is query set it may have many objects 
        return Response(serializer.data,status=200) #safe =False because serialized is list of dictionary it contain many objects
        

    def post(self,request):
        data=request.data
        s=userserializer(data=data)
        if s.is_valid():
            s.save()
            return Response(s.data,status=201)
        else:
            return Response(s.errors,status=400)




class testclassdetails(APIView):
    def getobject(self,id):
        try:
            return user.objects.get(id=id)
        except Exception as e:
            return Response({'error':'user not found'},status=404)
    def get(self,request,id=None):
        u=self.getobject(id)
        serializer=userserializer(u) # many =True because this is query set it may have many objects 
        return Response(serializer.data,status=200)

    def put(self,request,id=None):
        u=self.getobject(id)
        data=request.data
        s=userserializer(u,data=data)
        if s.is_valid():
            s.save()
            return Response(s.data,status=201)
        else:
            return Response(s.errors,status=400)

    def delete(self,request,id=None):
        u=u=self.getobject(id)
        u.delete()
        return HttpResponse(status=204)







#generic api


class testgeneric (generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    serializer_class=userserializer
    queryset=user.objects.all()
    lookup_field="id"

    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id) 
        else:
            return self.list(request)  
    
    def post(self,request):
        return self.create(request)
    
    def put(self,request,id=None):
        return self.update(request,id)


    def delete(self,request,id=None):
        return self.destroy(request,id)