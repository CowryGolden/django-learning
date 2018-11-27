from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    """ 主题表单 """
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
    
class EntryForm(forms.ModelForm):
    """ 主题相关条目的表单 """
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}    # 字段text的输入小部件，将文本区域的宽度设置为80列