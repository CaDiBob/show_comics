# Публикация комиксов

Скрипт скачивает комиксы [xkcd](https://xkcd.com/) и публикует их в вашей группе [ВКонтакте](https://vk.com/).

Для работы скрипта нужно [создать группу в ВКонтакте](https://vk.com/groups?tab=admin).

Для постинга на стену нужен ключ доступа пользователя. Чтобы его получить, [нужно создать приложение с типом standalone](https://vk.com/dev) — это подходящий тип для приложений, которые просто запускаются на компьютере. Поcле как создали приложение можно перейти к процедуре получения ключа к [API ВКонтакте](https://vk.com/dev/implicit_flow_user), для постинга на стену достаточно этих прав: `photos, groups, wall и offline`.

Все чувствительные данные прячем в `.env` файл.

`VK_GROUP_ID`=id вашей группы в ВК можно узнать [здесь](https://regvk.com/id/).

`VK_APP_ID`=client_id вашего приложения можно узнать на [странице вашего приложения в разделе настроек](https://vk.com/apps?act=manage).

`VK_ACCESS_TOKEN`= ваш ключ к [API ВКонтакте](https://vk.com/dev/implicit_flow_user).

### Как установить

Python3 должен быть установлен, затем используйте `pip`:

```bash
pip install -r requirements.txt
```
### Как запустить

```bash
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).