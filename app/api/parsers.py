from fastapi import APIRouter
from selenium import webdriver
from typing import Dict, List
from app.parsers.technodom_parser import TechnodomParser
from app.parsers.dns_parser import DNSScraper
from app.parsers.marwin_parser import MarwinParser

router = APIRouter()

@router.get("/technodom")
def parse_technodom() -> Dict[str, List]:
    driver = webdriver.Chrome()
    try:
        parser = TechnodomParser(driver)
        return parser.parse()
    finally:
        driver.quit()

@router.get("/dns")
def parse_dns() -> List[str]:
    scraper = DNSScraper()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@router.get("/marwin")
def parse_marwin() -> List[str]:
    scraper = MarwinParser()
    try:
        return scraper.parse()
    finally:
        scraper.close()

@router.get("/all")
def parse_all() -> Dict[str, List]:
    technodom_games, dns_games, marwin_games = [], [], []

    driver = webdriver.Chrome()
    try:
        technodom_parser = TechnodomParser(driver)
        technodom_games = technodom_parser.parse()
    finally:
        driver.quit()

    dns_scraper = DNSScraper()
    try:
        dns_games = dns_scraper.parse()
    finally:
        dns_scraper.close()

    marwin_scraper = MarwinParser()
    try:
        marwin_games = marwin_scraper.parse()
    finally:
        marwin_scraper.close()

    return {
        "technodom": technodom_games,
        "dns": dns_games,
        "marwin": marwin_games
    }
