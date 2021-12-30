from django.shortcuts import render
from . import distance as ds
# Create your views here.

def result(request): 
    locList = request.POST.get('inpLocation')
    print("the loclIst is", locList)
    locList = locList.split(', ')
    print(locList)
    locList = [i.strip() for i in locList if i!= ""]
    
    path, minDistance, Map = ds.getPath(locList)
    print(path)
    strPath = "  =>  ".join(path.split(', '))
    return render(request, 'Path.html', {"path": strPath, "minDistance": minDistance, "Map": Map})