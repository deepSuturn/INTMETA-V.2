from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
import json
from intmeta.intmetapp import core
from intmeta.intmetapp import subcalls

# Create your views here.

def index(request):
    request.session.clear()
    return render(request, 'index.html')

def kraken(request, uploaded_file2=None):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        attribute = request.POST.get('attributeid')
        savefile = FileSystemStorage()
        # Pega o nome do arquivo
        name = savefile.save(uploaded_file.name, uploaded_file)
        # how we get the current directory
        d = os.getcwd()
        # saving the file in the media directory
        file_directory = d + '/media/' + name
        print("kraken file")
        # Tratamento de erro, modifica o comportamento a cada erro identificado
        try:
            dfd3, dfd3_2, maxpercent, maxreads, total_reads, most_classified_organism = core.kraken(file_directory, attribute)
            request.session['user_data'] = {
                'dfd3': dfd3,
                'dfd3_2': dfd3_2,
                'maxpercent': int(maxpercent),
                'maxreads': int(maxreads),
                'total_reads': int(total_reads),
                'most_classified_organism': most_classified_organism,
                'twofiles': False
            }
            if uploaded_file2 is not None:
                dfd32, dfd3_22, maxpercent2, maxreads2, total_reads2, most_classified_organism2 = core.kraken(file_directory, attribute)
                request.session['user_data']['dfd32'] = dfd32
                request.session['user_data']['twofiles'] = True
        except IndexError:
            return redirect(index)
        except ValueError:
            return redirect(index)
        subcalls.krakenkrona(file_directory)
        return redirect(results)
    return render(request, 'kraken.html')

def clark(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        savefile = FileSystemStorage()
        # pega o nome do arquivo
        name = savefile.save(uploaded_file.name, uploaded_file)
        uploaded_file2 = request.FILES['document2']
        savefile2 = FileSystemStorage()
        # pega o nome do arquivo
        name2 = savefile2.save(uploaded_file2.name, uploaded_file2)
        # how we get the current directory
        d = os.getcwd()
        # saving the file in the media directory
        file_directory = d + '/media/' + name
        # saving the file in the media directory
        file_directory2 = d + '/media/' + name2
        # Tratamento de erro, modifica o comportamento a cada erro identificado
        try:
            dfd3, dfd3_2, maxpercent, maxreads, total_reads = core.clark(file_directory)
            request.session['user_data'] = {
                'dfd3': dfd3,
                'dfd3_2': dfd3_2,
                'maxpercent': int(maxpercent),
                'maxreads': int(maxreads),
                'total_reads': int(total_reads),
                'twofiles': False
            }
        except IndexError:
            return redirect(index)
        except ValueError:
            return redirect(index)
        subcalls.clarkkrona(file_directory2)
        return redirect(results)
    return render(request, 'clark.html')

def metamaps(request):
    return render(request, 'metamaps.html')

def dc(request):
    request.session.clear()
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def krona(request):
    return render(request, 'krona.html')

def results(request):
    user_data = request.session.get('user_data', None)
    if not user_data:
        return redirect(index)
    
    dfd3 = user_data['dfd3']
    dfd3_2 = user_data['dfd3_2']
    maxpercent = user_data['maxpercent']
    maxreads = user_data['maxreads']
    total_reads = user_data['total_reads']
    most_classified_organism = user_data['most_classified_organism']
    dfd3_json = json.dumps(dfd3, indent=4, default=str, ensure_ascii=False)
    dfd3_2 = json.dumps(dfd3_2, indent=4, default=str, ensure_ascii=False)
    print(dfd3_2)
    return render(request, 'results.html', {'dfd3_json': dfd3_json, 'dfd3_2': dfd3_2, 'maxreads': maxreads, 'total_reads': total_reads, 'maxpercent': maxpercent, 'most_classified_organism': most_classified_organism})
