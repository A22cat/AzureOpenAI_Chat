import streamlit as st
import openai
import os

# ここに st.set_page_config() を移動（import直後！）最初に一度だけ書く
st.set_page_config(
    page_title="Azure OpenAI チャット",
    page_icon="🐱",
    layout="centered",
)

# envファイル読込なしのため、コメントアウト
# .envファイルからAPIキーとエンドポイントなどを読み込むときに利用
#load_dotenv()

# AzureポータルからコピーしたAPIキーとエンドポイントを貼り付けます。
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")    # これ超重要（画面のモデル バージョンでは動かず、2023-12-01-previewで動く）
model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")    # Azureで作ったデプロイメント名

# 以降はAPI_KEY, ENDPOINT, api_version, model_nameを使う
print(API_KEY)
print(ENDPOINT)
print(api_version)
print(model_name)

# Azure OpenAIクライアントを作成 
client = openai.AzureOpenAI(
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=api_version
)
print(client)

# ページタイトル表示
st.title("Azure OpenAI チャット")

# セッションにチャット履歴がなければ初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- チャット履歴を画面に表示（userは右、AIは左） ---
for msg in st.session_state.messages:
    if msg["role"] == "user":  # ユーザーのメッセージの場合
        with st.container():
            col1, col2 = st.columns([5, 1])  # 右寄せにするためカラムの比率を変更
            with col1:
                st.markdown(
                    f"<div style='text-align: right; background-color: #DCF8C6; padding: 8px; border-radius: 8px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            with col2:
                img_col, label_col = st.columns([2, 1])  # ラベルと画像を上下配置
                with label_col:
                    st.image(
                        "image/user_cat_icon_01.png",
                        width=40
                    )
                with img_col:
                    st.markdown("<div style='padding-top:12px; font-weight:bold;'>あなた</div>", unsafe_allow_html=True)
    else:  # AIのメッセージの場合
        with st.container():
            col1, col2 = st.columns([1, 5])  # 左寄せにするためカラムの比率を変更
            with col1:
                img_col, label_col = st.columns([1, 2])  # 画像とラベルを並べる
                with img_col:
                    st.image(
                        "image/ai_cat_ion_02.png",
                        width=40
                    )
                with label_col:
                    st.markdown("<div style='padding-top:12px; font-weight:bold;'>AI</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f"<div style='text-align: left; background-color: #F1F0F0; padding: 8px; border-radius: 8px;'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )

# 自動でスクロールを一番下に（JavaScriptを直接HTMLで埋め込み）
#st.write('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)

# 区切り線を表示
st.divider()

# --- ユーザー入力フォームエリア ---
with st.form(key="chat_form", clear_on_submit=True):
    # ユーザーの質問入力欄
    user_input = st.text_area("質問を入力してください:", height=100)

    # ファイルアップロード欄（txtファイル限定）
    uploaded_file = st.file_uploader("ファイルをアップロード", type=["txt"])

    # 送信ボタン
    submitted = st.form_submit_button("送信")

    if submitted and (user_input or uploaded_file):
        # 入力された質問内容を保持
        full_user_input = user_input

        # ファイルがアップロードされた場合、ファイル内容を付加
        if uploaded_file is not None:
            file_content = uploaded_file.read().decode('utf-8')
            full_user_input += "\n\n【アップロードされたファイルの内容】\n" + file_content

        # ユーザーメッセージを履歴に追加
        st.session_state.messages.append({"role": "user", "content": full_user_input})

        # AI応答待ち時のスピナー表示(ローディング中の表示)
        with st.spinner('AIが考え中...🐾'):
            # Azure OpenAIにチャット履歴を送信して応答を取得
            response = client.chat.completions.create(
                model=model_name,
                messages=st.session_state.messages
            )

            # AIの応答を履歴に追加
            ai_response = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # 最新のチャット履歴を反映するためページをリロード
        st.rerun()
