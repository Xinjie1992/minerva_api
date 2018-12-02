# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from minerva.models import Build,App


@require_http_methods(["GET"])
def addApp(req):
    app_name = req.GET.get('appName')
    if not app_name:
        resp = {"hasError": "true", "message": "缺少应用名!"}
    elif (App.objects.filter(app_name=app_name).count() >= 1):
        resp = {"hasError": "true", "message": "应用已存在!"}
    else:
        App(app_name=app_name).save()
        resp = {"hasError": "false", "message": "success"}
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["GET"])
def getApp(req):
    list = App.objects.all()
    data = serializers.serialize("json", list)
    return HttpResponse(data)


@require_http_methods(["GET"])
def addBuild(req):
    image =  req.GET.get('image')
    app_name = req.GET.get('appName')
    commit = req.GET.get('commit')
    if not req.GET.get('commit'):
        commit = None
    if not image:
        resp = {"hasError": "true", "message": "缺少镜像名!"}
    elif not app_name or App.objects.filter(app_name=app_name).count() < 1:
        resp = {"hasError": "true", "message": "应用名不存在!"}
    else:
        Build(image=image, app_name=app_name, commit=commit).save()
        resp = {"hasError":"false","message":"success"}
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["GET"])
def getBuild(req):
    app_name = req.GET.get('appName')
    if not app_name:
        list = Build.objects.all()
        data = serializers.serialize("json", list)
        return HttpResponse(data)
    else:
        list = Build.objects.filter(app_name=app_name)
        data = serializers.serialize("json", list)
        return HttpResponse(data)

