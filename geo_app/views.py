from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import UploadDetailsForm
from .models import Details, Coordinates, CountAnn
from datetime import datetime


def get_time_range(objs):

    """Returns The Lowest time bound , and Highest time bounds for filtering in frontend."""

    start_dates = set()
    end_dates = set()
    for obj in objs:
        start_dates.add(int(str(obj.project_start_time).split('-')[0]))
        end_dates.add(int(str(obj.project_completion_time).split('-')[0]))

    return sorted(start_dates), sorted(end_dates)


def home(request):

    """Main Driver Function for User data visualization and filtering with necessary information."""
    if not request.user.is_authenticated:
        cnt = CountAnn.objects.get(id=1)
        cnt.count += 1
        cnt.save()


    details = []
    category = {}
    start_dates, end_dates = get_time_range(Details.objects.all())
    i = 0

    for data in Details.objects.all():  # Getting details and category
        try:
            category[data.category].append(i)
        except:
            category[data.category] = [i]
        i += 1
        details.append(data)

    # When request  is POST

    if request.method == 'POST':    # When we filter in frontend it will send an POST request to backend

        filtered_details = []
        final_f_details = []
        if request.POST['category'] == '':
            for data in details:
                filtered_details.append([data.project_name, data.id,  int(str(data.project_start_time).split('-')[0]),
                                         int(str(data.project_completion_time).split('-')[0])])
        else:
            for idx in category[request.POST['category']]:
                d_p = details[idx]
                filtered_details.append([d_p.project_name, d_p.id, int(str(d_p.project_start_time).split('-')[0]),
                                         int(str(d_p.project_completion_time).split('-')[0])])

        # Conditions for time range based filtering

        srt_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if srt_date != '' and end_date != '':
            for data in filtered_details:
                if data[2] >= int(srt_date) and data[3] <= int(end_date):
                    final_f_details.append(data)
        elif srt_date != '':
            for data in filtered_details:
                if data[2] >= int(srt_date):
                    final_f_details.append(data)
        elif end_date != '':
            for data in filtered_details:
                if data[3] <= int(end_date):
                    final_f_details.append(data)
        else:
            final_f_details = filtered_details

        data = {
            'details': final_f_details,
        }
        return JsonResponse(data)

    # When request is GET

    context = {
        'details': details,
        'category': category,
        'start_dates': start_dates,
        'end_dates': end_dates
    }
    return render(request, 'home.html', context)


def get_percentage_amount_time(data):

    """This function calculates remaining time percentage against (end time - curr working days)"""

    start_date = datetime.strptime(str(data.project_start_time), '%Y-%m-%d')
    end_date = datetime.strptime(str(data.project_completion_time), '%Y-%m-%d')
    est_days = (end_date - start_date).days
    curr_date = datetime.now()

    time_remaining = (end_date - curr_date).days / est_days * 100
    return round(time_remaining, 2) if time_remaining > 0 else 0


def get_details(request):

    """This Function will return the Project details along with location data in a viewable format."""

    if request.method == 'POST':    # When request is POST then we'll return coordinates and project details
        dp = Details.objects.get(id=int(request.POST['project_id']))
        dt = datetime.strptime(f'{dp.project_start_time}', '%Y-%m-%d')
        dt2 = datetime.strptime(f'{dp.project_completion_time}', '%Y-%m-%d')
        project = [dp.project_name, dp.category, dp.affiliated_agency, dp.description, dt.strftime('%d %B, %Y'),
                   dt2.strftime('%d %B, %Y'), f'<b>JPY  {dp.total_budget} Million</b>', f'<b>{dp.completion_percentage} %</b>',
                   dp.id]

        coordinates = [[c.lng, c.lat] for c in dp.coordinates_set.all()]
        pct_time = f'<b>{get_percentage_amount_time(dp)} % </b>   [Based on Estimated Date and Completed Days]'
        l_c = len(coordinates)
        data = {
            'project': project,
            'coordinates': coordinates,
            'l_c': l_c,
            'pct_time': pct_time
        }
        return JsonResponse(data)

# Excluded
# This function is excluded right now , because of the csv file format


def upload_details(request):

    """ This view uploads a details files , but we will not use it , because the dataset given is not valid.
        By invalid means when we try parse the data by csv delimiter it parses commas inside quotes."""
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            form = UploadDetailsForm(request.POST, request.FILES)

            if form.is_valid():
                up_file = request.FILES['file']

                file_data = up_file.read().decode("utf-8")
                csv_data = file_data.split("\n")
                exclude = csv_data.pop(0).split(',')
                print(exclude)
                form.save()

                for data in csv_data:
                    """Saving the data sequence, will start from here"""

                    d = data.split(',')
                    obj = Details(
                        category=d[0], affiliated_agency=d[1], description=d[2], project_start_time=d[3],
                        project_completion_time=d[4], total_budget=d[5], completion_percentage=d[6]
                    )
                    obj.save()

                    # Section for upload multiple coordinates
                    coordinates = d[7].split('-')

                return HttpResponse("<p style='font-size:25px; text-align:center;"
                                    " margin-top:20%;'> Uploaded File Successfully </p>")

        else:
            return render(request, 'upload-files.html')
    return redirect('home')


# End Excluded

def issue_form(request):

    """This one stores issues of a particular ongoing project, and counts it."""

    if request.method == 'POST':    # When request is POST
        det = Details.objects.get(id=int(request.POST['id']))   # Get details object from database
        det.issue_set.create(issue=request.POST['issue'])   # Create Issue for the details
        det.issue_count += 1    # And increase the count of issues for this details object
        det.save()  # Finally save
    return HttpResponse('Success')  # This line doesn't make any sense


def admin(request):

    """View specially for admin users, admin can search a project
        by title, agency or sort them by count of issues they have"""
    if request.user.is_authenticated and request.user.is_superuser:

        if request.method == 'POST':
            key = request.POST['keyword']
            if key == '' and 'sort' in request.POST:
                result = sorted(Details.objects.all(), key=lambda x: x.issue_count, reverse=True)   # Sorting by issue

            elif key != '' and 'sort' in request.POST:
                data_points = Details.objects.filter(
                    Q(project_name__startswith=key) | Q(affiliated_agency__startswith=key)
                )
                result = sorted(data_points, key=lambda x: x.issue_count, reverse=True)
            else:
                result = Details.objects.filter(
                    Q(project_name__startswith=key) | Q(affiliated_agency__startswith=key)
                )
            final_result = []
            for data in result:
                final_result.append([data.project_name, data.id, data.issue_count])

            data = {
                'projects': final_result
            }
            return JsonResponse(data)

        return render(request, 'admin-page.html')
    return redirect('home')


def get_admin_vizes(request):

    """Returns Map Geo Location for given  coordinates"""

    if request.method == 'POST':
        dp = Details.objects.get(id=int(request.POST['id']))
        coordinates = [[c.lng, c.lat] for c in dp.coordinates_set.all()]
        l_c = len(coordinates)
        data = {
            'coordinates': coordinates,
            'l_c': l_c
        }
        return JsonResponse(data)
