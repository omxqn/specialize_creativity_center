import json
from django.http import QueryDict, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa

from Home.models import Profile
from Home.decorators import allowed_users
from django.contrib.auth.decorators import login_required

from patient.models import Lab_examination, Prescription, Medicines, TestType, Test, test_perameters
from pharamacy.models import Main_category, Product, Cart, CartItem, Order, OrderItem
from io import BytesIO


# Create your views here.

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# pdf = render_to_pdf('new/group_goal_statement.html',context)
# return HttpResponse(pdf, content_type='application/pdf')

def test_report_pdf(request,id,test_type):
    x=Prescription.objects.get(pk=id)
    print('Line no 39',x.patient.name)
    report_info=Test.objects.filter(prescription=x,test_type=test_type)
    print('Line no 41',report_info)
    context={'report_info': report_info,'test_type':test_type,'x':x}
    pdf = render_to_pdf('lab/test_report_pdf.html',context )
    return HttpResponse(pdf, content_type='application/pdf')

@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy','Lab'])
def pharamacy_dashboard(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    if user_profile.role == 'Lab':
        return redirect('pharamacy_patient_prescription')
    context = {'user_profile': user_profile,
               'users': users, }
    return render(request, 'pharamacy_dashboard.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def pharamacy_devices(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, }
    return render(request, 'pharamacy_devices.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def pharamacy_medicine_stock(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    all_products = Product.objects.filter(available=True)
    context = {'user_profile': user_profile,
               'users': users, 'all_products': all_products}
    return render(request, 'pharamacy_medicine_stock.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def add_medicine(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'categories': Main_category.objects.all()}
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        if not product_name:
            messages.error(request, 'Product Name is required')
            return redirect('add_medicine')
        if not description:
            messages.error(request, 'Description is required')
            return redirect('add_medicine')
        if category == 'Select':
            messages.error(request, 'Select category please')
            return redirect('add_medicine')

        if not stock:
            messages.error(request, 'Stock required')

            return redirect('add_medicine')
        if not price:
            messages.error(request, 'Price required')

            return redirect('add_medicine')
        x = Main_category.objects.get(id=category)
        Product.objects.create(name=product_name, category=x, stock=stock, price=price,
                               description=description).save()
        messages.error(request, 'Stock added succesffuly.')

        return redirect('add_medicine')
    return render(request, 'add_medicine_stock.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def edit_medicine(request, id):
    users = User.objects.get(username=request.user)
    product_info = Product.objects.get(pk=id)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'categories': Main_category.objects.all(), 'product_info': product_info}
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        price = request.POST.get('price')

        if not product_name:
            messages.error(request, 'Product Name is required')
            return redirect('edit_medicine', product_info.id)
        if not description:
            messages.error(request, 'Description is required')
            return redirect('edit_medicine', product_info.id)
        if category == 'Select':
            messages.error(request, 'Select category please')
            return redirect('edit_medicine', product_info.id)

        if not stock:
            messages.error(request, 'Stock required')

            return redirect('add_medicine')
        if not price:
            messages.error(request, 'Price required')

            return redirect('add_medicine')
        x = Main_category.objects.get(id=category)
        print('Print value of category:', category, x.id, x.name)
        product_info.name = product_name
        product_info.category = x
        product_info.stock = stock
        product_info.price = price
        product_info.description = description
        product_info.save()
        messages.error(request, 'Stock updated succesffuly.')

        return redirect('edit_medicine', product_info.id)
    return render(request, 'edit_medicine_stock.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy','Lab'])
def pharamacy_patient_prescription(request):
    users = User.objects.get(username=request.user)
    Prescriptions = Prescription.objects.all()

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'Prescriptions': Prescriptions}
    return render(request, 'pharamacy_patient_prescriptions.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def prescription_details(request, id):
    users = User.objects.get(username=request.user)
    prescription_info = Prescription.objects.get(pk=id)
    medicine_list = Medicines.objects.filter(prescription=prescription_info).order_by('-date')
    Lab_examination_list = Lab_examination.objects.filter(prescription=prescription_info).order_by('-date')
    if request.method == 'POST':
        test_fee = request.POST.get('test_fee')
        examination_id = request.POST.get('examination_id')
        x = Lab_examination.objects.get(id=examination_id)

        if len(test_fee) != 0:
            x.test_fee = test_fee

        if len(request.FILES) != 0:
            my_file = request.FILES['test_upload']

            x.report = my_file

            x.save()

        x.save()

        messages.success(request, 'Report addedd successfully')
        return redirect('prescription_details', prescription_info.id)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'prescription_info': prescription_info, 'medicine_list': medicine_list,
               'Lab_examination_list': Lab_examination_list}
    return render(request, 'pharamacy_patient_prescriptions_details.html', context)

@csrf_exempt
def add_test_report(request, id):
    users = User.objects.get(username=request.user)
    Lab_examination_info = Lab_examination.objects.get(pk=id)
    test_type_info=TestType.objects.get(pk=Lab_examination_info.test_type_id)

    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract the 'results' dictionary from the JSON data
        results = data.get('results', {})
        print('Line no 205 is:',results)

        # Process the results data as needed
        for row_id, result in results.items():
            # Do something with the row_id and result
            print(f"Row ID: {row_id}, Result: {result}")
            perameter_info = test_perameters.objects.get(pk=row_id)
            Test.objects.create(prescription=Lab_examination_info.prescription,test_type=test_type_info.type_name,perameter_name=perameter_info.perameter_name,ref_range=perameter_info.ref_range,results=result).save()


        redirect_url = reverse('test_report_pdf', args=[Lab_examination_info.prescription.id, test_type_info.type_name])
        return JsonResponse({'message': 'Results processed successfully', 'redirect_url': redirect_url}, status=200)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users,'test_type_info':test_type_info}
    return render(request, 'lab/add_test_report.html', context)
@login_required(login_url='Login')
@allowed_users(allowed_roles=['Lab'])
def prescription_details_lab(request, id):
    users = User.objects.get(username=request.user)
    prescription_info = Prescription.objects.get(pk=id)
    medicine_list = Medicines.objects.filter(prescription=prescription_info).order_by('-date')
    Lab_examination_list = Lab_examination.objects.filter(prescription=prescription_info).order_by('-date')

    if request.method == 'POST':
        test_fee = request.POST.get('test_fee')
        examination_id = request.POST.get('examination_id')
        x = Lab_examination.objects.get(id=examination_id)

        if len(test_fee) != 0:
            x.test_fee = test_fee

        if len(request.FILES) != 0:
            my_file = request.FILES['test_upload']

            x.report = my_file

            x.save()

        x.save()

        messages.success(request, 'Report addedd successfully')
        return redirect('prescription_details', prescription_info.id)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile,
               'users': users, 'prescription_info': prescription_info, 'medicine_list': medicine_list,
               'Lab_examination_list': Lab_examination_list}
    return render(request, 'lab/pharamacy_patient_prescriptions_details_lab.html', context)


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def pharamacy_profile(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    context = {'user_profile': user_profile, 'users': users}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        phone = request.POST.get('phone_number')

        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname

        if len(phone) != 0:
            user_profile.phone = phone

        if len(request.FILES) != 0:
            my_file = request.FILES['upload']

            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                user_profile.picture = request.FILES['upload']

                users.save()
                user_profile.save()

                messages.success(request, 'Data updated successfully')
                return redirect('pharamacy_profile')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('pharamacy_profile')
        users.save()
        user_profile.save()
        messages.success(request, 'Data updated successfully')
        return redirect('pharamacy_profile')

    return render(request, 'pharamacy_setting.html', context)


def _cart_id(request):
    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    return session_id


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    # cart, created = Cart.objects.get_or_create(cart_id='xyz')

    try:  # update
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:  # creating new cart item
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart_detail')





@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def add_to_cart(request):



    if request.method == 'POST':

        ids = request.POST.getlist('id[]')




        for product_id in ids:
            print('line no 808',product_id)
            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
            # cart, created = Cart.objects.get_or_create(cart_id='xyz')

            try:  # update
                cart_item = CartItem.objects.get(product=product, cart=cart)
                if cart_item.quantity < cart_item.product.stock:
                    cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:  # creating new cart item
                cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                cart_item.save()




        return JsonResponse(
            'Product added into cart', safe=False
        )







@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def cart_detail(request, total=0, counter=0, cart_items=None):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe_total = int(total)

    if request.method == 'POST':

        billingName = request.POST.get('stripeBillingName')
        billingAddress1 = request.POST.get('stripeBillingAddressLine1')
        billingCity = request.POST.get('stripeBillingAddressCity')
        billingPostcode = request.POST.get('stripeBillingAddressZip')
        billingCountry = request.POST.get('stripeBillingAddressCountryCode')

        order_details = Order.objects.create(total=total, billingName=billingName, billingCity=billingCity,
                                             billingPostcode=billingPostcode,
                                             billingCountry=billingAddress1, )
        order_details.save()
        for order_item in cart_items:
            or_item = OrderItem.objects.create(product=str(order_item.product), quantity=order_item.quantity,
                                               price=order_item.product.price, order=order_details)
            or_item.save()

            # reduce stock
            products = Product.objects.get(id=order_item.product.id)
            products.stock = int(order_item.product.stock - order_item.quantity)
            products.save()
            order_item.delete()

        return redirect('thanks_page', order_details.id)

    return render(request, 'cart.html',
                  dict(cart_items=cart_items, total=total, counter=counter, stripe_total=stripe_total,
                       user_profile=user_profile,
                       users=users))


def random_with_N_digits(param):
    pass


@login_required(login_url='Login')
@allowed_users(allowed_roles=['Pharamacy'])
def thanks_page(request, order_id):
    order_details = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order_details)
    # print('Line no 260 is:',len(order_items))
    #
    #
    # user_email = []
    # user_email.append(order_details.emailAddress)
    # subject = 'Thank you for placing order.'
    #
    # html_content = render_to_string('email/order_email_new.html',
    #                                 {'order_no': str(random_with_N_digits(10)), 'total': order_details.total,'order_items':order_items,'order_details':order_details
    #                                  })
    # text_content = strip_tags(html_content)
    #
    # msg = EmailMultiAlternatives(subject, text_content, 'adnanrafique340@gmail.com', user_email)
    # msg.attach_alternative(html_content, "text/html")
    #
    # msg.send()
    request.session.flush()
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)

    return render(request, 'thankyou_page.html',
                  {'order_no': str(random_with_N_digits(10)), 'order_details': order_details,
                   'user_profile': user_profile,
                   'users': users})


def cart_remove(request, product_id):  # minus button fucntionaly
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # cart = Cart.objects.get(cart_id='xyz')
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')
