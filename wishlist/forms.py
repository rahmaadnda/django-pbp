from django import forms
from .models import BarangWishlist

class Input_Form(forms.ModelForm):
    class Meta:
        model = BarangWishlist
        fields = ["nama_barang","nama_barang", "deskripsi",]