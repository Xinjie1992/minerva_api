# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.db.models import Q
from minerva.models import Build,App,Version,Relation


@require_http_methods(["GET"])
def addApp(req):
    app_name = req.GET.get('appName')
    if not app_name:
        resp = {"hasError": "true", "message": "缺少应用名!"}
    elif (App.objects.filter(app_name=app_name).count() >= 1):
        resp = {"hasError": "true", "message": "应用已存在!"}
    else:
        App(app_name=app_name).save()
        appId = App.objects.only('id').get(app_name=app_name)
        data = {"id":str(appId.id),"app_name":app_name}
        resp = {"hasError": "false", "message":data }
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
        for item in list:
            print(item.__dict__)
        data = serializers.serialize("json", list)
        return HttpResponse(data)
    else:
        list = Build.objects.filter(app_name=app_name)
        data = serializers.serialize("json", list)
        return HttpResponse(data)


@require_http_methods(["GET"])
def getVersion(req):
    list = Version.objects.filter(Q(is_delete='N')|Q(is_delete='n'))
    data = serializers.serialize("json", list)
    return HttpResponse(data)

@require_http_methods(["GET"])
def addVersion(req):
    version_name = req.GET.get('version')
    if not version_name:
        resp = {"hasError": "true", "message": "缺少版本号!"}
    elif (Version.objects.filter(Q(version=version_name),Q(is_delete='N')|Q(is_delete='n')).count() >= 1):
        resp = {"hasError": "true", "message": "版本号已存在!"}
    else:
        Version(version=version_name).save()
        versionId = Version.objects.only('id').get(Q(version=version_name),Q(is_delete='N')|Q(is_delete='n'))
        data = {"id": str(versionId.id), "version": version_name}
        resp = {"hasError": "false", "message": data}
    return HttpResponse(json.dumps(resp), content_type="application/json")

@require_http_methods(["POST"])
def setVersion(req):
    postBody = req.body
    json_result = json.loads(postBody)
    print(json_result)
    versionId = json_result['versionId']
    appId = json_result['appId']
    Relation.objects.filter(version_id=versionId).delete()
    for item in appId:
        Relation(version_id=versionId,app_id=item).save()
    list = Relation.objects.filter(version_id=versionId)
    data = serializers.serialize("json", list)
    resp = {"hasError": "false", "message": data}
    return HttpResponse(json.dumps(resp), content_type="application/json")
