from django import forms
import pdb
from momonitor.main.models import (SimpleServiceCheck, 
                                   UmpireServiceCheck, 
                                   CompareServiceCheck,
                                   ComplexServiceCheck,
                                   CodeServiceCheck,
                                   ComplexRelatedField,
                                   Service)

class ServiceCheckForm(forms.ModelForm):
    title = "Create/Edit Resources"
    enctype = None
    service = forms.CharField(widget=forms.HiddenInput(attrs={'readonly':True}))
    def __init__(self,*args,**kwargs):
        service_id = kwargs.pop("service_id","")
        super(ServiceCheckForm,self).__init__(*args,**kwargs)
        if service_id:
            self.fields['service'].widget.attrs['value'] = service_id
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['description'].widget.attrs['placeholder'] = "Enter brief description here..."
        self.fields['name'].widget.attrs['placeholder'] = "Check Name"
        self.fields['failures_before_alert'].widget.attrs['placeholder'] = "i.e. 1"
        self.fields['frequency'].widget.attrs['placeholder'] = "i.e. */5 * * * *"
        if self.fields.has_key("endpoint"):
            self.fields['endpoint'].widget.attrs['placeholder'] = "http://example.org"
        if self.fields.has_key("timeout"):
            self.fields['timeout'].widget.attrs['placeholder'] = "i.e. 100"
        

class UmpireServiceCheckForm(ServiceCheckForm):
    title="Create/Edit Umpire Checks"
    template="modal_forms/umpire_check.html"
    class Meta:
        model = UmpireServiceCheck

class CompareServiceCheckForm(ServiceCheckForm):
    title="Create/Edit Compare Checks"
    template="modal_forms/compare_check.html"
    class Meta:
        model = CompareServiceCheck

    def __init__(self,*args,**kwargs):
        super(CompareServiceCheckForm,self).__init__(*args,**kwargs)
        self.fields['comparator'].widget.attrs['style'] = "width:100px"
        self.fields['compared_value'].widget.attrs['style'] = "width:100px"

class SimpleServiceCheckForm(ServiceCheckForm):
    title="Create/Edit Simple Checks"
    template="modal_forms/simple_check.html"
    class Meta:
        model = SimpleServiceCheck

class CodeServiceCheckForm(forms.ModelForm):
    enctype = "multipart/form-data"
    title="Create/Edit Code Checks"
    template="modal_forms/code_check.html"
    
    def __init__(self,*args,**kwargs):
        service_id = kwargs.pop("service_id","")
        super(CodeServiceCheckForm,self).__init__(*args,**kwargs)
        self.fields['service'].widget.attrs['class']="hide"
        self.fields['service'].widget.attrs['readonly']=True
        self.fields['description'].widget.attrs['rows'] = 5
        self.fields['description'].widget.attrs['placeholder'] = "Enter brief description here..."

    class Meta:
        model = CodeServiceCheck

class ComplexServiceCheckForm(ServiceCheckForm):
    title="Create/Edit Complex Check"
    class Meta:
        model = ComplexServiceCheck

class ComplexRelatedForm(forms.ModelForm):
    complex_check = forms.CharField(widget=forms.HiddenInput(attrs={'readonly':True}))
    title = "Add Rule to Complex Check"
    class Meta:
        model = ComplexRelatedField

class ServiceForm(forms.ModelForm):
    title="Create/Edit Service"
    template="modal_forms/serviceform.html"
    class Meta:
        model = Service

RESOURCE_FORM_MAP = {
    Service:ServiceCheckForm,
    UmpireServiceCheck:UmpireServiceCheckForm,
    SimpleServiceCheck:SimpleServiceCheckForm,
    ComplexServiceCheck:ComplexServiceCheckForm,
    CompareServiceCheck:CompareServiceCheckForm,
    CodeServiceCheck:CodeServiceCheckForm,
    ComplexRelatedField:ComplexRelatedForm,
    Service:ServiceForm
}
