        from django.shortcuts import render,HttpResponse
        from django.contrib import messages
        from .forms import UserRegistrationForm
        from .models import UserRegistrationModel


        # Create your views here.
        def UserRegisterActions(request):
            if request.method == 'POST':
                form = UserRegistrationForm(request.POST)
                if form.is_valid():
                    print('Data is Valid')
                    form.save()
                    messages.success(request, 'You have been successfully registered')
                    form = UserRegistrationForm()
                    return render(request, 'UserRegistrations.html', {'form': form})
                else:
                    messages.success(request, 'Email or Mobile Already Existed')
                    print("Invalid form")
            else:
                form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        def UserLoginCheck(request):
            if request.method == "POST":
                loginid = request.POST.get('loginname')
                pswd = request.POST.get('pswd')
                print("Login ID = ", loginid, ' Password = ', pswd)
                try:
                    check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
                    status = check.status
                    print('Status is = ', status)
                    if status == "activated":
                        request.session['id'] = check.id
                        request.session['loggeduser'] = check.name
                        request.session['loginid'] = loginid
                        request.session['email'] = check.email
                        print("User id At", check.id, status)
                        return render(request, 'users/UserHome.html', {})
                    else:
                        messages.success(request, 'Your Account Not at activated')
                        return render(request, 'UserLogin.html')
                except Exception as e:
                    print('Exception is ', str(e))
                    pass
                messages.success(request, 'Invalid Login id and password')
            return render(request, 'UserLogin.html', {})
        def UserHome(request):
            return render(request, 'users/UserHome.html', {})

        def UserPreProcess(request):
            from .algorithms.DataPreprocess import StartDataPreProcess
            from django.conf import settings
            import pandas as pd
            obj = StartDataPreProcess()
            data = obj.startProcess()
            path = settings.MEDIA_ROOT + "\\" + "train.csv"
            train = pd.read_csv(path)

            df = train.to_html
            return render(request,'users/preprocessdata.html',{'data':df})

        def UserPredictions(request):
            from .algorithms.MyAlgorithm import AlgorithmCode
            obj = AlgorithmCode()
            obj.startAlgo()
            from django.conf import settings
            import pandas as pd
            test = settings.MEDIA_ROOT + "\\" + "test.csv"
            test = pd.read_csv(test)
            test.columns = ['buying_price', 'maintainence_cost', 'number_of_doors', 'number_of_seats', 'luggage_boot_size',
                        'safety_rating']
            pred = settings.MEDIA_ROOT + "\\" + "prediction.csv"
            pred = pd.read_csv(pred)
            pred.columns=['Predictions Results']
            df1 = test.to_html
            df2 = pred.to_html
            return render(request,'users/predictions.html',{'data':df1,'df2':df2})