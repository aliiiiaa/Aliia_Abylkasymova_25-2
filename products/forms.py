from django import forms


class ProductCreateForms(forms.Form):
    image = forms.FileField(required=False)
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea())
    rate = forms.FloatField()


class CommentCreateForms(forms.Form):
    text = forms.CharField(max_length=355)

