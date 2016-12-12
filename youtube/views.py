from download import test
from django.http import HttpResponse, JsonResponse
from download.test import find_url, data, ts, parse_stream, stream_data

import json

def test(request):
    da = find_url(data)
    print type(da)
    return JsonResponse(da)

def comp(request):
    res = parse_stream(stream_data)
    print request.META.get('REMOTE_ADDR')
    print type(res)
    return JsonResponse(res)

