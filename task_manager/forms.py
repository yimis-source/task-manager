from django import forms   

class crete_new_taskForm(forms.Form):
    title = forms.CharField(label='titulo', max_length=100)
    description = forms.CharField(label= 'decripcion de la tarea' ,widget=forms.Textarea)
    due_date = forms.DateField(label='fecha de vencimiento',  widget=forms.SelectDateWidget)