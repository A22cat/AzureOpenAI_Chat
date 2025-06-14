# Azure OpenAI チャット -  セットアップガイド

本ガイドでは、Azure OpenAI チャットのセットアップに関する設定、ローカル環境での実行手順、および、Azure App Serviceへのデプロイ手順の概要を説明します。

## 1. 前提条件

- [Azureアカウント](https://azure.microsoft.com/ja-jp/free/)
- [Python 3.10 以降](https://www.python.org/downloads/)
- [Visual Studio Code](https://code.visualstudio.com/)
  - [Azure App Service 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice)
  - [Python 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-python.python)


## 2. Azureリソースの準備

Azureポータルにログインし、以下のリソースを作成します。リソース名は任意ですが、後で環境変数に設定するため控えておいてください。

### a. Azure OpenAI Service

1.  Azureポータルで「Azure OpenAI」を検索し、「作成」を選択します。
2.  サブスクリプション、リソースグループ、リージョン、一意の名前を入力します。
3.  価格レベルは「Standard S0」を選択します。
4.  作成後、リソースに移動し、「Go to Azure AI Foundy portal」＞ 左サイドバーの「チャット」＞「新しいデプロイの作成」＞ 「基本モデルから」を選択し、以下のモデルをデプロイします。
    -   **Chatモデル**: `gpt-4o` または `gpt-4o-mini`など
    -   開発環境では、コストを考慮すると `gpt-4o-mini` の選択肢を検討することができます。
5.  左サイドバーの共有リソースから「デブロイ」で作成したデプロイを選択し、「キー」と「エンドポイント」、「デプロイメント名」を控えます。


## 3. ローカル環境での実行
1. GitHub.com からローカルコンピューターにリポジトリをクローンします。
2. プロジェクトのルートディレクトリで、ターミナルを開きます。
3. env.example をコピーして `.env` という名前のファイルを作成します。Azureリソースの作成時に控えた各サービスのキーとエンドポイントをすべて設定します。
必要なPythonパッケージをインストールします。

Bash
```
pip install -r requirements.txt
```

Streamlitアプリを起動します。

Bash
```
streamlit run main_db_chat_ai.py
```
ブラウザで http://localhost:8501 が開き、アプリケーションが表示されます。


## 4. VSCodeを使用したAzure App Serviceへのデプロイ
VSCodeのAzure拡張機能を使って、アプリケーションをデプロイします。

1. Azure ポータルでApp Service を開き、左側のメニューから 「設定」 >「環境変数」を選択し、[+追加]からアプリケーション設定にenvファイルの内容を一つずつ環境変数として追加します。
    - 名前：環境変数のキー（例：AZURE_OPENAI_ENDPOINT）
    - 値：環境変数の値 (例：https://your-resource.openai.azure.com/)
2. 左側のメニューから 「構成」(Configration) > 全般設定 を選択し、「スタートアップコマンド」に以下を設定して保存します。

```
python -m streamlit run main_openai_nyazuchat.py --server.port 8000 --server.address 0.0.0.0
```

3. 次にVSCodeで「ファイル」>「フォルダーを開く...」でプロジェクトフォルダ（chat-openai-azure）を選択し、開きます。
4. 左のアクティビティバーからAzureアイコンを選択し、Azureアカウントにサインインします。
5. Azure拡張機能パネルに戻り、リソースの一覧からデプロイ先のApp Serviceを探します。
対象のApp ServiceはStoppedではなく通常は起動したままデプロイします。
6. 対象のApp Serviceを右クリックし、「Deploy to Web App...」を選択します。
7. 「Would you like to update your workspace configuration to run build commands on the target server?This should improve deployment performance.」の確認メッセージが表示されたら、「Yes」を選択します。「Yes」を選ぶと、今後同じワークスペースからデプロイする際に、ビルドコマンド（依存パッケージのインストールなど）がAzure側で実行されるように設定され、デプロイが効率化されます。この設定は .vscode/settings.json に保存され、プロジェクト単位で適用されます。後から変更したい場合も、ワークスペース設定で編集できます。
8. 「Are you sure you want to deploy to "<App Service名>"? This will overwrite any previous deplyment and cannot be undone.」の確認メッセージが表示されたら、「Deploy」を選択します。現在のWebアプリに新しいコードを上書いてデプロイします。
8. デプロイが完了すると通知が表示されます。その後、App ServiceのURLにアクセスして、アプリケーションが正しく動作することを確認します。