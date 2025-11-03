# 占いのお店リスト抽出ツール

Googleマップから「占い」のお店を全国から抽出するPythonスクリプトです。

## 必要な環境

- Python 3.7以上
- Google Maps Platform APIキー（Places API (New) が有効化されていること）

## セットアップ

### 1. Google Maps Platform APIキーの取得

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. プロジェクトを作成または選択
3. 「APIとサービス」→「ライブラリ」から「Places API (New)」を有効化
4. 「認証情報」からAPIキーを作成
5. APIキーに適切な制限を設定（推奨）

### 2. 依存パッケージのインストール

```bash
pip install requests
```

### 3. 環境変数の設定

```bash
export GOOGLE_MAPS_API_KEY='your-api-key-here'
```

または、`.env`ファイルを作成：

```
GOOGLE_MAPS_API_KEY=your-api-key-here
```

## 使用方法

```bash
python extract_fortune_shops.py
```

## 出力ファイル

実行すると以下のファイルが生成されます：

1. **fortune_shops_list.csv** - CSV形式の店舗リスト
2. **fortune_shops_list.json** - JSON形式の店舗リスト

## 出力データの項目

- `id`: 店舗ID
- `name`: 店舗名
- `address`: 住所
- `phone`: 電話番号
- `rating`: 評価
- `user_ratings_total`: レビュー数
- `latitude`: 緯度
- `longitude`: 経度
- `types`: カテゴリ
- `website`: ウェブサイトURL
- `google_maps_url`: GoogleマップURL

## 検索範囲

日本全国47都道府県を対象に検索します。各都道府県で以下のキーワードで検索：

- 占い
- 占い館
- 占いの館
- タロット占い
- 手相占い
- fortune telling

## 注意事項

### API使用料金

- Google Places API (New)は従量課金制です
- Text Search: 1,000リクエストあたり $32
- 全国検索を実行すると、数百～数千のリクエストが発生する可能性があります
- 無料枠: 月額$200のクレジット（新規登録時）

### レート制限

- APIのレート制限に配慮し、リクエスト間に適切な待機時間を設けています
- 大量検索の場合は時間がかかります（全国で30分～1時間程度）

### データの精度

- Google Places APIで取得できる店舗情報に依存します
- すべての占い店舗が網羅されているわけではありません
- 店舗情報が登録されていない、またはカテゴリが異なる場合は抽出されません

## トラブルシューティング

### エラー: GOOGLE_MAPS_API_KEY 環境変数が設定されていません

環境変数が正しく設定されているか確認してください：

```bash
echo $GOOGLE_MAPS_API_KEY
```

### エラー: 403 Forbidden

- APIキーが正しいか確認
- Places API (New)が有効化されているか確認
- APIキーの制限設定を確認

### 結果が少ない

- 検索キーワードを追加してカスタマイズ
- 検索半径を調整
- より細かい地域単位で検索

## カスタマイズ

### 検索キーワードの変更

`search_queries`リストを編集：

```python
search_queries = [
    "占い",
    "占い館",
    # 追加のキーワード
]
```

### 検索対象地域の変更

`JAPAN_PREFECTURES`リストを編集して特定の都道府県のみに絞ることができます。

## ライセンス

このスクリプトの使用にあたっては、Google Maps Platform利用規約を遵守してください。
