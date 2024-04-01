import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from steps.models import User, Steps

@csrf_exempt
def userAPI(request):
    user = User.exist(request)
    print(user)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    return JsonResponse(data=model_to_dict(user), status=200, safe=False)

@csrf_exempt
def dashboardAPI(request):
    user = User.exist(request)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    return JsonResponse(data=list(Steps.get_dash_data()), status=200, safe=False)

@csrf_exempt
def selfDashboardAPI(request):
    user = User.exist(request)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    steps = Steps.objects.filter(user__id=user.id).order_by('-added_at').values()
    return JsonResponse(data=list(steps), status=200, safe=False)

@csrf_exempt
def deleteStepAPI(request, pk):
    user = User.exist(request)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    if request.method == "DELETE":
        Steps.objects.filter(id=pk, user__id=user.id).delete()
        steps = Steps.objects.filter(user__id=user.id).order_by('-added_at').values()
        return JsonResponse(data=list(steps), status=200, safe=False)

@csrf_exempt
def createStepAPI(request):
    user = User.exist(request)
    if not user:
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            new_steps = Steps(user=user, steps=data['steps'])
            new_steps.save()
            steps = Steps.objects.filter(user__id=user.id).order_by('-added_at').values()
            return JsonResponse(data=list(steps), status=200, safe=False)
        except:
            return HttpResponse('Some error ocurred, try again later', status=400)
        