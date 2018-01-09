from django.shortcuts import render, HttpResponse
from django.urls import reverse
from .forms import NewPartForm
from .models import Part
import json

# Create your views here.
def index(request):
    partform = NewPartForm()
    #print(partform)
    context = {
        'part_form' : partform,
    }
    #print(serializers.serialize('json', Part.objects.all()))
    return render(request, 'parts/index.html', context=context)

def add_child(request):
    if request.method == 'POST':
        model_resp = Part.objects.add_subpart(
            request.POST['parent_id'],
            request.POST['child_id'],
            request.POST['quantity']
        )
        print(model_resp)
        return HttpResponse(json.dumps(model_resp), content_type='application/json')

def remove_child(request):
    if request.method == 'POST':
        model_resp = Part.objects.remove_subpart(
            request.POST['parent_id'],
            request.POST['child_id']
            )
        return HttpResponse(json.dumps(model_resp), content_type='application/json')

def search_for_part_name_json(request):
    if request.method == 'POST':
        ret_json = Part.objects.get_tree_json(request.POST['tree_search'])
        #print(ret_json)
        return HttpResponse(json.dumps(ret_json), content_type='application/json')

def get_part_list(request):
    #print(request.GET)
    if 'search_text' in request.GET:
        return HttpResponse(
            json.dumps(Part.objects.get_flat_json(request.GET['search_text'])),
            content_type='application/json'
            )
    return HttpResponse(json.dumps(Part.objects.get_flat_json('')), content_type='application/json')

def get_part_edit_form(request, part_id):
    found_part = Part.objects.filter(id=part_id)
    if found_part:
        found_part = found_part[0]
        form_data = {
            'part_name' : found_part.name,
            'is_divisable' : found_part.is_divisible,
            'part_desc' : found_part.desc,
        }
        the_form = NewPartForm(initial=form_data)
        context = {
            'part_id' : found_part.id,
            'edit_form' : the_form,
        }
        return render(request, 'parts/edit_form.html', context=context)
    return HttpResponse("Part not found")

def get_new_part_form(request):
    the_form = NewPartForm()
    context = {
        'form' : the_form
    }
    return render(request, 'parts/add_form.html', context=context)

def create_new_part(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status':False}), content_type='application/json')
    form = NewPartForm(request.POST)
    if form.is_valid():
        model_resp = Part.objects.add_new_part(form.cleaned_data)
    else:
        return HttpResponse(json.dumps({
            'status' : False,
            'form' : form.as_table()
        }), content_type='application/json')
    if model_resp['status']:
        return HttpResponse(json.dumps({
            'action':reverse('parts:updatepart', kwargs={'part_id': model_resp['new_part'].id}),
            'status':True
        }), content_type='application/json')
    return HttpResponse(json.dumps(model_resp), content_type='application/json')

def update_part(request, part_id):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status':False}), content_type='application/json')
    form = NewPartForm(request.POST)
    if form.is_valid():
        model_resp = Part.objects.update_part(part_id, form.cleaned_data)
        return HttpResponse(json.dumps(model_resp), content_type='application/json')
    return HttpResponse(json.dumps({'status':False}), content_type='application/json')

def delete_part(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'status':False}), content_type='application/json')
    #print(request.POST)
    model_resp = Part.objects.delete_part(request.POST)
    return HttpResponse(json.dumps(model_resp), content_type='application/json')
