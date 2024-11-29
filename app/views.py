from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home_page(request):
    return render(request, "home.html")

@login_required
def page1(request):
    return render (request, 'page1.html', {})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("page1")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form":form}) 

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os

@login_required
def upload_file(request):
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        return HttpResponse(f"File uploaded at {file_url}")
    return render(request, "page1.html")

@login_required
def create_dataset(request):
    # Add logic for creating datasets
    return HttpResponse("Dataset created successfully!")

@login_required
def export_dataset(request):
    # Add logic for exporting datasets
    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename=datasets.zip"
    # Include dataset export logic here
    return response

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from io import StringIO

@login_required
def upload_and_display(request):
    dataset_name = None
    table = None
    describe_html = None
    info_html = None  # For storing formatted info output
    info = None

    if request.method == "POST" and "dataset" in request.FILES:
        dataset = request.FILES["dataset"]
        dataset_name = dataset.name

        try:
            # Read the uploaded CSV file
            df = pd.read_csv(dataset)

            # Generate dataset details
            table = {
                "columns": df.columns.tolist(),
                "values": df.head(10).values.tolist(),  # Display first 10 rows
            }
            describe = df.describe()

            # Convert the describe result to HTML table
            describe_html = describe.to_html(classes='table table-bordered table-striped')

            # Capture info as a string
            buffer = StringIO()
            df.info(buf=buffer)
            info = buffer.getvalue()

            # Format the info as HTML for better visualization
            info_html = "<pre style='white-space: pre-wrap;'>"
            info_html += info.replace("\n", "<br>")  # Replace newlines with <br> tags
            info_html += "</pre>"

        except Exception as e:
            return render(request, "page1.html", {"error": f"Error processing file: {e}"})

    return render(
        request,
        "page1.html",
        {
            "dataset_name": dataset_name,
            "table": table,
            "describe_html": describe_html,  # Pass describe as HTML
            "info_html": info_html,  # Pass formatted info as HTML
            "info": info,  # You can still pass the raw info if needed
        },
    )