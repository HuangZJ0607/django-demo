from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from PIL import Image


class ArticleColumn(models.Model):
    """栏目的model"""
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    """文章的model"""
    # 定义文章作者。 author 通过 models.ForeignKey 外键与内建的 User 模型关联在一起
    # 参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。通常设置为 CASCADE 级联删除就可以了
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(ArticleColumn, null=True, blank=True, on_delete=models.CASCADE, related_name='article')

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题。
    # models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    # CharField 有一个必填参数 max_length，它规定字符的最大长度
    title = models.CharField(max_length=100)

    # 文章正文。
    # 保存大量文本使用 TextField
    body = models.TextField()

    # 浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 点赞数
    likes = models.PositiveIntegerField(default=0)

    # 文章创建时间。DateTimeField 为一个日期字段。参数default=timezone.now指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数auto_now=True指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        # ordering是元组，括号中只含一个元素是要补上逗号
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        # reverse()方法返回文章详情页面的url，实现了路由重定向
        return reverse('article:article-detail', args=[self.id])

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article

    def was_created_recently(self):
        # 若文章是 1 分钟内发表的，则返回 True
        diff = timezone.now() - self.created

        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False
