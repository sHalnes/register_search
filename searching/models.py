from django.db import models

# Create your models here.
class SearchResults(models.Model):
    '''
    A database of companies which were searched via the searching app. Just in case.
    '''

    id = models.IntegerField(verbose_name='Organizarion number', primary_key=True)
    org_name = models.CharField(max_length=100)
    last_visited = models.DateTimeField(auto_now=True)
    n_visits = models.IntegerField(default=0)


    def __str__(self):
        '''
        representing model
        :return: self.org_name, self.n_visits, self.last_visited
        '''
        return '{} vas visited {} times. Last visit: {}'.format(self.org_name, self.n_visits, self.last_visited)


# we can also add a new function to display 5 most popular searches