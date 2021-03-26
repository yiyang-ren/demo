from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.



#分数表
class Score(models.Model):
    client = models.CharField(max_length=20,unique=True,verbose_name='客户端号')
    score = models.IntegerField(verbose_name='分数', default=0,
                                validators=[MaxValueValidator(10000000), MinValueValidator(1)])

    class Meta:
        verbose_name = '分数登记表'
        verbose_name_plural = verbose_name

#名次表
class Rank(models.Model):
    c_id = models.OneToOneField(Score,on_delete=models.CASCADE,primary_key=True)
    rank = models.IntegerField(validators=[MinValueValidator(1)],verbose_name='名次')