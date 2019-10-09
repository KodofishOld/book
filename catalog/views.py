from django.shortcuts import render
import catalog.trainTicket as myhome
# Create your views here.

def book(request):
    ticket = '-1111'
    if request.method == 'POST':
        start = request.POST['start']
        end = request.POST['end']
        ticket = request.POST['ticket']
        info = ""
        a = myhome.inputByWebInit()
        for i in range(int(ticket)):
            info = info + myhome.inputByWeb(a, start, end)
            info = info + '<br/>' + '<br/>'

        return printf(request, ticket, start, end,info)
    return render(request, 'order.html', locals())



def printf(request, ticket, start, end,info):
    print('ticket number = %d' %int(ticket))
    st = int(ticket)
    sr = str(start)
    se = str(end)
    sw = str(info)
    return render(request, 'ok.html', locals())