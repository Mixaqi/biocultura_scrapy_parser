from __future__ import annotations

import os

import psycopg2
import scrapy


class SaveToPostgresPipeLine:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host = os.environ.get("PG_HOST"),
            user = os.environ.get("PG_USER"),
            password = os.environ.get("PG_PASSWORD"),
            database = os.environ.get("PG_NAME"),
        )
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS expositors(
            Id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            link VARCHAR(150),
            contact_name VARCHAR(150),
            email VARCHAR (100),
            phone VARCHAR(20),
            whatsapp_phone VARCHAR(250),
            country VARCHAR(40))""")

    def process_item(self, item: dict[str, str], spider: scrapy.Spider) -> None:
        self.cur.execute(""" 
        INSERT INTO expositors (
            title,
            link,
            contact_name,
            email,
            phone,
            whatsapp_phone,
            country
        ) VALUES (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s            
        )""", (
            item["title"],
            item["link"],
            item["contact_name"],
            item["email"],
            item["phone"],
            item["whatsapp_phone"],
            item["country"],
        ))
        self.conn.commit()
        return item

    def close_spider(self, spider: scrapy.Spider) -> None:
        self.cur.close()
        self.conn.close()
