from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .permissions import IsUserOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOnly]

@extend_schema( 
 parameters=[OpenApiParameter( 
     name='r_ids', 
     type={'type': 'string'}, 
     location=OpenApiParameter.QUERY, 
     required=True, 
     style='form', 
     explode=False, 
 )], 
 responses=OpenApiTypes.OBJECT, 
) 
@api_view(['GET'])    
def dates_list(request, pk):
    if request.method == 'GET':
        candidate = User.objects.get(pk=pk)
        candidate_slots = candidate.slots
        recruiters_ids = request.query_params.get('r_ids')
        recruiters_ids = recruiters_ids.split(',')
        recruiters = User.objects.filter(pk__in=recruiters_ids)
        slots = candidate_slots.copy()
        for recruiter in recruiters:
            recruiter_slots = recruiter.slots
            for date in candidate_slots:
                if date not in recruiter_slots:
                    del slots[date]
                else:
                    candidate_hours = slots[date]
                    recruiter_hours = recruiter_slots[date]
                    intersection = list(set(candidate_hours) & set(recruiter_hours))
                    intersection.sort()
                    slots[date] = intersection

        return Response(slots)