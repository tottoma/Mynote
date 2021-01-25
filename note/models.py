from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

## ノート機能 https://www.tech-tech.xyz/python-django-tutorial2-html.html
class Category(models.Model):
    """ノートのカテゴリ"""
    name = models.CharField('タイトル', max_length=255)
    color = models.TextField('カラー', blank=True, null=True)

    def __str__(self):
        return self.name
    #def get_posts_count(self):
        #return Note.objects.filter(name=self).count()
## 紐付け https://qiita.com/saka___21/items/5233f4bb4a252bcaf44e
class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='ユーザ名')
    title = models.CharField('タイトル', max_length=20)
    content = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='カテゴリ')
    created_at = models.DateTimeField('作成日', auto_now_add=True)#作成時間 自動
    updated_at = models.DateTimeField('更新日', auto_now=True)#更新時間 自動

    def __str__(self):
        return str(self.note_id)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Note'

## 打鍵数を記録する
class KeyLog(models.Model):
    note_id = models.ForeignKey(Note, to_field='note_id', on_delete=models.PROTECT, verbose_name='note_id')
    counted_at = models.DateTimeField('カウント時間',auto_now_add=True)
    count = models.IntegerField('文字数')
    key = models.IntegerField('キーコード', blank=True, null=True)

    def __str__(self):
        return str(self.note_id)+','+str(self.count)+','+str(self.counted_at)
    class Meta:
        verbose_name = 'KeyLog'
        verbose_name_plural = 'KeyLog'

## 心拍数をwebAPIで取得する
class HeartLog(models.Model):
    # 登録時間はサーバ側で自動的
    user_id = models.IntegerField(
        verbose_name='ユーザID',
        blank=True
    )
    measured_at = models.DateTimeField(#自動
        verbose_name='登録時間',
        auto_now_add=True,
    )
    bpm = models.FloatField(
        verbose_name='心拍数',
        blank=True
    )

    # 以下は管理サイト上の表示設定
    def __str__(self):
        return self.measured_at

    class Meta:
        verbose_name = '心拍データ'
        verbose_name_plural = '心拍データ'
