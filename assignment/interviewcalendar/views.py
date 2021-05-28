from .models import User
from .serializers import UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])    
def dates_list(request, pk):
    if request.method == 'GET':
        candidate = User.objects.get(pk=pk)
        candidate_slots = candidate.slots
        recruiters_ids = request.query_params.get('r_ids')  # u'2,3,4' <- this is unicode
        recruiters_ids = recruiters_ids.split(',')
        recruiters = User.objects.filter(pk__in=recruiters_ids)

        for recruiter in recruiters:
            recruiter_slots = recruiter.slots
            for date in candidate_slots:
                if date not in recruiter_slots:
                    del candidate_slots[date]
                else:
                    candidate_hours = candidate_slots[date]
                    recruiter_hours = recruiter_slots[date]
                    candidate_slots[date] = list(set(candidate_hours) & set(recruiter_hours))

        return Response(candidate_slots)