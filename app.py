import streamlit as st
import cv2
import mediapipe as mp
import time
import random
import gradio as gr
import threading
import queue

# =========================================================
# 🌟 Gradio ゲームセットアップ（ローカル対応版）
# =========================================================
def launch_gradio_game(level):
    import random, time, asyncio

    async def reaction_game():
        html = """
        <div style='text-align:center;'>
            <div style='width:150px; height:150px; background-color:#ff4b5c; margin:auto; border-radius:10px;'></div>
            <p style='font-size:22px;'>🔴 赤です！緑になるまで待ってください…</p>
        </div>
        """
        yield html, ""
        await asyncio.sleep(random.uniform(2, 5))
        green_time = time.time()
        html_green = f"""
        <div style='text-align:center;'>
            <div style='width:150px; height:150px; background-color:#4CAF50; margin:auto; border-radius:10px;'></div>
            <p style='font-size:22px;'>🟢 今クリック！</p>
        </div>
        """
        yield html_green, str(green_time)

    def record_time():
        return str(time.time())

    def record_reaction(user_click_time, green_time):
        try:
            green_time = float(green_time)
            user_time = float(user_click_time)
            if user_time < green_time:
                return "<p style='color:red;'>❌ 早すぎ！まだ赤でした！</p>"
            else:
                reaction = user_time - green_time
                return f"<p style='font-size:22px; color:#007bff;'>⚡ あなたの反応時間: {reaction:.3f} 秒 ⚡</p>"
        except:
            return "<p style='color:red;'>⚠️ 緑が出てからクリックしてください。</p>"

    def new_math_question():
        a, b = random.randint(10, 99), random.randint(10, 99)
        return f"{a} + {b} = ?", a + b, ""

    def check_math_answer(user_answer, correct_answer):
        if not user_answer.strip():
            return "⚠️ 答えを入力してください！"
        try:
            user_val = int(user_answer)
        except:
            return "❌ 数字を入力してください。"
        if user_val == correct_answer:
            return "✅ 正解！頭が冴えてきましたね！"
        else:
            return f"❌ 残念！正解は {correct_answer} でした。"

    def generate_sequence():
        seq = "".join(str(random.randint(0, 9)) for _ in range(5))
        return seq, "", ""

    async def show_and_hide(seq):
        html = f"<p style='font-size:30px; color:#ff80ab;'>{seq}</p>"
        yield html
        await asyncio.sleep(2)
        yield "<p style='font-size:24px; color:#666;'>覚えましたか？入力してください！</p>"

    def check_memory_answer(user_input, seq):
        if user_input == seq:
            return "🎉 正解！集中力アップ！"
        else:
            return f"❌ 残念！正解は「{seq}」でした。"

    breathe_phases = [("🌿 吸って…", 4), ("💫 止めて…", 3), ("🌸 吐いて…", 5)]

    async def breathing_session(rounds=3):
        output = ""
        for r in range(rounds):
            output += f"<h3 style='color:#00bfa5;'>🧘‍♀️ ラウンド {r+1} / {rounds}</h3>"
            for text, duration in breathe_phases:
                output += f"<p style='font-size:26px; color:#4CAF50;'>{text}</p>"
                yield output
                await asyncio.sleep(duration)
            output += "<hr>"
        yield "<h2 style='color:#00bcd4;'>🌟 お疲れさまでした！</h2>"

    with gr.Blocks(title="眠気リフレッシュゲーム🎮") as demo:
        if level == 1:
            gr.Markdown("## ⚡ 反射神経ゲーム")
            reaction_display = gr.HTML()
            start_reaction_btn = gr.Button("スタート！")
            click_btn = gr.Button("今クリック！")
            hidden_green_time = gr.Textbox(visible=False)
            hidden_click_time = gr.Textbox(visible=False)
            result_display = gr.HTML()
            start_reaction_btn.click(reaction_game, outputs=[reaction_display, hidden_green_time])
            click_btn.click(record_time, outputs=hidden_click_time).then(
                record_reaction, inputs=[hidden_click_time, hidden_green_time], outputs=result_display
            )
        elif level == 2:
            gr.Markdown("## 🧮 暗算ゲーム")
            question = gr.Textbox(label="問題", interactive=False)
            answer_box = gr.Textbox(label="答えを入力")
            result = gr.Textbox(label="結果", interactive=False)
            correct_answer_state = gr.State()
            new_q_btn = gr.Button("新しい問題")
            check_a_btn = gr.Button("答え合わせ")
            new_q_btn.click(new_math_question, outputs=[question, correct_answer_state, answer_box])
            check_a_btn.click(check_math_answer, inputs=[answer_box, correct_answer_state], outputs=result)
        elif level == 3:
            gr.Markdown("## 🧠 記憶ゲーム")
            seq_display = gr.HTML()
            seq_input = gr.Textbox(label="思い出した数字を入力")
            result3 = gr.Textbox(label="結果", interactive=False)
            seq_state = gr.State()
            show_btn = gr.Button("問題を表示")
            check_btn3 = gr.Button("答え合わせ")
            show_btn.click(generate_sequence, outputs=[seq_state, seq_input, result3]).then(
                show_and_hide, inputs=seq_state, outputs=seq_display
            )
            check_btn3.click(check_memory_answer, inputs=[seq_input, seq_state], outputs=result3)
        elif level == 4:
            gr.Markdown("## 🌿 呼吸ゲーム")
            start_breath = gr.Button("スタート！")
            display4 = gr.HTML("<p>深呼吸の準備をしましょう…</p>")
            start_breath.click(breathing_session, outputs=display4)

    interface = demo.launch(share=False, prevent_thread_lock=True)

    if isinstance(interface, dict):
        return interface.get("local_url") or interface.get("app_url")
    elif hasattr(interface, "local_url"):
        return interface.local_url
    elif isinstance(interface, tuple) and len(interface) >= 2:
        return interface[1]
    return None


