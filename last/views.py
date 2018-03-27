import json
import uuid

import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.cache import cache

from core.models import *
from last.settings import LOG_FILE


def debug(msg):
    with open(LOG_FILE, 'r') as original: data = original.read()
    with open(LOG_FILE, 'w') as modified: modified.write(data +str(repr(msg))+"\n")

def pass_click(d, index, network_id, request):
    check_ip_pass = True
    check_number = True

    if d['allow_ip'] is not None:
        check_ip_pass = False
        ip_address = get_client_ip(request)
        ip_address = ip_address.split('.')
        for allow_ip in  d['allow_ip'].split(','):
            allow_ip = allow_ip.strip()
            ip_rule = allow_ip.split('.')
            if (ip_rule[0] == '*' or ip_rule[0] == ip_address[0]) and (ip_rule[1] == '*' or ip_rule[1] == ip_address[1]):
                check_ip_pass = True


    if d['number_click_per_minute'] is not None and int(d['number_click_per_minute']) > 0:
        check_number = False
        i = datetime.datetime.now()
        datetime_str_to_minute = i.strftime('%Y%m%d%H%M')
        cache_key = str(network_id) + '_' + str(index) + '_' + str(datetime_str_to_minute)

        if cache.get(cache_key) is not None:
            current_cache = cache.get(cache_key)
            if int(current_cache) < int(d['number_click_per_minute']):
                check_number = True
                cache.incr(cache_key)
        else:
            check_number = True
            cache.delete_pattern(str(network_id) + "_" + str(index) + '_*')
            cache.set(cache_key, 1)


    return check_number and check_ip_pass

def get_click_url(network, request):

    network_urls = json.loads(network.click_url)

    index = -1
    for d in network_urls:
        index = index + 1
        if d['click_url'] is not None and pass_click(d, index, network.id, request):
            return str(d['click_url'])

    return 'http://media.seniorphp.net'


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

    network_click_url = get_click_url(network, request)

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
        if "?" not in network_click_url:
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

            go_away_url =  network_click_url + sign_url + 'uid=' + str(click.id)

            if network.auto == 1 and click.id % 10000 == 0:
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


