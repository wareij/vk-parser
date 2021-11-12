import requests
import time
from config import*


'''
Мой первый с нуля написанный скрипт. Специально писался без использования библиотеки vk_api, дабы было больше возможностей попрактиковаться в программировании.
К сожалению, я на тот момент еще не вникал в работу метода execute.
'''

# Задаем колличество постов, которые проверит скрипт в каждой группе
# (Посты будут проверяться начиная с самых свежих. Максимальное число - 100)
POSTS = 20


# Получам список айдишников и названий сообществ заданного пользователя
def get_groups():
    g_values = {}
    groups = (requests.get(S_URL + 'groups.get', params={'extended': 1, 'user_id': USER_ID,'access_token': ACCESS_TOKEN, 'v': 5.131})).json()    
    groups = groups['response']['items']
    for i in groups:
        g_values[i['id']] = i['screen_name']

    return g_values

# Получаем списки лайков заданного пользователя по сообществам
def get_likes(g_values):
    change_id = ('-' + str(g_values[0]))
    likes = []
    try:
        for i in range(POSTS):
            post = (requests.get(S_URL + 'wall.get', params={'offset': i, 'owner_id': change_id, 'count': 1,
                                                             'access_token': ACCESS_TOKEN, 'v': 5.131})).json()
            post_id = post['response']['items'][0]['id'] 
            time.sleep(0.2)

            like = (requests.get(S_URL + 'likes.isLiked', params={'user_id': USER_ID, 'type': 'post', 'owner_id': change_id,
                                                                 'item_id': post_id, 'access_token': ACCESS_TOKEN, 'v': 5.131})).json()
            like = like['response']['liked']

            if like == 1:
                likes.append(f'https://vk.com/{g_values[1]}?w=wall{change_id}_{post_id}')
            else:
                likes.append(like)
            time.sleep(0.2)
    except:
        None
        
    return likes    

def calc():
    for i in get_groups().items():        
        print(i)
        print(get_likes(i))
        time.sleep(0.2)        

def main():    
    calc()
   
if __name__ == '__main__':
    main()