# =========================================================
# 🌙 Streamlit 部分
# =========================================================
st.set_page_config(page_title="AI Sleepy Detector", layout="wide")
st.title("😴 AI眠気判定＋ゲーム連動")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

if "stage" not in st.session_state:
    st.session_state.stage = "camera"

if st.session_state.stage == "camera":
    st.markdown("### 👁️ 30秒間の瞬き回数を計測します")
    if st.button("▶ 判定スタート"):
        cap = cv2.VideoCapture(0)
        blink_count = 0
        blink_detected = False
        start_time = time.time()
        frame_placeholder = st.empty()
        info_placeholder = st.empty()

        while time.time() - start_time < 10:
            ret, frame = cap.read()
            if not ret:
                st.error("カメラが見つかりません。")
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    left_eye_top = face_landmarks.landmark[159].y
                    left_eye_bottom = face_landmarks.landmark[145].y
                    diff = abs(left_eye_top - left_eye_bottom)
                    if diff < 0.004:
                        if not blink_detected:
                            blink_count += 1
                            blink_detected = True
                    else:
                        blink_detected = False
            frame_placeholder.image(rgb, channels="RGB")
            info_placeholder.markdown(f"### ⏳ 計測中… 瞬き回数: **{blink_count}回**")
            time.sleep(0.1)
        cap.release()
        st.session_state.blink_count = blink_count
        st.session_state.stage = "result"
        st.rerun()

elif st.session_state.stage == "result":
    blink_count = st.session_state.blink_count
    st.markdown(f"### 💤 判定結果：瞬き {blink_count} 回")

    if blink_count < 10:
        level = 1
        st.success("⚡ 元気いっぱい → 反射神経ゲーム！")
    elif blink_count < 20:
        level = 2
        st.info("🧮 少し眠そう → 暗算ゲーム！")
    elif blink_count < 30:
        level = 3
        st.warning("🧠 かなり眠い → 記憶ゲーム！")
    else:
        level = 4
        st.error("🌿 限界！深呼吸しましょう！")

    if st.button("🎮 ゲーム起動"):
        with st.spinner("ゲームを準備中..."):
            q = queue.Queue()

            def run_game():
                url = launch_gradio_game(level)
                q.put(url)

            threading.Thread(target=run_game).start()

            # 最大5秒待機
            for _ in range(10):
                time.sleep(0.5)
                if not q.empty():
                    st.session_state.game_url = q.get()
                    break

        if "game_url" in st.session_state and st.session_state.game_url:
            st.success(f"✅ ゲーム準備完了！ [ここをクリックして開く]({st.session_state.game_url})")
        else:
            st.error("ゲームURLが取得できませんでした…💦 もう一度試してください。")
