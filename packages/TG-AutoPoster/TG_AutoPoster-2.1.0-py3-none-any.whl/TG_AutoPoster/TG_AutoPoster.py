#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import configparser
import os
from pathlib import Path
from re import sub
from tempfile import TemporaryDirectory
from time import sleep

from loguru import logger as log
from pyrogram import Client
from vk_api import VkApi

from TG_AutoPoster.handlers import auth_handler, captcha_handler
from TG_AutoPoster.group import Group
from TG_AutoPoster.sender import PostSender

if os.name != "nt":
    TEMP_DIR = TemporaryDirectory(prefix="TG_AutoPoster")
    CACHE_DIR = Path(TEMP_DIR.name)
else:
    CACHE_DIR = Path.cwd() / ".cache"
CONFIG_PATH = Path.cwd() / "config.ini"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="TG_AutoPoster",
        description="Telegram Bot for AutoPosting from VK",
        epilog="(C) 2018-2020 Adrian Polyakov\nReleased under the MIT License.",
    )

    parser.add_argument(
        "-6", "--ipv6", action="store_true", help="Использовать IPv6 при подключении к Telegram (IPv4 по умолчанию)"
    )
    parser.add_argument(
        "-l",
        "--loop",
        action="store_const",
        const=True,
        default=False,
        help="Запустить бота в бесконечном цикле с проверкой постов раз в час (по умолчанию)",
    )
    parser.add_argument("-s", "--sleep", type=int, default=0, help="Проверять новые посты каждые N секунд", metavar="N")
    parser.add_argument(
        "-c",
        "--config",
        default=CONFIG_PATH,
        help="Абсолютный путь к конфиг файлу бота (по умолчанию {})".format(CONFIG_PATH),
    )
    parser.add_argument(
        "--cache-dir",
        default=CACHE_DIR,
        help="Абсолютный путь к папке с кэшем бота (по умолчанию используется временная папка; .cache в Windows)",
    )
    parser.add_argument("-d", "--debug", action="store_true", help="Режим отладки")
    parser.add_argument(
        "-i",
        "--ignore-errors",
        action="store_true",
        help="Игнорировать любые возникающие ошибки (работает с параметром --loop)"
    )
    return parser


