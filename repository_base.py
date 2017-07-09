from datetime import datetime, timedelta

class Repository:
    """Abstract base class for the repositories.
    The sub classes should implement the get_data method."""
    def date_formatted(date):
        return date.strftime('%d %b %H:%M')

    def get_data(self,topic_name, numdays,utcOffsetInMinutes):
        raise NotImplementedError( "Should have implemented this" )