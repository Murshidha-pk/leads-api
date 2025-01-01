from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from api.models import Lead

from api.serializers import LeadSerializer

from rest_framework import authentication,permissions

from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.

class BookListCreateView(APIView):

    def get(self,request,*args,**kwargs):

        context={"message":"listing all books"}

        return Response(data=context)
    
    def post(self,request,*args,**kwargs):

        context={"message":"creating a new book object"}

        return Response(data=context)
    
#put,update,delete next clss

class BookRetrieveUpdateDestroyView(APIView):

    def get(self,request,*args,**kwargs):

        context={"message":"fetch a specific book detail"}

        return Response(data=context)
    
    def put(self,request,*args,**kwargs):

        context={"message":"logic for updating a book"}

        return Response(data=context)
    
    def delete(self,request,*args,**kwargs):

        context={"message":"logic for deleting a book"}

        return Response(data=context)
    

#serializers
#list

class LeadListCreateView(APIView):

    authentication_classes=[JWTAuthentication]

    permission_classes=[permissions.IsAdminUser]

    def get(self,request,*args,**kwargs):

        qs=Lead.objects.all()

        #converting query set to python native_type

        serializer_instance=LeadSerializer(qs,many=True) #serializertion
        
        #get data from serializer_instance

        return Response(data=serializer_instance.data)
    
#create

    def post(self,request,*args,**kwargs):
        
        serializer_instance=LeadSerializer(data=request.data) #deserializertion

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
    
        return Response(data=serializer_instance.errors)     #if maybe errors

#detail

class LeadRetrieveDestroyUpdateView(APIView):

    authentication_classes=[JWTAuthentication]

    permission_classes=[permissions.IsAdminUser]

    serializer_class=LeadSerializer

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Lead.objects.get(id=id)
        
        serializer_instance=self.serializer_class(qs)   #here get one field using id so not use many=True

        return Response(data=serializer_instance.data)
    
    #delete

    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Lead.objects.get(id=id).delete()

        return Response(data={"message":"deleted"})
    
    #update 

    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        lead_obj=Lead.objects.get(id=id)

        serializaer_instance=self.serializer_class(data=request.data,instance=lead_obj)

        if serializaer_instance.is_valid():

            serializaer_instance.save()

            return Response(data=serializaer_instance.data)
        
        return Response(data=serializaer_instance.errors)

#summary
from django.db.models import Count
class LeadSummaryView(APIView):

    def get(self,request,*args,**kwargs):

        total_lead_count=Lead.objects.all().count()

        source_summary=Lead.objects.all().values("source").annotate(count=Count("source"))

        course_summary=Lead.objects.all().values("course").annotate(count=Count("course"))

        status_summary=Lead.objects.all().values("status").annotate(count=Count("status"))

        





        context={
            "total":total_lead_count,
            "source_summary":source_summary,
            "course_summary":course_summary,
            "status_summary":status_summary,
        }

        return Response(data=context)


    