class AutoPoster:
    IGNORE_ERRORS = False

    def __init__(self, config_path=CONFIG_PATH, cache_dir=CACHE_DIR, ipv6=False):
        self.cache_dir = cache_dir
        self.config_path = config_path
        # Чтение конфигурации бота из файла config.ini
        self._reload_config()
        # Инициализация Telegram бота
        self.bot = Client("TG_AutoPoster", ipv6=ipv6, config_file=config_path, workdir=os.getcwd())
        self.bot.set_parse_mode("html")
        # Чтение из конфига логина, пароля, а также токена (если он есть)
        vk_login = self.config.get("global", "login")
        vk_pass = self.config.get("global", "pass")
        vk_token = self.config.get("global", "token", fallback="")
        # Чтение из конфига пути к файлу со стоп-словами
        self.stop_list = self.config.get("global", "stop_list", fallback=[])
        self.blacklist = self.config.get("global", "blacklist", fallback=[])
        if self.stop_list:
            # Инициализация списка стоп-слов
            with open(self.stop_list, "r", encoding="utf-8") as f:
                self.stop_list = [i.strip() for i in f.readlines()]
            log.info("Загружен список стоп-слов")
        if self.blacklist:
            with open(self.blacklist, encoding="utf-8") as f:
                self.blacklist = [i.strip() for i in f.readlines()]
            log.info("Загружен черный спиок слов")
        # Инициализация ВК сессии
        if vk_token:  # Если в конфиге был указан токен, то используем его
            self.vk_session = VkApi(token=vk_token)  # При использовании токена будут недоступны аудиозаписи
        else:  # В противном случае авторизуемся, используя логин и пароль
            self.vk_session = VkApi(
                login=vk_login, password=vk_pass, auth_handler=auth_handler, captcha_handler=captcha_handler
            )
            self.vk_session.auth()

    def run(self):
        # Переход в папку с кэшем
        try:
            os.chdir(self.cache_dir)
        except FileNotFoundError:
            os.mkdir(self.cache_dir)
        domains = self.config.sections()[3:] if self.config.has_section("proxy") else self.config.sections()[2:]
        for domain in domains:
            try:
                chat_id = self.config.getint(domain, "channel")
            except ValueError:
                chat_id = self.config.get(domain, "channel")
            disable_notification = self.config.getboolean(
                domain,
                "disable_notification",
                fallback=self.config.getboolean("global", "disable_notification", fallback=False),
            )
            disable_web_page_preview = self.config.getboolean(
                domain,
                "disable_web_page_preview",
                fallback=self.config.getboolean("global", "disable_web_page_preview", fallback=True),
            )
            send_stories = self.config.getboolean(
                domain, "send_stories", fallback=self.config.getboolean("global", "send_stories", fallback=False)
            )
            last_id = self.config.getint(domain, "last_id", fallback=0)
            pinned_id = self.config.getint(domain, "pinned_id", fallback=0)
            send_reposts = self.config.get(domain, "send_reposts", fallback=self.config.get("global", "send_reposts", fallback=0))
            sign_posts = self.config.getboolean(
                domain, "sign_posts", fallback=self.config.getboolean("global", "sign_posts", fallback=True)
            )
            what_to_parse = set(
                self.config.get(domain, "what_to_send", fallback=self.config.get("global", "what_to_send", fallback="all")).split(",")
            )
            posts_count = self.config.getint(domain, "posts_count", fallback=self.config.get("global", "posts_count", fallback=11))
            last_story_id = self.config.getint(domain, "last_story_id", fallback=0)
            group = Group(
                domain,
                self.vk_session,
                last_id, pinned_id,
                send_reposts,
                sign_posts,
                what_to_parse,
                posts_count,
                last_story_id
            )
            # Получение постов
            posts = group.get_posts()
            for post in posts:
                skip_post = False
                for word in self.stop_list:
                    if word.lower() in post.text.lower():
                        skip_post = True  # Если пост содержит стоп-слово, то пропускаем его.
                        log.info("Пост содержит стоп-слово, поэтому он не будет отправлен.")
                # Отправка постов
                if not skip_post:
                    for word in self.blacklist:
                        post.text = sub(word, "", post.text)
                    with self.bot:
                        sender = PostSender(self.bot, post, chat_id, disable_notification, disable_web_page_preview)
                        sender.send_post()
                self.config.set(domain, "pinned_id", str(group.pinned_id))
                self.config.set(domain, "last_id", str(group.last_id))
                self._save_config()
            if send_stories:
                # Получение историй, если включено
                stories = group.get_stories()
                for story in stories:
                    with self.bot:
                        sender = PostSender(
                            self.bot,
                            story,
                            self.config.get(domain, "channel"),
                            disable_notification,
                            disable_web_page_preview,
                        )
                        sender.send_post()
                        self.config.set(domain, "last_story_id", str(group.last_story_id))
                    self._save_config()
            log.debug("Clearing cache directory {}", self.cache_dir)
            for data in os.listdir(self.cache_dir):
                os.remove(self.cache_dir / data)
        self._save_config()

    def infinity_run(self, interval=3600):
        while True:
            try:
                self.run()
            except Exception as exc:
                log.opt(exception=True).exception("При работе программы возникла ошибка")
                if self.IGNORE_ERRORS:
                    log.warning("Было включено игнорирование ошибок, возобновление работы")
                else:
                    log.error("Продолжение работы невозможно. Выход...")
                    raise exc
            else:
                log.info("Работа завершена. Отправка в сон на {} секунд.", interval)
                sleep(interval)
                self._reload_config()

    def _save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)
        log.debug("Config saved.")

    def _reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        log.debug("Config reloaded.")
