from django.http import HttpResponse,Http404
from django.shortcuts import redirect, render
from spaces.models import File,Space
from django.utils.text import slugify
from spaces.utils import decrypt, encrypt
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django import forms
from Crypto.PublicKey import RSA

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

def home_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST'  :
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                clean_file = request.FILES['file']
                file_name = clean_file.name
                clean_file = clean_file.read()
                key=request.user.space.first().public_key
                public_key = RSA.import_key(key)
                encrypted_bytes = encrypt(clean_file, public_key)
                encrypted_file = ContentFile(encrypted_bytes, name=file_name) 
                
                # Assign the temporary file to the FileField
                space = request.user.space.first()
                file = File(
                    space=space,
                    name=file_name,
                    file=encrypted_file
                )
                file.save()
                            
                return redirect("home")
        else:
            form = FileUploadForm()
        space = request.user.space.first()
        files = File.objects.filter(space=space)
        for f in files :
            f.size = f.file.size
        return render(request, 'home.html', {'user': request.user, 'form':form,'files': files })
    return redirect('/')

@login_required
def my_files_page(request):
    space = request.user.space.first()
    files = File.objects.filter(space=space)
    for f in files :
        f.size = f.file.size
    return render(request, 'my_files.html', {'files': files})


@login_required
def download_key(request, key_type):
    space = request.user.space.first()
    if key_type == 'private':
        key_data = space.private_key
        file_extension = 'private_key.txt'
    elif key_type == 'public':
        key_data = space.public_key
        file_extension = 'public_key.txt'
    else:
        return HttpResponse("Invalid key type", status=400)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{slugify(space.user.username)}_{file_extension}"'
    response.write(key_data)
    return response

@login_required
def download_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.get(space=space, id=file_id)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    response.write(file.file.read())
    return response

@login_required
def decrypt_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.filter(space=space, id=file_id)
    if file.count() == 0 : return Http404() 
    file = file.first()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    decrypted_bytes = decrypt(file.file.read(), RSA.import_key(space.private_key))
    try:
        decrypted_string = decrypted_bytes.decode('utf-8')
    except :
        decrypted_string = decrypted_bytes
    response.write(decrypted_string)
    return response

@login_required
def delete_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.filter(space=space, id=file_id)
    if file.count() == 0 : return Http404() 
    file = file.first()
    file.delete()
    return redirect('home')