from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
from io import StringIO
import plotly.express as px
import plotly.io as pio

# Home Page View
def home_page(request):
    return render(request, "home.html")

# Page 1 (User Dashboard)
@login_required
def page1(request):
    return render(request, 'page1.html', {})

# User Signup View
def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("page1")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def upload_and_display(request):
    dataset_name = None
    table = None
    describe_html = None
    info_html = None
    info = None

    # If the form is submitted with a file
    if request.method == "POST" and "dataset" in request.FILES:
        dataset = request.FILES["dataset"]
        dataset_name = dataset.name

        try:
            # Save the uploaded file in session (for later retrieval)
            request.session['dataset'] = dataset.read().decode('utf-8')
            request.session['dataset_name'] = dataset.name  # Store dataset name

            # Read the uploaded CSV file into pandas DataFrame
            df = pd.read_csv(StringIO(request.session['dataset']))

            # Save the dataframe to the session for later use
            request.session['df'] = df.to_dict(orient='records')  # Save as dict for session storage

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

    # If the dataset is already stored in session (on page reload)
    elif 'dataset' in request.session:
        dataset_name = request.session.get('dataset_name')
        try:
            df = pd.read_csv(StringIO(request.session['dataset']))

            # Save the dataframe to the session for later use
            request.session['df'] = df.to_dict(orient='records')  # Save as dict for session storage

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
            return render(request, "page1.html", {"error": f"Error loading session data: {e}"})

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

# Dataset Visualization View
@login_required
def visualize(request):
    plot_div = None
    df = None

    # Check if the DataFrame (df) is in the session (it would be passed from upload_and_display)
    if "df" in request.session:
        df = pd.DataFrame(request.session["df"])  # Load the DataFrame from session
        
        if request.method == "POST":
            # Get x, y, and plot type from the form
            x_column = request.POST.get("x_column")
            y_column = request.POST.get("y_column")
            plot_type = request.POST.get("plot_type")

            # Create the plot based on the selected options
            try:
                if plot_type == "hist":
                    fig = px.histogram(df, x=x_column, nbins=20, title=f"Histogram of {x_column}")
                elif plot_type == "scatter":
                    fig = px.scatter(df, x=x_column, y=y_column, title=f"Scatter Plot: {x_column} vs {y_column}")
                elif plot_type == "count":
                    fig = px.histogram(df, x=x_column, title=f"Count Plot of {x_column}")
                
                # Convert the plot to HTML for embedding
                plot_div = pio.to_html(fig, full_html=False)
            except Exception as e:
                return render(request, "visualize.html", {"error": f"Error creating plot: {e}"})

    return render(
        request,
        "visualize.html",
        {
            "plot_div": plot_div,  # Pass the plot as HTML if a plot was generated
            "df": df,  # Pass the DataFrame to select columns for plotting
            "columns": df.columns.tolist() if df is not None else []  # Provide column names for form selection
        },
    )