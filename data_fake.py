from datetime import datetime, timedelta
from repository_base import Repository

class FakeRepository(Repository):
    def get_data(self,topic_name,numdays,utcOffsetInMinutes):

        today=datetime.today()

        # Create some test data
        # Three values from yesterday and three values from today
        dataPoint = ( 
            (20.1,today-timedelta(1.8)),
            (19.1,today-timedelta(1.4)),
            (22.1,today-timedelta(1.2)),
            (23.3,today-timedelta(0.9)),
            (19.1,today-timedelta(0.5)),
            (30.1,today-timedelta(0.1)),
            (29.1,today)
        )

        values = []
        labels = []

        for value,time in dataPoint:
            if (time > (today - timedelta(numdays))):
                values.append(value)
                labels.append(super(FakeRepository,self).date_formatted(time))

        return labels, values
