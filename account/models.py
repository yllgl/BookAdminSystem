from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=20,unique=True)
    password = models.CharField(verbose_name="密码",max_length=128)
    email = models.CharField(verbose_name="邮箱",max_length=30,unique=True)
    isadmin = models.BooleanField(verbose_name="管理员账户",default=False)
    def __str__(self):
        return self.username
class Book(models.Model):
    onboard = models.BooleanField(default=True,verbose_name="在架上")
    title = models.CharField(max_length=300,verbose_name="书名")
    summary = models.TextField(verbose_name="图书介绍",blank=True,null=True)
    author = models.CharField(max_length=100, verbose_name="作者",blank=True,null=True)
    imgdir = models.CharField(max_length=300,verbose_name="图片路径",blank=True,null=True)
    translator = models.CharField(max_length=50, verbose_name="译者",blank=True,null=True)
    isbn = models.CharField(max_length=15, verbose_name="ISBN号")
    chinaclass = models.CharField(max_length=30, verbose_name="中图分类号")
    binding = models.CharField(max_length=20, verbose_name="装帧",blank=True,null=True)
    language = models.CharField(max_length=20, verbose_name="语言",blank=True,null=True)
    publisherAddress = models.CharField(max_length=20, verbose_name="出版地",blank=True,null=True)
    price = models.CharField(max_length=40, verbose_name="定价",blank=True,null=True)
    publisher = models.CharField(max_length=40, verbose_name="出版社",blank=True,null=True)
    isbn10 = models.CharField(max_length=10, verbose_name="10位ISBN号")
    page = models.CharField(max_length=6, verbose_name="页数",blank=True,null=True)
    category_choices = (
        (0, "马克思主义、列宁主义、毛泽东思想、邓小平理论"),
        (1, "哲学、宗教"),
        (2, "社会科学总论"),
        (3, "政治、法律"),
        (4, "军事"),
        (5, "经济"),
        (6, "文化、科学、教育、体育"),
        (7, "语言、文字"),
        (8, "文学"),
        (9, "艺术"),
        (10, "历史、地理"),
        (11, "其他"),
        (12, "自然科学总论"),
        (14, "数理科学和化学"),
        (15, "天文学、地球科学"),(16, "生物科学"),
        (17, "医药、卫生"),(18, "农业科学"),(19, "工业技术"),(20, "交通运输"),
        (21, "航空、航天"), (23, "环境科学、安全科学"), (25, "综合性图书"))
    category = models.SmallIntegerField(verbose_name="类别", choices=category_choices)
    pubdate = models.CharField(max_length=15,verbose_name="出版日期",blank=True,null=True)
    def __str__(self):
        return self.title
class Record(models.Model):
    bookid = models.ForeignKey("Book",on_delete=models.CASCADE)
    userid = models.ForeignKey("User", on_delete=models.CASCADE)
    status_choices = ((0,"还书"),(1,"借书"))
    category = models.SmallIntegerField(verbose_name="状态", choices=status_choices)
    datetime = models.DateTimeField(auto_now_add=True,verbose_name="操作时间")