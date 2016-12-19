from django.shortcuts import render, render_to_response, RequestContext, redirect
from tensorflow1.newmodel import getScore
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os, subprocess, urllib
# Create your views here.

def home(request):
    if request.method == 'POST':
        files = request.FILES.getlist('myfile')
        allBuckets = ""
        unknowns = ""
        for i in files:
            myfile = i
            fs = FileSystemStorage()
            filename = fs.save('uploads/' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            
            knowClass = getScore(filename)
            allBuckets += knowClass + " "
            
            if knowClass == '':
                # return redirect("/retrain")
                unknowns += filename + ", "
            else:
                fname = filename.replace("uploads/","")
                if os.path.isfile("tf_files/animals/"+knowClass+"/"+fname):
                    os.rename("tf_files/animals/"+knowClass+"/"+fname,"tf_files/animals/"+knowClass+"/1"+fname )
                else:
                    os.rename(filename,"tf_files/animals/"+knowClass+"/"+fname )

        allBuckets = allBuckets.replace(" ", ", ")
        allBuckets = allBuckets[:-2]
        unknowns = unknowns[:-2].replace('uploads/','')
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url,
            'knowClass': knowClass,
            'allBuckets' : allBuckets,
            'unknowns' : unknowns
        })
        
    return render(request, 'index.html')

def retrain(request):
    if request.method == 'POST':
        directory = request.POST.get('foldername', None)
        if not os.path.exists("tf_files/animals/"+directory):
            os.makedirs("tf_files/animals/"+directory)
        files = request.FILES.getlist("upload")
        foldername = "tf_files/animals/" + directory + "/"
        for x, i in enumerate(files):
            upload = i
            fs = FileSystemStorage()
            filename = fs.save(foldername + upload.name, upload)
        retrainpy = "tensorflow\examples\image_retraining\\"
        exfile = "retrain.py " 
        params = " --bottleneck_dir=tf_files\\bottlenecks --how_many_training_steps 500 --model_dir=tf_files\inception --output_graph=tf_files\retrained_graph.pb --output_labels=tf_files\retrained_labels.txt --image_dir tf_files\animals"
        os.system("retrain.bat")
        Training_Complete = 'Training_Complete'
        return render(request, 'CreateNewclass.html', {
            'Training_Complete' : Training_Complete
        })       
    return render(request, 'CreateNewclass.html')
