st.markdown(
"""
   <style>
    /* Hide entire top header bar (Share, Fork, Manage App, Help, About) */
    /* Hide header, menu, footer */
   header {display: none !important;}
    /* Hide the main menu (hamburger icon) */
   #MainMenu {visibility: hidden;}
    /* Hide the footer (including "Hosted by Streamlit") */
   footer {visibility: hidden;}
    /* Hide help sidebar if present */
   div[data-testid="stHelpSidebar"] {display: none;}

    /* Responsive styles for mobile devices */
    @media (max-width: 768px) {
        /* Make header image smaller and centered */
        img.header-img {
            width: 70% !important;
        }
        /* Make main header text larger for readability */
        h1, h2, h3, h4, h5, h6 {
            font-size: calc(1.2em + 1vw) !important;
        }
        /* Stack columns vertically instead of side by side */
        .block-container {
            flex-direction: column !important;
        }
        /* Make buttons and inputs full width */
        button, input[type=text], input[type=password], textarea, input[type=number] {
            width: 100% !important;
            font-size: 1.2em;
            padding: 12px;
        }
        /* Adjust margins/padding for better mobile fit */
        .css-1d391kg {
            padding: 10px !important;
        }
        /* Make images scale down */
        img {
            max-width: 80% !important;
            height: auto !important;
        }
    }
   </style>
    """,
    unsafe_allow_html=True
    """, unsafe_allow_html=True
)

# --- Embed your new header image as a smaller header ---
# --- Embed your header image ---
header_image_url = "https://i.imgur.com/WhRBcgw.png"

# --- Apply background CSS ---
@@ -48,13 +75,21 @@
       background-color: rgba(0,0,0,0.3);
       z-index: -1;
   }}
    /* Make images with class 'header-img' responsive */
    img.header-img {
        width: 50%;
        max-width: 350px;
        height: auto;
        display: block;
        margin: 10px auto;
    }
   </style>
   """, unsafe_allow_html=True
)

# --- Show your smaller "XBOX TOOL" header (words only) ---
st.markdown(
    f'<img src="{header_image_url}" style="width: 50%; max-width: 350px; height: auto; display: block; margin: 10px auto;">',
    f'<img src="{header_image_url}" class="header-img" alt="XBOX TOOL">',
unsafe_allow_html=True
)

@@ -65,6 +100,7 @@
else:
users = {}

# --- Session state for login ---
if 'logged_in' not in st.session_state:
st.session_state['logged_in'] = False
if 'user' not in st.session_state:
@@ -130,7 +166,7 @@ def login():
q, a = generate_captcha()
st.session_state['captcha_q'], st.session_state['captcha_a'] = q, a

# Async functions for simulating API calls
# Async functions (simulate API)
async def convert_gamertag_to_xuid(gamertag):
await asyncio.sleep(1)
return "1234567890"
