import urllib.error
from os.path import getsize
from re import IGNORECASE, MULTILINE, sub

from bs4 import BeautifulSoup
from loguru import logger as log
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo
from vk_api import exceptions
from vk_api.audio import VkAudio
from wget import download

from TG_AutoPoster.tools import add_audio_tags, build_menu, start_process

MAX_FILENAME_LENGTH = 255
DOMAIN_REGEX = r"https://(m\.)?vk\.com/"


class VkPostParser:
    def __init__(self, post, domain, session, sign_posts=False, what_to_parse=None):
        self.session = session
        try:
            self.audio_session = VkAudio(session)
        except IndexError:
            self.audio_session = None
        self.sign_posts = sign_posts
        self.pattern = "@" + sub(DOMAIN_REGEX, "", domain)
        self.raw_post = post
        self.post_url = "https://vk.com/wall{owner_id}_{id}".format(**self.raw_post)
        self.text = ""
        self.user = None
        self.repost = None
        self.repost_source = None
        self.reply_markup = None
        self.media = []
        self.docs = []
        self.tracks = []
        self.poll = None
        self.attachments_types = []
        self.what_to_parse = what_to_parse if what_to_parse else {"all"}

    def generate_post(self):
        log.info("[AP] Парсинг поста.")
        if self.what_to_parse.intersection({"text", "all"}):
            self.generate_text()

        if "attachments" in self.raw_post:
            self.attachments_types = tuple(x["type"] for x in self.raw_post["attachments"])
            for attachment in self.raw_post["attachments"]:
                if attachment["type"] in ["link", "page", "album"] and self.what_to_parse.intersection({"link", "all"}):
                    self.generate_link(attachment)
                if attachment["type"] == "photo" and self.what_to_parse.intersection({"photo", "all"}):
                    self.generate_photo(attachment)
                if attachment["type"] == "video" and self.what_to_parse.intersection({"video", "all"}):
                    self.generate_video(attachment)
                if attachment["type"] == "doc" and self.what_to_parse.intersection({"doc", "all"}):
                    self.generate_doc(attachment)
                if attachment["type"] == "poll" and self.what_to_parse.intersection({"polls", "all"}):
                    self.generate_poll(attachment)
            if self.what_to_parse.intersection({"music", "all"}):
                self.generate_music()

        if self.sign_posts:
            self.generate_user()
            self.sign_post()

    def generate_text(self):
        if self.raw_post["text"]:
            log.info("[AP] Обнаружен текст. Извлечение.")
            self.text += self.raw_post["text"] + "\n"
            if self.pattern != "@":
                self.text = sub(self.pattern, "", self.text, flags=IGNORECASE)
            self.text = self.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            self.text = sub(r"\[(.*?)\|(.*?)\]", r'<a href="https://vk.com/\1">\2</a>', self.text, flags=MULTILINE)

    def generate_link(self, attachment):
        log.info("[AP] Парсинг ссылки...")
        if attachment["type"] == "link" and attachment["link"]["title"]:
            log.debug("Detected link. Adding to message")
            self.text += '\n🔗 <a href="{url}">{title}</a>'.format(**attachment["link"])
        elif attachment["type"] == "page":
            log.debug("Detected wiki page. Adding to message")
            self.text += '\n🔗 <a href="{view_url}">{title}</a>\n👁 {views} раз(а)'.format(**attachment["page"])
        elif attachment["type"] == "album":
            log.debug("Detected album. Adding to message")
            self.text += (
                '\n🖼 <a href="https://vk.com/album{owner_id}_{id}">'
                "Альбом с фотографиями: {title}</a>\n"
                "Описание: {description}".format(**attachment["album"])
            )

    def generate_photo(self, attachment):
        photo = None
        for i in attachment["photo"]["sizes"]:
            photo = i["url"]
        photo = download(photo, bar=None)
        if photo:
            self.media.append(InputMediaPhoto(photo))

    def generate_doc(self, attachment):
        try:
            attachment["doc"]["title"] = sub(r"[/\\:*?\"><|]", "", attachment["doc"]["title"])
            if attachment["doc"]["title"].endswith(attachment["doc"]["ext"]):
                doc = download(attachment["doc"]["url"], out="{title}".format(**attachment["doc"]))
            else:
                doc = download(attachment["doc"]["url"], out="{title}.{ext}".format(**attachment["doc"]))
            self.docs.append(doc)
        except urllib.error.URLError as error:
            log.exception("[AP] Невозможно скачать вложенный файл: {0}.", error)
            self.text += '\n📃 <a href="{url}">{title}</a>'.format(**attachment["doc"])

    def generate_video(self, attachment):
        log.info("[AP] Извлечение видео...")
        video_link = "https://m.vk.com/video{owner_id}_{id}".format(**attachment["video"])
        if not attachment["video"].get("platform"):
            soup = BeautifulSoup(self.session.http.get(video_link).text, "html.parser")
            if len(soup.find_all("source")) >= 2:
                video_link = soup.find_all("source")[1].get("src")
                file = download(video_link)
                if getsize(file) >= 2097152000:
                    log.info("[AP] Видео весит более 2 ГБ. Добавляем ссылку на видео в текст.")
                    self.text += '\n🎥 <a href="{0}">{1[title]}</a>\n👁 {1[views]} раз(а) ⏳ {1[duration]} сек'.format(
                        video_link.replace("m.", ""), attachment["video"]
                    )
                    del file
                    return None
                self.media.append(InputMediaVideo(file))
        else:
            self.text += '\n🎥 <a href="{0}">{1[title]}</a>\n👁 {1[views]} раз(а) ⏳ {1[duration]} сек'.format(
                video_link.replace("m.", ""), attachment["video"]
            )

    def generate_music(self):
        if "audio" in self.attachments_types:
            log.info("[AP] Извлечение аудио...")
            try:
                tracks = self.audio_session.get_post_audio(self.raw_post["owner_id"], self.raw_post["id"])
            except Exception as error:
                log.error("Ошибка получения аудиозаписей: {0}", error)
            else:
                for track in tracks:
                    name = (
                        sub(r"[^a-zA-Z '#0-9.а-яА-Я()-]", "", track["artist"] + " - " + track["title"])[
                        : MAX_FILENAME_LENGTH - 16
                        ]
                        + ".mp3"
                    )
                    if ".m3u8" in track["url"]:
                        log.warning("Файлом аудиозаписи является m3u8 плейлист.")
                        file = name
                        streamlink_args = ["streamlink", "--output", name.replace(".mp3", ".ts"), track["url"], "best"]
                        ffmpeg_args = ["ffmpeg", "-i", name.replace(".mp3", ".ts"), "-b:a", "320k", name]

                        result = start_process(streamlink_args)
                        if result > 0:
                            log.critical("При запуске команды {} произошла ошибка.", " ".join(streamlink_args))
                            continue

                        result = start_process(ffmpeg_args)
                        if result > 0:
                            log.critical("При запуске команды {} произошла ошибка", " ".join(ffmpeg_args))
                            continue
                    else:
                        try:
                            file = download(track["url"], out=name)
                        except (urllib.error.URLError, IndexError):
                            log.exception("[AP] Не удалось скачать аудиозапись. Пропускаем ее...")
                            continue
                    track_cover = download(track["track_covers"][-1]) if track["track_covers"] else None
                    log.debug("Adding tags in track")
                    result = add_audio_tags(
                        file,
                        title=track["title"],
                        artist=track["artist"],
                        track_cover=track_cover,
                    )
                    if result:
                        log.debug("Track {} ready for sending", name)
                        self.tracks.append((name, track["duration"], track["artist"], track["title"], track_cover))

    def generate_poll(self, attachment):
        self.poll = {
            "question": attachment["poll"]["question"],
            "options": [answer["text"] for answer in attachment["poll"]["answers"]],
            "allows_multiple_answers": attachment["poll"]["multiple"],
            "is_anonymous": attachment["poll"]["anonymous"],
        }
        if len(self.poll["options"]) == 1:
            self.poll["options"].append("...")

    def sign_post(self):
        button_list = []
        log.info("[AP] Подписывание поста и добавление ссылки на его оригинал.")
        if self.user:
            user = "https://vk.com/{0[domain]}".format(self.user)
            button_list.append(
                InlineKeyboardButton("Автор поста: {first_name} {last_name}".format(**self.user), url=user)
            )
        if self.attachments_types.count("photo") > 1:
            if self.user:
                self.text += '\nАвтор поста: <a href="{}">{first_name} {last_name}</a>'.format(user, **self.user)
            self.text += '\n<a href="{}">Оригинал поста</a>'.format(self.post_url)
        else:
            button_list.append(InlineKeyboardButton("Оригинал поста", url=self.post_url))
        self.reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1)) if button_list else None

    def generate_user(self):
        if "signer_id" in self.raw_post:
            log.debug("Retrieving signer_id")
            self.user = self.session.method(
                method="users.get", values={"user_ids": self.raw_post["signer_id"], "fields": "domain"}
            )[0]
        elif self.raw_post["owner_id"] != self.raw_post["from_id"]:
            self.user = self.session.method(
                method="users.get", values={"user_ids": self.raw_post["from_id"], "fields": "domain"}
            )[0]

    def generate_repost(self):
        log.info("Включена отправка репоста. Начинаем парсинг репоста.")
        source_id = int(self.raw_post["copy_history"][0]["from_id"])
        try:
            source_info = self.session.method(method="groups.getById", values={"group_id": -source_id})[0]
            repost_source = 'Репост из <a href="https://vk.com/{screen_name}">{name}</a>:\n\n'.format(**source_info)
        except exceptions.ApiError:
            source_info = self.session.method(method="users.get", values={"user_ids": source_id})[0]
            repost_source = 'Репост от <a href="https://vk.com/id{id}">{first_name} {last_name}</a>:\n\n'.format(
                **source_info
            )
        self.repost = VkPostParser(
            self.raw_post["copy_history"][0],
            source_info.get("screen_name", ""),
            self.session,
            self.sign_posts,
            self.what_to_parse,
        )
        self.repost.generate_post()
        self.repost.text = repost_source + self.repost.text


class VkStoryParser:
    def __init__(self, story):
        self.story = story
        self.text = ""
        self.media = []
        self.reply_markup = None

    def generate_story(self):
        if self.story["type"] == "photo":
            self.generate_photo()
        elif self.story["type"] == "video":
            self.generate_video()
        if self.story.get("link"):
            self.generate_link()

    def generate_photo(self):
        log.info("[AP] Извлечение фото...")
        photo = None
        for i in self.story["photo"]["sizes"]:
            photo = i["url"]
        photo = download(photo, bar=None)
        if photo is not None:
            self.media.append(InputMediaPhoto(photo))

    def generate_video(self):
        log.info("[AP] Извлечение видео...")
        video_link = None
        video_file = None
        for _, v in self.story["video"]["files"].items():
            video_link = v
        if video_link is not None:
            video_file = download(video_link)
        if video_file is not None:
            self.media.append(InputMediaVideo(video_file))

    def generate_link(self):
        log.info("[AP] Обнаружена ссылка, создание кнопки...")
        button_list = [InlineKeyboardButton(**self.story["link"])]
        self.reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
