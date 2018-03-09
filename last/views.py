import uuid

import datetime
from django.http import HttpResponse
from django.shortcuts import redirect

from core.models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def process(request):
    network_id = request.GET.get('network_id')
    network = Network.objects.get(pk=network_id)
    cookie_name = "network_id_%s" % network_id
    
    redirect_url = None
    cookie_value_must_set = None

    if cookie_name in request.COOKIES:
        cookie_value = request.COOKIES.get(cookie_name)
        if network.redirect_if_duplicate:
            if int(cookie_value) >= network.number_redirect:
                redirect_url = network.redirect_if_duplicate
            else:
                cookie_value_must_set = int(cookie_value) + 1

    else:
        cookie_value_must_set = 1
    
    if redirect_url is None and network.status == 1:
        request_full_url = 'http://media.seniorphp.net' + request.get_full_path()
        ip_address = get_client_ip(request)
        origin  = request.META.get('HTTP_REFERER')
        i = datetime.datetime.now()
        datetime_str = i.strftime('%Y-%m-%d %H:%M:%S')
        date_str = i.strftime('%Y-%m-%d')
        timestamp = i.timestamp()
        timestamp = str(timestamp).split(".")[0]
    
        if origin is None:
            origin = ''
        if "?" not in network.click_url:
            sign_url = '?'
        else:
            sign_url = '&'

        try:
            click = NetworkClick.objects.create(
                log_click_url=request_full_url,
                camp_ip=ip_address,
                camp_time=datetime_str,
                network=network,
                origin=origin,
                time=timestamp,

            )
            click.save()

            go_away_url =  network.click_url + sign_url + 'uid=' + str(click.id)

            if click.id % 10000 == 0:
                unique_phone = uuid.uuid4().int
                report = Report.objects.create(network=network, date=date_str, phone=unique_phone)
                report.save()

            redirect_url = go_away_url
        except Exception as e:
            return HttpResponse(repr(e))
     
    if redirect_url is not None:
        response = redirect(redirect_url)
        if cookie_value_must_set is not None:
            response.set_cookie(cookie_name, cookie_value_must_set, max_age=10000000)
         
        return response    
    

def process_old(request):

    network_id = request.GET.get('network_id')

    request_full_url = 'http://media.seniorphp.net' + request.get_full_path()

    ip_address = get_client_ip(request)

    origin  = request.META.get('HTTP_REFERER')

    i = datetime.datetime.now()

    datetime_str = i.strftime('%Y-%m-%d %H:%M:%S')
    date_str = i.strftime('%Y-%m-%d')

    timestamp = i.timestamp()
    timestamp = str(timestamp).split(".")[0]

    if origin is None:
        origin = ''


    network = Network.objects.get(pk=network_id)

    if "?" not in network.click_url:
        sign_url = '?'
    else:
        sign_url = '&'

    if network.status == 1:
        try:
            click = NetworkClick.objects.create(
                log_click_url=request_full_url,
                camp_ip=ip_address,
                camp_time=datetime_str,
                network=network,
                origin=origin,
                time=timestamp,

            )
            click.save()

            go_away_url =  network.click_url + sign_url + 'uid=' + str(click.id)

            if click.id % 10000 == 0:
                unique_phone = uuid.uuid4().int
                report = Report.objects.create(network=network, date=date_str, phone=unique_phone)
                report.save()

            return redirect(go_away_url)
        except Exception as e:
            return HttpResponse(repr(e))
    else:
        return HttpResponse('Error: Network status is inactive!')


