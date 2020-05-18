import time
import vk_api
import random
import wikipedia
import requests
import beat
import bs4
vk = vk_api.VkApi(token='34e79cbc4c66ba3f64a9b5f7fa3f0f3a2f2588cd4fd1a21b5b637b870e9b3434104515c768fa6cdeb0612') 
wikipedia.set_lang("RU")

values = {'out': 0, 'count': 100, 'time_offset': 60}


def write_msg(user_id, message, random_id):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def get_user(user):
    fie_lds = "bdate, city, sex, country, nickname,followers_count, occupation"
    r = vk.method('users.get', {'user_id': user, 'fields': fie_lds})
    print(r[0]['first_name'], r[0]['last_name'])
    nameuser = r[0]['first_name']
    return nameuser


def _clean_all_tag_from_str(string_line):
    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result


def _get_time():
    request = requests.get("https://my-calend.ru/date-and-time-today")
    b = bs4.BeautifulSoup(request.text, "html.parser")
    return _clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]


def check_message(message_in, user):  # ������ input, ��������� output
    message = ' ���� ��� ������������ ���������� ��� ����� ��������, �����������, ���������� ������ ��������. ������ ����������, ��� ��� ���!' \
            '\n�������� "������"'
    nameuser = get_user(user)
    try:
        req = " ".join(message_in.split()[1:])
        message_in = message_in.lower()
        if "/" in message_in:
            if ('������' or '��� �� ������') in message_in:
                message = "� ���� ��� ����, �� ������� ��� ���� �������: " \
                          "\n/����� - ����� ���������� ��������, � ������� �� ������ �������������" \
                          "\n/wiki - ����� ������ �� ��������� �� ������� '/wiki'" \
                          "\n/������ - ��������� ������� ������� � ���������." \
                          "\n/����� - ��������� ������� ����� �� ������� '/�����'" \
                          "\n��� �� �� ������ �� ���� ����������� ���������. ������ �� ����� �����������, ������ ��� ���� � ����� ��� ��� ��. "
            elif "�����" in message_in:
                message = "�������� ������������� � ���� ���������: vk.com/id" + str(
                    random.randrange(1, 432000000))
            elif "wiki" in message_in:
                message = '��� ��� � �����: \n' + str(
                    wikipedia.summary(" ".join(message_in.split()[1:])))
            elif '�����' in message_in:
                message = '������ �����: \n' + str(
                    _get_time())
            else:
                message = nameuser + ", ��������, � ���� ��� ����� �������. ��� ������� ����� ���������� �� ������� '/������'."
        if message_in in ["������", "��������", "������ ����", "������������", "����������"]:
            message = "������������, ������ ������� � ���� " + nameuser
        elif message_in in ["��� ����?", "��� ����", "��� ���������", "��� ����������"]:
            message = nameuser + ", ��� �������, ������� ���� � ��� ��� ���� ������! ����� ��� ��������� ������ � �� ������ �� ���� �������. ��������! "
        elif message_in in ['������ �� �� ������ �� �������', "������ ���� �� ����", "��� �� ����", "������"]:
            message = '���������� ������ �������� � ��� �� ���������, �� ������ ������� � �� ������ ������� ���! �������� ���� ����� ���� � ���� �� ������. '
            # return message, attachment
        elif message_in in ['�����', "���� ���� �� ������", "����� ���� �� ������ �� ������"]:
            message = "�� � �������� � �� 50, �� 70-80 ���� �� ���������� ������. ������ �� ���� ����������� �� �������?"
        elif message_in in ["��", "�������", "�����������", "�����", "����������"]:
            message = '��������� � ���� ��������! ����� ���������� �����... ���� ��� ���������, ������ �������� ����� � ���� ���� ��������) '
        elif message_in in ['����� � ���� ���� ��������', "�����", "����� ���� ��������"]:
            message = ['� ������ �� ������( 30 ������. ������������� ��� ������ �������� ��� � �������� ���������! �����, ����� ��� ��� �������. �� ��������! ']
        elif message_in in ['����','����������','������ ����','�����']:
            message = 'ciao'
        return message
    except Exception:
        pass
            


while True:
    response = vk.method('messages.getConversations', values)
    print(response)
    if response['items']:
        values['last_message_id'] = response['items'][0]['last_message']['id']
    for item in response['items']:
        user = item['last_message'][u'from_id']
        if user > 0:
            print(item)
            rand_id = item['last_message'][u'random_id']
            # nameuser = get_user(user)
            message_in = item['last_message']['text']
            message = check_message(message_in, user)

            write_msg(user, message, rand_id)

    time.sleep(0.5)