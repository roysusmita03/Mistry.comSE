from .models import Product, Order
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

def SignUpPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Validate that fields are not empty
        if not uname or not email or not pass1 or not pass2:
            return render(request, 'shop/signup.html', {'error': 'All fields are required.'})

        # Check if passwords match
        if pass1 != pass2:
            return render(request, 'shop/signup.html', {'password_error': 'Passwords do not match.'})

        # Create the user
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('LoginPage')

    return render(request, 'shop/signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        print(username, pass1)
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username and Password is Incorrect!")
    return render(request, 'shop/login.html')


def LogoutPage(request):
    logout(request)
    return redirect('LoginPage')


def index(request):  # Defines the `index` view function, which handles HTTP requests.
    product_objects = Product.objects.all()  # Retrieves all Product objects from the database.

    # search code
    # Extracts the 'item_name' parameter from the GET request, used for filtering products.
    item_name = request.GET.get('item_name')  
    if item_name != '' and item_name is not None:  # Checks if 'item_name' is not empty or None.
        # Filters the product objects by checking if 'item_name' is contained in the 'category' field.
        product_objects = product_objects.filter(category__icontains=item_name)

    # paginator code
    paginator = Paginator(product_objects, 8)  # Creates a paginator object to divide the product list into pages, 8 items per page.
    page = request.GET.get("page")  # Gets the current page number from the GET request.
    product_objects = paginator.get_page(page)  # Retrieves the products for the specified page.

    # Renders the 'shop/index.html' template, passing the paginated product objects as context.
    return render(request, 'shop/index.html', {'product_objects': product_objects})  


def detail(request, id):
    product_object = Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object': product_object})


def about(request):
    return render(request, 'shop/about.html')


def training(request):
    return render(request, 'shop/training.html')


def checkout(request):  # Defines the checkout view function to handle HTTP requests for the checkout process.
    if request.method == "POST":  # Checks if the request method is POST, indicating a form submission.
        items = request.POST.get('items', '')  # Retrieves the 'items' value from the POST request, defaulting to an empty string if not provided.
        name = request.POST.get('name', "")  # Retrieves the 'name' value from the POST request, defaulting to an empty string if not provided.
        email = request.POST.get('email', "")  # Retrieves the 'email' value from the POST request, defaulting to an empty string if not provided.
        address = request.POST.get('address', "")  # Retrieves the 'address' value from the POST request, defaulting to an empty string if not provided.
        city = request.POST.get('city', "")  # Retrieves the 'city' value from the POST request, defaulting to an empty string if not provided.
        state = request.POST.get('state', "")  # Retrieves the 'state' value from the POST request, defaulting to an empty string if not provided.
        zipcode = request.POST.get('zipcode', "")  # Retrieves the 'zipcode' value from the POST request, defaulting to an empty string if not provided.
        total = request.POST.get('total', "")  # Retrieves the 'total' value from the POST request, defaulting to an empty string if not provided.
        order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode,  # Creates an Order object with the retrieved data.
                      total=total)
        order.save()  # Saves the Order object to the database.

    return render(request, 'shop/checkout.html')  # Renders the checkout.html template to display the checkout page.


from django.shortcuts import redirect, get_object_or_404
from decimal import Decimal
from django.urls import reverse


def rate_product(request, id):
    product_object = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        # Get the rating from the form input
        rating_input = request.POST.get('rating')

        # Check if the rating input is not empty
        if rating_input:
            try:
                # Convert the input to a float
                rating = float(rating_input)

                # Convert the rating to Decimal
                decimal_rating = Decimal(rating)

                # Update product rating (average it with the existing rating)
                product_object.rating = (product_object.rating + decimal_rating) / Decimal('2')

                # Save the product object
                product_object.save()
            except ValueError:
                # In case of invalid input, just ignore and do nothing
                pass

        # Redirect back to the detail page
        return redirect(reverse('detail', args=[id]))

    # If the request is not POST, redirect to the detail page
    return redirect(reverse('detail', args=[id]))




# #This code is part of a Django project, implementing views for an e-commerce-like application. Here’s a breakdown of the code:

# ---

# ### **Imports**
# - **Models**: `Product` and `Order` are imported from the `models` module, representing database tables for products and orders.
# - **Django Utilities**:
#   - `Paginator` handles pagination of lists.
#   - `HttpResponse`, `render`, and `redirect` handle HTTP responses and rendering templates.
#   - `User`, `authenticate`, `login`, and `logout` manage user authentication.
#   - `messages` enables sending feedback messages to users.
#   - `login_required` is a decorator to restrict access to certain views.
# - **Decimal**: Handles precision for product ratings.

# ---

# ### **View Functions**

# #### **SignUpPage**
# - Displays a sign-up form (`signup.html`) for creating a new user.
# - **POST Method**:
#   - Validates user input to ensure fields are not empty.
#   - Checks if passwords match.
#   - Creates a new `User` object in the database using `create_user`.
#   - Redirects to the login page after successful registration.
# - **GET Method**:
#   - Renders the sign-up template.

# ---

# #### **LoginPage**
# - Displays a login form (`login.html`) to authenticate users.
# - **POST Method**:
#   - Fetches username and password from the request.
#   - Authenticates the user using Django's `authenticate`.
#   - Logs in the user if credentials are correct and redirects to the `index` page.
#   - Displays an error message for invalid credentials.
# - **GET Method**:
#   - Renders the login template.

# ---

# #### **LogoutPage**
# - Logs out the current user using Django's `logout` and redirects to the login page.

# ---

# #### **index**
# - Displays a paginated list of products on the main page (`index.html`).
# - **Search Feature**:
#   - Filters products by category based on the `item_name` query parameter.
# - **Pagination**:
#   - Limits the number of products displayed per page (8).
#   - Uses `Paginator` to generate paginated results.

# ---

# #### **detail**
# - Displays detailed information about a specific product using its `id`.
# - Renders the `detail.html` template with the product object.

# ---

# #### **about**
# - Displays an informational "About" page using the `about.html` template.

# ---

# #### **training**
# - Displays a "Training" page using the `training.html` template.

# ---

# #### **checkout**
# - Handles checkout operations.
# - **POST Method**:
#   - Retrieves customer and order details from the request.
#   - Creates and saves an `Order` object in the database.
# - **GET Method**:
#   - Renders the `checkout.html` template.

# ---

# #### **rate_product**
# - Allows users to rate a product.
# - **POST Method**:
#   - Retrieves the `rating` input from the form.
#   - Validates and converts the input to a `Decimal` value.
#   - Updates the product's `rating` by averaging the new and existing ratings.
#   - Saves the updated product object to the database.
#   - Redirects to the `detail` page of the product.
# - **Fallback**:
#   - Redirects to the `detail` page if the request is not `POST`.

# ---

# ### **Key Features**
# 1. **User Management**:
#    - Supports sign-up, login, and logout functionalities.
# 2. **Product Management**:
#    - Lists, searches, paginates, and displays detailed product information.
# 3. **Order Processing**:
#    - Saves customer details and orders during checkout.
# 4. **Product Rating**:
#    - Implements a simple rating system that averages user inputs.

# ---

# ### **Enhancements Possible**
# 1. Add validation for existing usernames or emails during sign-up.
# 2. Implement messages for successful actions or errors (e.g., using `messages`).
# 3. Enhance error handling (e.g., invalid `id` in `detail` or `rate_product`).
# 4. Protect views like `index` and `detail` with `login_required` decorators.
# 5. Improve UI feedback for search and rating operations.






















































































































































































































































































































































