from Crypto.PublicKey import RSA
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify

from spaces.models import File
from spaces.tasks import encrypt_and_save
from spaces.utils import decrypt, get_all_files

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={"class": "custom-file-input"}))


async def home_page(request):
    is_authenticated = request.user.is_authenticated
    if is_authenticated:
        space = request.user.space.first()

        if request.method == "POST":
            form = FileUploadForm(request.POST, request.FILES)
            web_file = request.FILES["file"]
            raw_file = web_file.read()
            file_name = web_file.name
            file_instance = File.objects.create(space=space, name=file_name, end=False, data=raw_file)
            encrypt_and_save(request.user.id, file_instance.id)
            return redirect("home")
        else:
            form = FileUploadForm()
        
        return render(
            request, "home.html", {"user": request.user, "form": form, "files": get_all_files(space)}
        )
    else:
        return render(request, "home.html", {"user": request.user})


@login_required
def my_files_page(request):
    space = request.user.space.first()
    files = File.objects.filter(space=space)
    for f in files:
        f.size = f.file.size
    return render(request, "my_files.html", {"files": files})


@login_required
def download_key(request, key_type):
    space = request.user.space.first()
    if key_type == "private":
        key_data = space.private_key
        file_extension = "private_key.txt"
    elif key_type == "public":
        key_data = space.public_key
        file_extension = "public_key.txt"
    else:
        return HttpResponse("Invalid key type", status=400)
    response = HttpResponse(content_type="text/plain")
    response[
        "Content-Disposition"
    ] = f'attachment; filename="{slugify(space.user.username)}_{file_extension}"'
    response.write(key_data)
    return response


@login_required
def download_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.get(space=space, id=file_id)
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="{file.name}"'
    response.write(file.data)
    return response


@login_required
def decrypt_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.filter(space=space, id=file_id)
    if file.count() == 0:
        return Http404()
    file = file.first()
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = f'attachment; filename="{file.name}"'
    decrypted_bytes = decrypt(file.data, RSA.import_key(space.private_key))
    try:
        decrypted_string = decrypted_bytes.decode("utf-8")
    except:
        decrypted_string = decrypted_bytes
    response.write(decrypted_string)
    return response


@login_required
def delete_file(request, file_id):
    space = request.user.space.first()
    file = File.objects.filter(space=space, id=file_id)
    if file.count() == 0:
        return Http404()
    file = file.first()
    file.delete()
    return redirect("home")
