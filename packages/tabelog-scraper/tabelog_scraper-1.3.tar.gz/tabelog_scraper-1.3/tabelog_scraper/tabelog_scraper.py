#!/usr/bin/python
# -*- coding: utf-8 -*-
"""メインモジュール
"""
from typing import Dict, Tuple, Text, Any, List
from tabelog_scraper.adapter.extractor.scrapeing_extractor import ScrapingExtractor
from tabelog_scraper.adapter.tabelog_recommender import TabelogRecommender


def scrape(target_url: str, limit_page_count: int = 10,
           ignore_urls: List[str] = []) -> Tuple[Dict[Text, Any]]:
    """スクレイピング処理
    スクレイピング処理を実行。時間がかかることに注意

    Args:
        target_url (:obj:`str`): スクレイピングしたい食べログページを指定。1ページ目を利用すること。
        limit_page_count (:obj:`int`): スクレイピングする上限ページを指定。
        ignore_urls (:obj:`List[str]`): スクレイピング対象にしない店舗URLを指定。
    Returns:
        Tuple[Dict[Text, Any]]: 取得できたDict型の店舗情報リストをタプル型で返却
    """

    # 実行
    extractor = ScrapingExtractor(target_url, limit_page_count)
    return TabelogRecommender(extractor).execute(ignore_urls)


if __name__ == '__main__':
    """
    テスト実行用
    """
    result = scrape(
        "https://tabelog.com/tokyo/A1315/A131501/R1644/rstLst/1/?svd=20200313&svt=1900&svps=2",
        1)
    print(result)
