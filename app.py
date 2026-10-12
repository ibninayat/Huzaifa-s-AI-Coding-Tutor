import os, time, json
from pathlib import Path
from datetime import datetime
import requests
import streamlit as st
from streamlit_ace import st_ace
from dotenv import load_dotenv
from groq import Groq

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env", override=True)
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
HISTORY = DATA / "history.json"
JUDGE0_URL = os.getenv("JUDGE0_URL", "https://ce.judge0.com").rstrip("/")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

st.set_page_config(page_title="Huzaifa's AI Coding Tutor", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --cp-bg:#080d19; --cp-panel:#101a2b; --cp-line:#263751; --cp-text:#edf4ff; --cp-muted:#9aabc4; --cp-cyan:#43e0d0; --cp-violet:#a78bfa; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: radial-gradient(ellipse at 12% 0%, rgba(60,91,160,.18), transparent 35%), radial-gradient(ellipse at 90% 5%, rgba(28,177,167,.10), transparent 28%), var(--cp-bg); color:var(--cp-text); }
.block-container { padding-top:1.4rem; padding-bottom:2.5rem; max-width:1600px; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0c1424 0%,#0a1120 100%); border-right:1px solid var(--cp-line); }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 { font-family:'Space Grotesk',sans-serif; }
[data-testid="stHeader"] { background:rgba(8,13,25,.78); }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.035em; }
h1 { font-size:2rem !important; }
[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(20,34,56,.94),rgba(13,23,39,.94)); border:1px solid var(--cp-line); padding:18px 20px; border-radius:16px; box-shadow:0 10px 28px rgba(0,0,0,.13); }
[data-testid="stMetricLabel"] { color:var(--cp-muted); font-weight:600; }
[data-testid="stMetricValue"] { font-family:'Space Grotesk',sans-serif; color:#f5f8ff; }
.stButton>button, .stDownloadButton>button { border-radius:10px; border:1px solid #344864; font-weight:700; min-height:2.65rem; transition:all .18s ease; }
.stButton>button[kind="primary"] { background:linear-gradient(105deg,#7c5cff,#4f8cff); border:0; color:white; box-shadow:0 7px 22px rgba(99,102,241,.22); }
.stButton>button:hover, .stDownloadButton>button:hover { border-color:var(--cp-cyan); transform:translateY(-1px); }
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input { background:#0a1322; border:1px solid #2b3d58; border-radius:10px; color:#edf4ff; }
[data-testid="stSelectbox"] [data-baseweb="select"] > div { background:#101a2b; border-color:#2b3d58; border-radius:10px; }
[data-testid="stExpander"] { background:rgba(16,26,43,.62); border:1px solid var(--cp-line); border-radius:12px; }
[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:#263751; }
.cp-hero { position:relative; overflow:hidden; padding:27px 30px; border-radius:20px; border:1px solid rgba(111,148,205,.32); background:linear-gradient(115deg,rgba(24,37,70,.98),rgba(13,51,72,.95) 58%,rgba(21,41,70,.98)); margin:0 0 1.4rem 0; box-shadow:0 16px 42px rgba(0,0,0,.20); }
.cp-hero:after { content:''; position:absolute; width:240px; height:240px; right:-65px; top:-110px; border-radius:50%; border:1px solid rgba(67,224,208,.22); box-shadow:0 0 0 28px rgba(67,224,208,.035),0 0 0 56px rgba(167,139,250,.025); }
.cp-eyebrow { color:var(--cp-cyan); text-transform:uppercase; letter-spacing:.19em; font-size:.72rem; font-weight:800; margin-bottom:8px; }
.cp-title { color:#fff; font-family:'Space Grotesk',sans-serif; font-size:2rem; font-weight:700; line-height:1.15; letter-spacing:-.04em; margin:0; }
.cp-subtitle { color:#c2d2e9; font-size:.98rem; margin-top:10px; max-width:780px; line-height:1.6; }
.cp-pill { display:inline-block; border:1px solid rgba(67,224,208,.35); color:#bafbf3; background:rgba(67,224,208,.08); padding:5px 10px; border-radius:999px; font-size:.75rem; font-weight:700; margin-top:15px; margin-right:7px; }
[data-testid="stCode"] { border:1px solid #2b3d58; border-radius:12px; }
footer { visibility:hidden; }
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="cp-hero"><div class="cp-eyebrow">✦ Your personal developer workspace</div><p class="cp-title">Huzaifa's AI Coding Tutor <span style="color:#43e0d0">/</span> AI Coding Studio</p><div class="cp-subtitle">Learn smarter. Build confidently. Run code across languages, get AI-powered debugging, and track your progress in one focused workspace.</div><span class="cp-pill">✦ AI-powered learning</span><span class="cp-pill">⌘ Multi-language IDE</span><span class="cp-pill">↗ Progress insights</span></div>""", unsafe_allow_html=True)

LANGUAGES = {
 "C (GCC)":{"id":50,"ext":"c","starter":'#include <stdio.h>\n\nint main(void) {\n    printf("Hello, World!\\n");\n    return 0;\n}',"hint":"Use scanf() for input."},
 "C++ (GCC)":{"id":54,"ext":"cpp","starter":'#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',"hint":"Use cin for input."},
 "Java (OpenJDK)":{"id":62,"ext":"java","starter":'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',"hint":"Use class name Main on this runner."},
 "JavaScript (Node.js)":{"id":63,"ext":"js","starter":'console.log("Hello, World!");',"hint":"Use console.log() for output."},
 "Python 3":{"id":71,"ext":"py","starter":'name = input("Enter your name: ")\nprint(f"Hello, {name}!")',"hint":"Use input() to read text."},
 "C# (Mono)":{"id":51,"ext":"cs","starter":'using System;\nclass Program {\n    static void Main() {\n        Console.WriteLine("Hello, World!");\n    }\n}',"hint":"Use Console.ReadLine() for input."},
 "Go":{"id":60,"ext":"go","starter":'package main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello, World!")\n}',"hint":"Use fmt.Scanln() for simple input."},
 "Rust":{"id":73,"ext":"rs","starter":'fn main() {\n    println!("Hello, World!");\n}',"hint":"Use std::io for input."}
}

def read_history():
    try:
        obj=json.loads(HISTORY.read_text(encoding="utf-8"))
        return obj if isinstance(obj,list) else []
    except (FileNotFoundError,json.JSONDecodeError): return []
def save_history(items): HISTORY.write_text(json.dumps(items[-250:],ensure_ascii=False,indent=2),encoding="utf-8")
def ai_client():
    key=os.getenv("GROQ_API_KEY","").strip()
    return Groq(api_key=key) if key else None
def run_judge0(code, lang_id, user_input, timeout_s):
    headers={"Content-Type":"application/json"}
    token=os.getenv("JUDGE0_AUTH_TOKEN","").strip()
    if token: headers["X-Auth-Token"]=token
    payload={"source_code":code,"language_id":lang_id,"stdin":user_input,"cpu_time_limit":timeout_s,"wall_time_limit":max(timeout_s+2,3),"memory_limit":128000}
    response=requests.post(f"{JUDGE0_URL}/submissions?base64_encoded=false&wait=false",headers=headers,json=payload,timeout=20)
    response.raise_for_status(); data=response.json(); sub_token=data.get("token")
    if not sub_token: return data
    for _ in range(30):
        time.sleep(1)
        poll=requests.get(f"{JUDGE0_URL}/submissions/{sub_token}?base64_encoded=false&fields=stdout,stderr,compile_output,message,status,time,memory",headers=headers,timeout=20)
        poll.raise_for_status(); data=poll.json()
        if data.get("status",{}).get("id") not in (1,2): return data
    return {"status":{"description":"Still processing / timed out waiting"},"message":"Execution service is still processing this run. Try again shortly."}
def ask_ai(mode, language, level, question, code="", execution=None):
    client=ai_client()
    if not client: raise RuntimeError("GROQ_API_KEY is missing. Add it to the .env file beside app.py.")
    guidance={
      "Learn a concept":"Explain from first principles with a small example and common mistakes.",
      "Get a hint":"Give a useful hint first; do not immediately reveal the full solution.",
      "Explain code":"Explain the supplied code step by step for a beginner.",
      "Debug code":"Identify likely syntax, runtime, and logic errors; explain and suggest corrected code.",
      "Generate practice":"Create three exercises with hints and expected outcomes. Put solutions in a separate section.",
      "Review my solution":"Review correctness, readability, edge cases, and style. Do not claim execution unless execution data is supplied.",
      "Improve code":"Suggest clear improvements and provide an improved version, explaining the changes."
    }
    prompt=f"Mode: {mode}\nLanguage: {language}\nStudent level: {level}\nQuestion: {question or '(not provided)'}\nCode:\n```{LANGUAGES.get(language,{}).get('ext','text')}\n{code}\n```\nExecution result (if any): {json.dumps(execution,ensure_ascii=False)[:3500]}\nInstructions: {guidance.get(mode,'Answer helpfully and accurately for a student.')}"
    res=client.chat.completions.create(model=MODEL,temperature=.25,messages=[{"role":"system","content":"You are AI Coding Tutor Pro, a supportive programming instructor for university beginners. Be accurate, structured, beginner-friendly. Never claim code has run unless execution results are provided. Never ask for secrets."},{"role":"user","content":prompt}])
    return res.choices[0].message.content or "No response returned."

if "sources" not in st.session_state: st.session_state.sources={k:v["starter"] for k,v in LANGUAGES.items()}
if "project_files" not in st.session_state:
    st.session_state.project_files = {"main.cpp": LANGUAGES["C++ (GCC)"]["starter"]}
if "active_file" not in st.session_state: st.session_state.active_file = "main.cpp"
if "run_result" not in st.session_state: st.session_state.run_result=None
if "ai_answer" not in st.session_state: st.session_state.ai_answer=""
with st.sidebar:
    st.markdown("### 🚀 Huzaifa's AI Coding Tutor")
    st.caption("PRO DEVELOPER WORKSPACE")
    st.divider()
    page=st.radio("Navigation",["Dashboard","Online IDE","AI Tutor","My Progress","About"])
    st.divider()
    level=st.selectbox("Learning level",["Beginner","BSCS Semester 1–2","Intermediate","Advanced"],index=1)
    st.caption("AI features require a valid Groq API key in .env. Code runs through the configured Judge0 service.")
    if os.getenv("GROQ_API_KEY","").strip(): st.success("Groq key found")
    else: st.warning("Add GROQ_API_KEY to .env")
history=read_history()

if page=="Dashboard":
    st.title("Your workspace, at a glance")
    st.caption("A focused place to learn, experiment, debug, and grow as a developer.")
    a,b,c=st.columns(3); a.metric("Saved activities",len(history)); b.metric("Languages used",len({x.get('language') for x in history if x.get('language')})); c.metric("Code runs",sum(x.get('type')=='execution' for x in history))
    left,right=st.columns(2)
    with left:
        st.subheader("Quick start")
        st.markdown("1. Open **Online IDE** to write and run C, C++, Java, Python, JavaScript, C#, Go, or Rust.\n2. Use **AI Tutor** for explanations, hints, debugging, practice, and code review.\n3. Visit **My Progress** to see and export your activity history.")
    with right:
        st.subheader("Recent activity")
        if history:
            for item in reversed(history[-5:]): st.write(f"**{item.get('time','')}** · {item.get('language','')} · {item.get('mode',item.get('status','Activity'))}")
        else: st.info("Your activity will appear here after your first session.")
    st.info("Review AI-generated code before using it. Never paste passwords, API keys, or private data into the tutor.")

elif page=="Online IDE":
    st.title("⌘ Online IDE")
    st.caption("Write, compile, execute, and inspect your code — all from one workspace.")
    language=st.selectbox("Programming language",list(LANGUAGES),index=1,key="ide_language")
    if st.session_state.get("last_ide_language") != language:
        starter_name = "Main.java" if language.startswith("Java") else f"main.{LANGUAGES[language]['ext']}"
        st.session_state.project_files.setdefault(starter_name, LANGUAGES[language]["starter"])
        st.session_state.active_file = starter_name
        st.session_state.last_ide_language = language
    st.caption(LANGUAGES[language]["hint"])
    # Lightweight project explorer: each file is editable and downloadable; the selected file is the run target.
    file_col, editor_col = st.columns([.30, .70], gap="large")
    with file_col:
        st.subheader("📁 Project files")
        current_files = list(st.session_state.project_files.keys())
        active = st.selectbox("Open file", current_files, index=current_files.index(st.session_state.active_file) if st.session_state.active_file in current_files else 0, key="active_file_picker")
        st.session_state.active_file = active
        new_name = st.text_input("New file name", placeholder="example.py", key="new_file_name")
        if st.button("＋ Create file", use_container_width=True):
            clean_name = Path(new_name.strip()).name
            if not clean_name or "." not in clean_name:
                st.warning("Enter a file name with an extension, e.g. notes.py")
            elif clean_name in st.session_state.project_files:
                st.warning("That file already exists.")
            else:
                st.session_state.project_files[clean_name] = ""
                st.session_state.active_file = clean_name
                st.rerun()
        st.caption("The active file is the one sent to the code runner. Additional files are kept in this workspace.")
        if st.button("🗑 Remove active file", use_container_width=True, disabled=len(current_files) <= 1):
            st.session_state.project_files.pop(st.session_state.active_file, None)
            st.session_state.active_file = next(iter(st.session_state.project_files))
            st.rerun()
        st.download_button("⬇ Download active file", st.session_state.project_files.get(active, ""), file_name=active, use_container_width=True)
    with editor_col:
        ext = Path(active).suffix.lower().lstrip(".")
        ace_modes = {"py":"python", "c":"c_cpp", "h":"c_cpp", "cpp":"c_cpp", "cc":"c_cpp", "java":"java", "js":"javascript", "ts":"typescript", "cs":"csharp", "go":"golang", "rs":"rust", "html":"html", "css":"css", "json":"json", "md":"markdown", "txt":"text"}
        ace_mode = ace_modes.get(ext, LANGUAGES[language]["ext"])
        st.subheader(f"⌘ Editor · {active}")
        st.caption("Syntax highlighting · auto-indent · keyboard shortcuts · dark editor theme")
        default_code = st.session_state.project_files.get(active, st.session_state.sources.get(language, LANGUAGES[language]["starter"]))
        code = st_ace(value=default_code, language=ace_mode, theme="tomorrow_night", key=f"ace_{active}", height=420, tab_size=4, show_gutter=True, show_print_margin=False, wrap=True, auto_update=True, min_lines=14, font_size=14)
        if code is None: code = default_code
        st.session_state.project_files[active] = code
        st.session_state.sources[language] = code
    user_input = st.text_area("⌨ Program input (stdin)", height=80, placeholder="Enter input your program reads, such as a name or numbers.")
    timeout = st.slider("Execution time limit (seconds)", 1, 10, 5)
    run, explain, debug, improve = st.columns(4)
    run_clicked = run.button("▶ Run code", type="primary", use_container_width=True)
    explain_clicked = explain.button("✦ Explain", use_container_width=True)
    debug_clicked = debug.button("⚒ Debug", use_container_width=True)
    improve_clicked = improve.button("↗ Improve", use_container_width=True)
    st.markdown("---")
    st.subheader("🖥 Output Console")
    result = st.session_state.run_result
    if result:
        status = result.get("status", {}).get("description", "Unknown status")
        if status == "Accepted": st.success(f"{status} · {result.get('time','?')} s · {result.get('memory','?')} KB")
        elif "Error" in status or "Exceeded" in status or "Compilation" in status: st.error(status)
        else: st.info(status)
        for label, key in [("Program output", "stdout"), ("Compilation output", "compile_output"), ("Error / stderr", "stderr"), ("Message", "message")]:
            if result.get(key):
                st.markdown(f"**{label}**")
                st.code(result[key], language="text")
        if not any(result.get(k) for k in ("stdout", "compile_output", "stderr", "message")): st.caption("No text output returned.")
    else: st.info("Your program output and errors will appear here after you run the code.")
    st.caption("Code execution is provided by the configured Judge0 service. Do not run sensitive or confidential code through a public endpoint.")
    if run_clicked:
        if not code.strip(): st.warning("Enter some code first.")
        else:
            try:
                with st.spinner(f"Compiling and running {language}..."): result=run_judge0(code,LANGUAGES[language]["id"],user_input,timeout)
                st.session_state.run_result=result
                history.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"type":"execution","mode":"Run Code","language":language,"level":level,"question":"Code execution","code":code[:6000],"status":result.get("status",{}).get("description","Unknown"),"answer":result.get("stdout") or result.get("compile_output") or result.get("stderr") or result.get("message") or "No output"})
                save_history(history); st.rerun()
            except requests.HTTPError as e:
                st.error(f"Judge0 returned HTTP error: {e}")
                if e.response is not None: st.code(e.response.text[:1200])
            except requests.RequestException as e: st.error(f"Could not reach the execution service: {e}")
    if explain_clicked or debug_clicked or improve_clicked:
        mode="Explain code" if explain_clicked else "Debug code" if debug_clicked else "Improve code"
        try:
            with st.spinner("AI tutor is analyzing your code..."): answer=ask_ai(mode,language,level,"Please help with the code in the editor.",code,st.session_state.run_result)
            st.session_state.ai_answer=answer
            history.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"type":"tutor","mode":mode,"language":language,"level":level,"question":"Please help with the code in the editor.","code":code[:6000],"answer":answer})
            save_history(history)
        except Exception as e: st.error(f"AI request failed: {type(e).__name__}: {e}")
    if st.session_state.ai_answer:
        st.markdown("---\n### 🧑‍🏫 AI result")
        st.markdown(st.session_state.ai_answer)
        st.download_button("Download AI response",st.session_state.ai_answer,"ai_response.md","text/markdown")

elif page=="AI Tutor":
    st.title("✦ AI Learning Studio")
    st.caption("Get explanations that match your level, hints that help you think, and debugging support when you get stuck.")
    st.write("Learn concepts, get hints, explain code, debug, review solutions, and generate practice exercises.")
    mode=st.selectbox("Tutor mode",["Learn a concept","Get a hint","Explain code","Debug code","Generate practice","Review my solution","Improve code"])
    language=st.selectbox("Language / subject",list(LANGUAGES),index=1,key="tutor_language")
    question=st.text_area("Your question or task",height=100,placeholder="Example: Explain variables in C++ for a BSCS second-semester student.")
    code=st.text_area("Code (optional)",height=190,placeholder="Paste your code here for explanation, debugging, or review.")
    if st.button("Ask AI Tutor",type="primary"):
        if not question.strip() and not code.strip(): st.warning("Enter a question or paste code first.")
        else:
            try:
                with st.spinner("Thinking..."): answer=ask_ai(mode,language,level,question,code)
                st.session_state.ai_answer=answer
                history.append({"time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"type":"tutor","mode":mode,"language":language,"level":level,"question":question,"code":code[:6000],"answer":answer})
                save_history(history)
            except Exception as e: st.error(f"AI request failed: {type(e).__name__}: {e}")
    if st.session_state.ai_answer:
        st.subheader("Tutor response"); st.markdown(st.session_state.ai_answer)
        st.download_button("Export answer",st.session_state.ai_answer,"tutor_answer.md","text/markdown")

elif page=="My Progress":
    st.title("↗ Learning analytics")
    st.caption("Review your activity, revisit past solutions, and keep your learning momentum going.")
    a,b=st.columns(2); a.metric("Saved activities",len(history)); b.metric("Tutor sessions",sum(x.get('type')=='tutor' for x in history))
    if history:
        counts={}
        for item in history: counts[item.get("language","Other")]=counts.get(item.get("language","Other"),0)+1
        st.subheader("Activities by language"); st.bar_chart(counts)
        st.subheader("History")
        for i,item in enumerate(reversed(history),1):
            with st.expander(f"{i}. {item.get('time','')} — {item.get('mode','Activity')} ({item.get('language','')})"):
                st.write(item.get("question",""))
                if item.get("code"): st.code(item["code"],language=item.get("language","text").lower())
                if item.get("status"): st.caption("Execution status: "+item["status"])
                st.markdown(str(item.get("answer","")))
        st.download_button("Export history (JSON)",json.dumps(history,ensure_ascii=False,indent=2),"ai_coding_tutor_history.json","application/json")
        if st.button("Clear history"):
            save_history([]); st.success("History cleared. Refresh the page to update metrics.")
    else: st.info("No activity yet. Use the Online IDE or AI Tutor first.")

else:
    st.title("About Huzaifa's AI Coding Tutor")
    st.markdown("""**Included:** multi-language code editor, Judge0 compile/run integration, stdin input, output and compilation errors, Groq-powered AI explanations/debugging, practice modes, and local history/progress.\n\n**Execution:** code is sent to the configured Judge0 service. Availability, supported language versions, limits, and privacy terms depend on that service. The default public endpoint may be rate-limited or unavailable; for production, use an authenticated managed plan or self-hosted Judge0.\n\n**Security:** never execute untrusted code directly on your own machine. Do not place API keys in source code or share `.env`.""")
    checks=["I understand the problem.","I chose suitable variables and data types.","I tested normal input.","I considered edge cases.","I can explain my code.","I reviewed the output and errors."]
    done=[st.checkbox(item,key=f"self_check_{i}") for i,item in enumerate(checks)]
    score=sum(done); st.progress(score/len(checks)); st.write(f"Self-evaluation: **{score}/{len(checks)}**")

st.caption("Educational project. AI can make mistakes. Do not submit passwords, API keys, or private data.")
