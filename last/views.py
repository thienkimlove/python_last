import json
import uuid

from user_agents import parse
import datetime

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render

from core.models import *
from last.settings import LOG_FILE
from urllib.parse import unquote


def debug(msg):
    with open(LOG_FILE, 'r') as original: data = original.read()
    with open(LOG_FILE, 'w') as modified: modified.write(data + str(repr(msg)) + "\n")


def test_sms(request):
    number = request.GET.get('num')
    text = request.GET.get('text')
    if number and text:
        text = unquote(unquote(text))
        user_agent = parse(request.META['HTTP_USER_AGENT'])

        if 'ios' in user_agent.os.family.lower():
            response = "sms:/%s/&body=%s" % (number, text)
        else:
            response = "sms:%s?body=%s" % (number, text)
        return render(request, 'core/redirect.html', {'sms_url': response})


def pass_click(d, index, network_id, request):
    check_ip_pass = True
    check_number = True

    allow_ips = d['allow_ip']

    if allow_ips:
        check_ip_pass = False
        ip_address = get_client_ip(request)
        ip_address = ip_address.split('.')
        for allow_ip in allow_ips.split(','):
            allow_ip = allow_ip.strip()
            ip_rule = allow_ip.split('.')
            if (ip_rule[0] == '*' or ip_rule[0] == ip_address[0]) and (
                    ip_rule[1] == '*' or ip_rule[1] == ip_address[1]):
                check_ip_pass = True

    # if d['number_click_per_minute'] is not None and int(d['number_click_per_minute']) > 0:
    #     check_number = False
    #     i = datetime.datetime.now()
    #     datetime_str_to_minute = i.strftime('%Y%m%d%H%M')
    #     cache_key = str(network_id) + '_' + str(index) + '_' + str(datetime_str_to_minute)
    #
    #     if cache.get(cache_key) is not None:
    #         current_cache = cache.get(cache_key)
    #         if int(current_cache) < int(d['number_click_per_minute']):
    #             check_number = True
    #             cache.incr(cache_key)
    #     else:
    #         check_number = True
    #         cache.delete_pattern(str(network_id) + "_" + str(index) + '_*')
    #         cache.set(cache_key, 1)

    return check_number and check_ip_pass


def get_click_url(network, request):
    network_urls = json.loads(network.click_url)

    index = -1
    for d in network_urls:
        index = index + 1
        if d['click_url'] and pass_click(d, index, network.id, request):
            return {'link_id': int(d['link_id']), 'url': str(d['click_url'])}

    return {'link_id': 0, 'url': 'http://media.seniorphp.net'}


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

    response_url = get_click_url(network, request)

    network_click_url = response_url.get('url')
    network_link_id = response_url.get('link_id')

    if cookie_name in request.COOKIES:
        cookie_value = request.COOKIES.get(cookie_name)
        if network.redirect_if_duplicate:
            if int(cookie_value) >= network.number_redirect:
                redirect_url = network.redirect_if_duplicate
            else:
                cookie_value_must_set = int(cookie_value) + 1

    else:
        cookie_value_must_set = 1

    real_redirect = False

    if redirect_url is None and network.status == 1:
        request_full_url = 'http://media.seniorphp.net' + request.get_full_path()
        ip_address = get_client_ip(request)
        origin = request.META.get('HTTP_REFERER')
        user_agent = request.META.get('HTTP_USER_AGENT')
        i = datetime.datetime.now()
        datetime_str = i.strftime('%Y-%m-%d %H:%M:%S')
        date_str = i.strftime('%Y-%m-%d')
        timestamp = i.timestamp()
        timestamp = str(timestamp).split(".")[0]

        not_allow_because_miss_header = False

        if network.must_set_header == 1:
            if origin is None or user_agent is None:
                not_allow_because_miss_header = True

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
                origin='not_allow_because_miss_header' if not_allow_because_miss_header else origin,
                time=timestamp,

            )
            click.save()

            go_away_url = network_click_url + sign_url + 'uid=' + str(click.id)

            if network.auto == 1 and click.id % 10000 == 0:
                unique_phone = uuid.uuid4().int
                report = Report.objects.create(network=network, date=date_str, phone=unique_phone)
                report.save()

            real_redirect = True
            if not_allow_because_miss_header is False:
                redirect_url = go_away_url
            else:
                redirect_url = None
        except Exception as e:
            return HttpResponse(repr(e))

    if redirect_url is not None:

        response = redirect(redirect_url)
        # here we start redirect.
        if real_redirect and network_link_id != 0:
            i = datetime.datetime.now()
            datetime_str_to_minute = i.strftime('%Y%m%d%H%M')
            try:
                obj = Traffic.objects.get(network=network, link_id=network_link_id, minute=int(datetime_str_to_minute))
                obj.click = F('click') + 1
                obj.save()
            except Traffic.DoesNotExist:
                Traffic.objects.create(network=network, link_id=network_link_id, minute=int(datetime_str_to_minute),
                                       click=1)

        if cookie_value_must_set is not None:
            response.set_cookie(cookie_name, cookie_value_must_set, max_age=10000000)

        return response
