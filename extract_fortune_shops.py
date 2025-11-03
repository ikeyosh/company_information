#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Googleマップから「占い」のお店を抽出するスクリプト
Google Places API (New) を使用
"""

import os
import json
import time
import csv
from typing import List, Dict
import requests

# APIキーの設定（環境変数から取得）
API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

# 日本の主要都道府県の中心座標
JAPAN_PREFECTURES = [
    {"name": "北海道", "lat": 43.064615, "lng": 141.346807},
    {"name": "青森県", "lat": 40.824308, "lng": 140.740051},
    {"name": "岩手県", "lat": 39.703532, "lng": 141.152709},
    {"name": "宮城県", "lat": 38.268837, "lng": 140.872097},
    {"name": "秋田県", "lat": 39.718614, "lng": 140.102364},
    {"name": "山形県", "lat": 38.240436, "lng": 140.363634},
    {"name": "福島県", "lat": 37.750299, "lng": 140.467551},
    {"name": "茨城県", "lat": 36.341811, "lng": 140.446793},
    {"name": "栃木県", "lat": 36.565725, "lng": 139.883565},
    {"name": "群馬県", "lat": 36.390668, "lng": 139.060406},
    {"name": "埼玉県", "lat": 35.856999, "lng": 139.648849},
    {"name": "千葉県", "lat": 35.605057, "lng": 140.123306},
    {"name": "東京都", "lat": 35.689487, "lng": 139.691706},
    {"name": "神奈川県", "lat": 35.447507, "lng": 139.642345},
    {"name": "新潟県", "lat": 37.902552, "lng": 139.023095},
    {"name": "富山県", "lat": 36.695291, "lng": 137.211338},
    {"name": "石川県", "lat": 36.594682, "lng": 136.625573},
    {"name": "福井県", "lat": 36.065219, "lng": 136.221640},
    {"name": "山梨県", "lat": 35.664158, "lng": 138.568449},
    {"name": "長野県", "lat": 36.651299, "lng": 138.180956},
    {"name": "岐阜県", "lat": 35.391227, "lng": 136.722291},
    {"name": "静岡県", "lat": 34.976987, "lng": 138.383057},
    {"name": "愛知県", "lat": 35.180188, "lng": 136.906565},
    {"name": "三重県", "lat": 34.730283, "lng": 136.508588},
    {"name": "滋賀県", "lat": 35.004531, "lng": 135.868605},
    {"name": "京都府", "lat": 35.021247, "lng": 135.755597},
    {"name": "大阪府", "lat": 34.686297, "lng": 135.519661},
    {"name": "兵庫県", "lat": 34.691269, "lng": 135.183071},
    {"name": "奈良県", "lat": 34.685334, "lng": 135.832748},
    {"name": "和歌山県", "lat": 34.226034, "lng": 135.167509},
    {"name": "鳥取県", "lat": 35.503891, "lng": 134.237736},
    {"name": "島根県", "lat": 35.472295, "lng": 133.050537},
    {"name": "岡山県", "lat": 34.661751, "lng": 133.934406},
    {"name": "広島県", "lat": 34.396033, "lng": 132.459595},
    {"name": "山口県", "lat": 34.185956, "lng": 131.470649},
    {"name": "徳島県", "lat": 34.065718, "lng": 134.559296},
    {"name": "香川県", "lat": 34.340149, "lng": 134.043444},
    {"name": "愛媛県", "lat": 33.841624, "lng": 132.765681},
    {"name": "高知県", "lat": 33.559706, "lng": 133.531079},
    {"name": "福岡県", "lat": 33.606576, "lng": 130.418297},
    {"name": "佐賀県", "lat": 33.249442, "lng": 130.299794},
    {"name": "長崎県", "lat": 32.744839, "lng": 129.873756},
    {"name": "熊本県", "lat": 32.789827, "lng": 130.741667},
    {"name": "大分県", "lat": 33.238172, "lng": 131.612619},
    {"name": "宮崎県", "lat": 31.911096, "lng": 131.423855},
    {"name": "鹿児島県", "lat": 31.560146, "lng": 130.557978},
    {"name": "沖縄県", "lat": 26.212401, "lng": 127.680932},
]


def search_places_nearby(lat: float, lng: float, radius: int = 50000) -> List[Dict]:
    """
    指定された座標周辺の占いのお店を検索

    Args:
        lat: 緯度
        lng: 経度
        radius: 検索半径（メートル）最大50000

    Returns:
        店舗情報のリスト
    """
    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.types,places.websiteUri,places.googleMapsUri'
    }

    # 占い関連のキーワード検索
    data = {
        "includedTypes": ["fortune_teller"],  # 占い師
        "maxResultCount": 20,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": radius
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get('places', [])
    except Exception as e:
        print(f"エラー発生: {e}")
        return []


def search_places_text(query: str, prefecture: str) -> List[Dict]:
    """
    テキスト検索で占いのお店を検索

    Args:
        query: 検索クエリ
        prefecture: 都道府県名

    Returns:
        店舗情報のリスト
    """
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.types,places.websiteUri,places.googleMapsUri'
    }

    data = {
        "textQuery": f"{query} {prefecture}",
        "maxResultCount": 20,
        "languageCode": "ja"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result.get('places', [])
    except Exception as e:
        print(f"エラー発生 ({prefecture}): {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"レスポンス: {e.response.text}")
        return []


def extract_shop_info(place: Dict) -> Dict:
    """
    店舗情報を抽出して整形

    Args:
        place: Places APIから取得した店舗情報

    Returns:
        整形された店舗情報
    """
    return {
        'id': place.get('id', ''),
        'name': place.get('displayName', {}).get('text', ''),
        'address': place.get('formattedAddress', ''),
        'phone': place.get('nationalPhoneNumber', ''),
        'rating': place.get('rating', ''),
        'user_ratings_total': place.get('userRatingCount', ''),
        'latitude': place.get('location', {}).get('latitude', ''),
        'longitude': place.get('location', {}).get('longitude', ''),
        'types': ','.join(place.get('types', [])),
        'website': place.get('websiteUri', ''),
        'google_maps_url': place.get('googleMapsUri', '')
    }


def main():
    """メイン処理"""

    if not API_KEY:
        print("エラー: GOOGLE_MAPS_API_KEY 環境変数が設定されていません")
        print("使用方法: export GOOGLE_MAPS_API_KEY='your-api-key'")
        return

    print("占いのお店抽出を開始します...")
    print(f"対象: 日本全国 {len(JAPAN_PREFECTURES)} 都道府県")

    all_shops = {}  # IDをキーにして重複を除外

    # 各都道府県で検索
    for i, prefecture in enumerate(JAPAN_PREFECTURES, 1):
        print(f"\n[{i}/{len(JAPAN_PREFECTURES)}] {prefecture['name']} を検索中...")

        # テキスト検索を使用（より確実に結果が得られる）
        search_queries = [
            "占い",
            "占い館",
            "占いの館",
            "タロット占い",
            "手相占い",
            "fortune telling"
        ]

        for query in search_queries:
            places = search_places_text(query, prefecture['name'])

            for place in places:
                shop_info = extract_shop_info(place)
                shop_id = shop_info['id']

                # 重複チェック
                if shop_id and shop_id not in all_shops:
                    all_shops[shop_id] = shop_info
                    print(f"  - {shop_info['name']} ({shop_info['address']})")

            # APIレート制限対策
            time.sleep(0.5)

        # 都道府県間で少し待機
        time.sleep(1)

    # CSV出力
    output_file = 'fortune_shops_list.csv'

    if all_shops:
        print(f"\n\n合計 {len(all_shops)} 件の占い店舗を抽出しました")
        print(f"結果を {output_file} に保存中...")

        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = ['id', 'name', 'address', 'phone', 'rating', 'user_ratings_total',
                         'latitude', 'longitude', 'types', 'website', 'google_maps_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for shop in all_shops.values():
                writer.writerow(shop)

        print(f"✓ 保存完了: {output_file}")

        # JSON形式でも保存
        json_file = 'fortune_shops_list.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(list(all_shops.values()), f, ensure_ascii=False, indent=2)
        print(f"✓ JSON保存完了: {json_file}")

    else:
        print("\n店舗が見つかりませんでした")


if __name__ == '__main__':
    main()
