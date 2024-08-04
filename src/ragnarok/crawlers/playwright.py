import json
import logging
import random
import re
import time
from collections import deque
from typing import List
from urllib.parse import urljoin, urlparse

import psutil
from bs4 import BeautifulSoup
from langdetect import detect
from markdownify import MarkdownConverter
from playwright.sync_api import sync_playwright
from tqdm import tqdm

from ..extractors.base import ExtractorOutput
from ..logger import RAGnarokLogger
from .base import BaseCrawler


class PlaywrightCrawler(BaseCrawler):
    def __init__(self, config: dict):
        self.config = config
        self.logger = RAGnarokLogger.get_logger()
        self.proxies = config.get("proxies", [])
        self.browser = config.get("browser", "firefox")

    def md(self, soup, **options):
        return MarkdownConverter(**options).convert_soup(soup)
    
    def log_memory_usage(self):
        process = psutil.Process()
        memory_info = process.memory_info()
        self.logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
        
    def save_checkpoint(self, results, queue, visited):
        checkpoint = {
            "results": json.dumps([result.to_dict() for result in results]),
            "queue": list(queue),
            "visited": list(visited)
        }
        with open("crawler_checkpoint.json", "w") as f:
            json.dump(checkpoint, f)

    def get_random_proxy(self):
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        ip, port, username, password = proxy.split(":")
        return {
            "server": f"http://{ip}:{port}",
            "username": username,
            "password": password,
        }

    def clean_content(self, content):
        content = re.sub(r"\n+", "\n", content)
        content = "\n".join(line.strip() for line in content.split("\n"))
        content = re.sub(r"([a-z])\n([A-Z])", r"\1.\n\2", content)
        content = re.sub(r" +", " ", content)
        return content.strip()

    def estimate_reading_time(self, content, wpm=200):
        words = len(content.split())
        return round(words / wpm)

    def crawl_url(self, page, url, max_retries=3, retry_delay=5):
        for attempt in range(max_retries):
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle", timeout=10000)
                content = page.content()

                if not content or len(content.strip()) < 50:
                    raise ValueError("Empty or too short content")

                return content
            except Exception as e:
                if attempt < max_retries - 1:
                    self.logger.warning(
                        f"Error crawling {url} (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay} seconds..."
                    )
                    time.sleep(retry_delay)
                else:
                    self.logger.error(
                        f"Failed to crawl {url} after {max_retries} attempts: {e}"
                    )
                    return None

    def is_valid_url(self, base_url, url):
        base_parsed = urlparse(base_url)
        parsed = urlparse(url)
        base_path = base_parsed.path.rstrip("/")
        current_path = parsed.path.split("#")[0].rstrip("/")
        if parsed.netloc == base_parsed.netloc and current_path.startswith(base_path):
            return current_path != base_path and not parsed.fragment
        return False

    def crawl(self, base_url, depth, save_checkpoint=False) -> List[ExtractorOutput]:
        self.logger.info(f"Starting crawl of {base_url} with depth {depth}")
        visited = set()
        queue = deque([(base_url, 0)])
        results = []
        total_urls = 1

        with sync_playwright() as p:
            proxy = self.get_random_proxy()
            if self.browser == "firefox":
                browser = p.firefox.launch(headless=True, proxy=proxy)
            elif self.browser == "chromium":
                browser = p.chromium.launch(headless=True, proxy=proxy)
            elif self.browser == "webkit":
                browser = p.webkit.launch(headless=True, proxy=proxy)
            else:
                raise ValueError(f"Invalid browser: {self.browser}")
            page = browser.new_page()

            page.route(re.compile(r"(\.png$)|(\.jpg$)|(\.gif$)|(\.svg$)|(\.ico$)|"), lambda route: route.abort())

            with tqdm(total=total_urls, desc="Crawling", unit="URL") as pbar:
                try:
                    while queue:
                        url, current_depth = queue.popleft()
                        url_without_fragment = url.split("#")[0]

                        if current_depth > depth:
                            break

                        if url_without_fragment in visited:
                            continue

                        visited.add(url_without_fragment)
                        self.logger.info(f"Crawling: {url}")

                        content = self.crawl_url(page, url)
                        if content is None:
                            continue

                        soup = BeautifulSoup(content, "html.parser")

                        title = soup.title.string if soup.title else "No title"
                        markdown_content = self.clean_content(
                            self.md(
                                soup,
                                strip=["a", "img", "code"],
                                autolinks=False,
                                heading_style="ATX",
                                newline_style="BACKSLASH",
                            )
                        )

                        meta_description = soup.find("meta", attrs={"name": "description"})
                        meta_description = (
                            meta_description["content"] if meta_description else None
                        )

                        headings = [
                            h.text
                            for h in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
                        ]
                        word_count = len(markdown_content.split())
                        character_count = len(markdown_content)
                        images_alt_text = [
                            img.get("alt", "")
                            for img in soup.find_all("img")
                            if img.get("alt")
                        ]

                        try:
                            language = detect(markdown_content)
                        except:
                            language = "unknown"

                        reading_time = self.estimate_reading_time(markdown_content)

                        metadata = {
                            "url": url,
                            "title": title,
                            "meta_description": meta_description,
                            "headings": headings,
                            "word_count": word_count,
                            "character_count": character_count,
                            "images_alt_text": images_alt_text,
                            "language": language,
                            "reading_time_minutes": reading_time,
                        }

                        results.append(
                            ExtractorOutput(text=markdown_content, metadata=metadata)
                        )

                        if len(results) % 10 == 0:
                            self.log_memory_usage()
                            if save_checkpoint:
                                self.logger.info(f"Saving checkpoint...")
                                self.save_checkpoint(results, queue, visited)

                        if current_depth < depth:
                            new_links = 0
                            queue_urls = set(url for url, _ in queue)
                            for link in soup.find_all("a", href=True):
                                full_url = urljoin(url, link["href"])
                                full_url_without_fragment = full_url.split("#")[0]

                                if (
                                    self.is_valid_url(base_url, full_url)
                                    and full_url_without_fragment not in visited
                                    and full_url_without_fragment not in queue_urls
                                ):
                                    queue.append((full_url, current_depth + 1))
                                    queue_urls.add(full_url_without_fragment)
                                    new_links += 1

                            total_urls += new_links
                            pbar.total = total_urls
                            pbar.refresh()

                        pbar.update(1)
                except Exception as e:
                    self.logger.error(f"Unexpected error during crawling: {e}")
                finally:
                    browser.close()
                    return results
