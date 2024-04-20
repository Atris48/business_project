from ghasedakpack import ghasedakpack

GHASEDAK_API = 'd9003bb6bd3e7f7e654465257d539a8712a885b210761c98ce8cd44776009782'
SMS = ghasedakpack.Ghasedak(GHASEDAK_API)


def send_sms(phone, template, parm1, parm2=None):
    if parm2 != None:
        SMS.verification({'receptor': phone, 'type': '1', 'template': template, 'param1': parm1, 'param2': parm2})
    else:
        SMS.verification({'receptor': phone, 'type': '1', 'template': template, 'param1': parm1})
