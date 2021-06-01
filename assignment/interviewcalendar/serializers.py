from rest_framework import serializers
from .models import User
from datetime import datetime
import datetime as dt

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['slots']

    def validate_slots(self, value):
        user = self.instance
        user_slots = user.slots
        slots_to_add = []
        for slot in value['slots']:
            dates=slot.split(' ')
            print(dates)
            date = datetime.strptime(dates[0], '%d/%m/%Y')
            hours = dates[1].split('-')
            start_hour = dt.time.fromisoformat(hours[0])
            end_hour = dt.time.fromisoformat(hours[1])
            date1 = datetime.combine(date, start_hour)
            date2 = datetime.combine(date, end_hour)
            print(date1, date2)
            print(date2-date1 == dt.timedelta(hours=1))
            user_slots.append(slot)
        
        # for key in value:
            # date = key
            # try:
            #     date_object = datetime.strptime(date, '%d-%m-%Y').date()
            #     print(date_object)
            # except:
            #     raise serializers.ValidationError("Date format should be: dd-mm-yyyy")
            # for hour in value[key]:
            #     if not isinstance(hour, int):
            #         raise serializers.ValidationError("Hours should be integers")
            #     if hour > 23 or hour < 0:
            #         raise serializers.ValidationError("Hours can't be bigger than 23 and smaller than 0")
            #     time = dt.time(hour, 0, 0)
            #     datetime_object = datetime.combine(date_object, time)
            #     if datetime_object < datetime.now():
            #         raise serializers.ValidationError("Date should be in future")
            # user_slots[key] = user_slots.get(key, []) + value[key]
        return user_slots