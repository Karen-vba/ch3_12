from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.
def search_list(request):
    if "cName" in request.GET:
        cName=request.GET["cName"]
        print(cName)
        result_list=students.objects.filter(cName__contains=cName)
    else:
        result_list=students.objects.all()
    
    error_message=""
    if not result_list:
        error_message="無此資料"
    

    #測試資料是否正確(開發人員使用)
    # for data in result_list:
    #     print(model_to_dict(data))


    # return HttpResponse("Hello")
    return render(request,"search_list.html",locals())

def index(request): 
    if "site_search" in request.GET:
        site_search=request.GET["site_search"]
        site_search=site_search.strip()  #去前後空白
        # print(site_search)
        #一個關鍵字,搜尋一個欄位
        # result_list=students.objects.filter(cName__contains=site_search)
        #一個關鍵字,搜尋多個欄位
        # result_list=students.objects.filter(
        #     Q(cName__contains=site_search)|
        #     Q(cEmail__contains=site_search)|
        #     Q(cBirthday__contains=site_search)|
        #     Q(cAddr__contains=site_search)|
        #     Q(cPhone__contains=site_search)
        # )
        #多個關鍵字,多個欄位
        keywords=site_search.split() #以空格切割
        print(keywords)
        # result_list=[]
        q_object=Q()
        for keyword in keywords:
            q_object.add(Q(cName__contains=keyword),Q.OR)
            q_object.add(Q(cEmail__contains=keyword),Q.OR)
            q_object.add(Q(cBirthday__contains=keyword),Q.OR)
            q_object.add(Q(cAddr__contains=keyword),Q.OR)
            q_object.add(Q(cPhone__contains=keyword),Q.OR)
        result_list=students.objects.filter(q_object)
    else:
        result_list=students.objects.all().order_by("cID")
    dataCount=len(result_list)
    status=True
    errormessage=""
    if not result_list:
        status=False
        errormessage="無此資料"
    
    paginator=Paginator(result_list,1)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number) #依據取得的page_number,得到對應的頁數的資料
    #page_obj包含該頁的資料的物件
    #page_obj.object_list該頁的資料
    #page_obj.has_next,page_obj.has_previous:是否有下一頁或上一頁
    #page_obj.next_page_number,page_obj.previous_page_number:上一頁,下一頁的頁碼
    #page_obj.number目前的頁碼
    #page_obj.paginator.num_pages:總頁數
    
    #分頁設定,每頁顯示3筆

    # print(dataCount)
    # return HttpResponse("Hello")
    return render(request,"index.html",locals())


def post(request):
    if request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr},")
        #orm
        add=students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        # return HttpResponse("Hello")
        return redirect("/index/")
    else:
        return render(request,"post.html",locals())

def edit(request,id=None):    
    print(f"id={id}")
    if request.method == "POST":
        cName=request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr},")
        #orm
        update=students.objects.get(cID=id)
        update.cName=cName
        update.cSex=cSex
        update.cBirthday=cBirthday
        update.cEmail=cEmail
        update.cPhone=cPhone
        update.cAddr=cAddr
        update.save()
        # return HttpResponse("Hello")
        return redirect("/index/")
    else:
        obj_data=students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"edit.html",locals())

def delete(request,id=None):
    print(f"id={id}")
    if request.method == "POST":
        delete_data=students.objects.get(cID=id)
        delete_data.delete()
        # return HttpResponse("Hello")
        return redirect("/index/")
    else:
        obj_data=students.objects.get(cID=id)
        print(model_to_dict(obj_data))        
        return render(request,"delete.html",locals())

def getallitems(request):
    result_list_object=students.objects.all()  #叫出所有資料
    # for data in result_list_object:
    #     print(model_to_dict(data))  #將資料轉成字典型別並輸出

    #querySet->object轉成list->dict
    result_list_dict=list(result_list_object.values())
    # print(result_list_dict)
    return JsonResponse(result_list_dict,safe=False)

def getitem(request,id=None):
    print(f"id={id}")
    result_list_object=students.objects.filter(cID=id)
    if not result_list_object.exists():
        return JsonResponse({"message":"無資料"})
    result_list_dict=list(result_list_object.values())
    # print(result_list_dict)
    return JsonResponse(result_list_dict,safe=False)

    # return HttpResponse("Hello")
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def createItem(request):
    try:
        if request.method == "GET":
            cName=request.GET["cName"]
            cSex=request.GET["cSex"]
            cBirthday=request.GET["cBirthday"]
            cEmail=request.GET["cEmail"]
            cPhone=request.GET["cPhone"]
            cAddr=request.GET["cAddr"]
            print("GET------------------")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName=request.POST["cName"]
            cSex=request.POST["cSex"]
            cBirthday=request.POST["cBirthday"]
            cEmail=request.POST["cEmail"]
            cPhone=request.POST["cPhone"]
            cAddr=request.POST["cAddr"]
            print("POST------------------")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
    except:
        return JsonResponse({"message":"缺少資料"})
    try:
    #orm
        add=students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save() 
        return JsonResponse({"message":"新增成功"})
    except:
        return JsonResponse({"message":"新增失敗"})
    

@csrf_exempt
def  updateItem(request,id=None):
    print(id)
    try:
        if request.method == "GET":
            cName=request.GET["cName"]
            cSex=request.GET["cSex"]
            cBirthday=request.GET["cBirthday"]
            cEmail=request.GET["cEmail"]
            cPhone=request.GET["cPhone"]
            cAddr=request.GET["cAddr"]
            print("GET------------------")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
        elif request.method == "POST":
            cName=request.POST["cName"]
            cSex=request.POST["cSex"]
            cBirthday=request.POST["cBirthday"]
            cEmail=request.POST["cEmail"]
            cPhone=request.POST["cPhone"]
            cAddr=request.POST["cAddr"]
            print("POST------------------")
            print(f"cName={cName},cSex={cSex},cBirthday={cBirthday},"+
                f"cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
    except:
        return JsonResponse({"message":"缺少資料"})
    try:
        #orm
        update=students.objects.get(cID=id)
        update.cName=cName
        update.cSex=cSex
        update.cBirthday=cBirthday
        update.cEmail=cEmail
        update.cPhone=cPhone
        update.cAddr=cAddr
        update.save()
        return JsonResponse({"message":"更新成功"})
    except:
        return JsonResponse({"message":"更新失敗"})
    
    # return HttpResponse("hello")

@csrf_exempt
def deleteItem(request,id=None):    
    print(id)
    try:
        delete_data=students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"刪除成功"})
    except:
        return JsonResponse({"message":"刪除失敗"})

    # return HttpResponse("hello")





        

    




    