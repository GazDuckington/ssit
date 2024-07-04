from django import forms
from .models import Nasabah, Pengajuan


class PengajuanForm(forms.ModelForm):
    class Meta:
        model = Pengajuan
        fields = [
            "nominal",
            "user",
            "metode",
        ]
        labels = {
            "nominal": "Nominal",
            # "user": "Nasabah",
            "metode": "Metode",
        }
        widgets = {
            "nominal": forms.NumberInput(),
            "user": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(PengajuanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["user"].initial = Nasabah.objects.get(uid=user)
            self.fields["user"].disabled = True
            # self.fields["user"].queryset = Nasabah.objects.get(uid=user.id)
