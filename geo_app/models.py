from django.db import models


class UploadDetails(models.Model):

    """This model is for the file"""

    file = models.FileField(upload_to='files')

    def __str__(self):
        return f'File with data parameters.'


class Details(models.Model):

    """This model will hold the project details"""

    project_name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    affiliated_agency = models.CharField(max_length=500)
    description = models.TextField()
    project_start_time = models.DateField()
    project_completion_time = models.DateField()
    total_budget = models.IntegerField()
    completion_percentage = models.FloatField()
    issue_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Details of {self.project_name} "


class Coordinates(models.Model):

    """This one holds coordinates information for a project."""

    details = models.ForeignKey(Details, on_delete=models.CASCADE)

    lng = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)


class Issue(models.Model):

    """Holds issue data and it's parent project."""

    details = models.ForeignKey(Details, on_delete=models.CASCADE)
    issue = models.CharField(max_length=200)

    def __str__(self):
        return f' Issue of {self.details.project_name}'


class CountAnn(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'User visited { self.count}'
