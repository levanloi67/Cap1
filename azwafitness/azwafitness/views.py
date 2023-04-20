from .model_classification import Model_Classification
from django.http import JsonResponse
import numpy as np
from django.views.decorators.csrf import csrf_exempt

# POST
@csrf_exempt
def predict(request):
    if request.method == "POST":
        data = request.POST.get("data")
        data = data.split(",")
        # data = [gender, weight, height]
        data = list(map(float, data))
        data = np.array(data).reshape(1, -1)#
        result = Model_Classification.get_instance().predict(data)
        result = result[0]
        # Day la the hinh cua nguoi ma m muon tim
        result = Model_Classification.get_instance().get_classes()[result]
        return JsonResponse({"result": result})
    return JsonResponse({"result": "fail"}) 