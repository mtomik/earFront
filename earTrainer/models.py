from __future__ import unicode_literals

from django.db import models
from .validators import validate_only_xml

class Job(models.Model):

    TYPES = (
        ('add','add'),
        ('create_samples','create_samples'),
    )

    # list of statuses that job can have
    STATUSES = (
        ('pending', 'pending'),
        ('started', 'started'),
        ('finished', 'finished'),
        ('failed', 'failed'),
    )

    type = models.CharField(choices=TYPES, max_length=20)
    status = models.CharField(choices=STATUSES, max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    argument = models.PositiveIntegerField()
    result = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        """Save model and if job is in pending state, schedule it"""
        super(Job, self).save(*args, **kwargs)
        if self.status == 'pending':
            from .tasks import TASK_MAPPING
            task = TASK_MAPPING[self.type]
            task.delay(job_id=self.id, n=self.argument)

class SamplesModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    samples_dir = models.CharField(max_length=100)
    positives = models.IntegerField(default=0)
    x_angle = models.FloatField(default=0.3)
    y_angle = models.FloatField(default=0.3)
    z_angle = models.FloatField(default=1.0)
    max_dev = models.IntegerField(default=40)
    w = models.IntegerField(default=20)
    h = models.IntegerField(default=40)
    status = models.CharField(max_length=50, default='NEW')

    def __str__(self):
        return self.name


class TrainerModel(models.Model):

    name = models.CharField(max_length=30)
    result_xml_path = models.CharField(max_length=120, default='')
    positives = models.ForeignKey(SamplesModel)
    negatives = models.IntegerField()
    num_stages = models.FloatField()
    precalcValBuf = models.FloatField()
    precalcIdxBuf = models.FloatField()
    numThreads = models.IntegerField()
    acceptanceBreak = models.FloatField()
    bt = models.CharField(max_length=10, default='RAB')
    minHitRate = models.FloatField()
    maxFalseAlarm = models.FloatField()
    weightTrimRate = models.FloatField()
    maxDepth = models.IntegerField()
    maxWeakCount = models.IntegerField()
    featureType = models.CharField(max_length=10, default='LBP')
    mode = models.CharField(default='ALL', max_length=10)

    status = models.CharField(max_length=50, default='NEW')

    def __str__(self):
        return self.name

class TesterModel(models.Model):
    name = models.CharField(max_length=100, default='default')
    samples = models.CharField(max_length=100, default='samples')
    descriptor = models.CharField(max_length=100, default='descriptor.txt')
    trainer = models.ForeignKey(TrainerModel, blank=True, null=True)
    result = models.FloatField(default=0)
    status = models.CharField(max_length=50, default='NEW')

    def __str__(self):
        return self.trainer.name


class XmlModel(models.Model):
    xml_file = models.FileField(validators=[validate_only_xml])












