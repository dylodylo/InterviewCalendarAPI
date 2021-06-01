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
        user_slots = user.slots['slots']     
        try:
            for slot in value['slots']:
                dates=slot.split(' ')
                try:
                    date = datetime.strptime(dates[0], '%d/%m/%Y')
                except:
                    raise serializers.ValidationError("Date format should be: dd/mm/yyyy")
                try:
                    hours = dates[1].split('-')
                    start_hour = dt.time.fromisoformat(hours[0])
                    end_hour = dt.time.fromisoformat(hours[1])
                    date1 = datetime.combine(date, start_hour)
                    date2 = datetime.combine(date, end_hour)
                except:
                    raise serializers.ValidationError("Hours should be in format: HH:MM-HH:MM")
                if date2-date1 != dt.timedelta(hours=1) or date1.minute != 0:
                    raise serializers.ValidationError("Slots can be only one hour periods, starts from full hour")
                user_slots.append(slot)
        except:
            raise serializers.ValidationError("Give slots in lits")
            
        return {'slots': list(set(user_slots))}