# bishalpaswanbot CORE ON TOP BABY !!!
# AUTO-REGION FINDER INFO API
# FULLY FIXED FOR ALL PLATFORMS
# NO API KEY REQUIRED
# JOIN @bishalpaswanbot FOR MORE LEAKS

import asyncio
import time
import httpx
import json
import random
import threading
import os
import sys
from collections import defaultdict
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from cachetools import TTLCache
from typing import Tuple
from proto import FreeFire_pb2, main_pb2, AccountPersonalShow_pb2
from google.protobuf import json_format, message
from google.protobuf.message import Message
from Crypto.Cipher import AES
import base64
import logging

# ---------- Logging Setup ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Config ----------
MAIN_KEY = base64.b64decode('WWcmdGMlREV1aDYlWmNeOA==')
MAIN_IV = base64.b64decode('Nm95WkRyMjJFM3ljaGpNJQ==')
RELEASEVERSION = "OB54"
USERAGENT = "Dalvik/2.1.0 (Linux; U; Android 13; CPH2095 Build/RKQ1.211119.001)"
SUPPORTED_REGIONS = [
    "IND", "SG", "ID", "BR", "VN", "US", "SAC", "NA",
    "RU", "TH", "TW", "BD", "PK", "ME", "CIS", "EUROPE"
]

# ---------- App Setup ----------
app = Flask(__name__)
CORS(app)
cache = TTLCache(maxsize=200, ttl=600)
uid_region_cache = TTLCache(maxsize=200, ttl=3600)
cached_tokens = defaultdict(dict)

# ---------- Helper Functions ------------
def pad(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([padding_length] * padding_length)

def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(pad(plaintext))

def decode_protobuf(encoded_data: bytes, message_type: message.Message) -> message.Message:
    instance = message_type()
    try:
        instance.ParseFromString(encoded_data)
        return instance
    except Exception as e:
        logger.error(f"Protobuf decode error: {e}")
        return None

async def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()

# ---------- Guest IDS --------------
def get_account_credentials(region: str) -> str:
    r = region.upper()
    
    credentials = {
        "IND": "uid=5294975093&password=MAHI-CODEX_CROWNX64_qrT34PTb",
        "BR": "uid=4712995836&password=MEHEDI_X_AURAMGTNWBCAP",
        "US": "uid=4774366356&password=ADD_HERE",
        "SAC": "uid=4774366356&password=ADD_HERE",
        "NA": "uid=4774366356&password=ADD_HERE",
        "VN": "uid=4737714557&password=ADD_HERE",
        "SG": "uid=4737718961&password=ADD_HERE",
        "ID": "uid=4737720872&password=ADD_HERE",
        "TH": "uid=4774298073&password=ADD_HERE",
        "TW": "uid=4774314170&password=ADD_HERE",
        "BD": "uid=4607333928&password=UDITGAMING_6ADAV",
        "PK": "uid=4774330898&password=ADD_HERE",
        "ME": "uid=4774339389&password=ADD_HERE",
        "RU": "uid=4774345536&password=ADD_HERE",
        "CIS": "uid=4774350397&password=ADD_HERE",
        "EUROPE": "uid=4774375811&password=ADD_HERE"
    }
    
    if r in credentials:
        return credentials[r]
    
    # Fallback to file
    try:
        with open("ucguest.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                raise ValueError("ucguest.txt is empty")
            uid, password = random.choice(lines).split()
            return f"uid={uid}&password={password}"
    except Exception as e:
        logger.error(f"Guest file error: {e}")
        return "uid=4587290647&password=BUNNY_FLASH_SBQ8W"

# -------------- Token Generation --------------
async def get_access_token(account: str, timeout: int = 15):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = f"{account}&response_type=token&client_type=2&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3&client_id=100067"
    headers = {
        'User-Agent': USERAGENT,
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded"
    }
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, data=payload, headers=headers)
            if resp.status_code != 200:
                logger.error(f"Access token failed: {resp.status_code}")
                return "0", "0"
            data = resp.json()
            return data.get("access_token", "0"), data.get("open_id", "0")
    except Exception as e:
        logger.error(f"Access token error: {e}")
        return "0", "0"

async def create_jwt(region: str):
    try:
        account = get_account_credentials(region)
        token_val, open_id = await get_access_token(account)
        
        if token_val == "0" or open_id == "0":
            logger.error(f"Invalid token/open_id for {region}")
            return

        body = json.dumps({
            "open_id": open_id,
            "open_id_type": "4",
            "login_token": token_val,
            "orign_platform_type": "4"
        })

        proto_bytes = await json_to_proto(body, FreeFire_pb2.LoginReq())
        payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)

        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        headers = {
            'User-Agent': USERAGENT,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION
        }

        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, data=payload, headers=headers)

            if resp.status_code != 200 or resp.headers.get("content-type") != "application/octet-stream":
                logger.warning(f"Token request failed for {region}: {resp.status_code}")
                return

            decoded = decode_protobuf(resp.content, FreeFire_pb2.LoginRes)
            if not decoded:
                return
                
            msg = json.loads(json_format.MessageToJson(decoded))

            cached_tokens[region] = {
                'token': f"Bearer {msg.get('token','0')}",
                'region': msg.get('lockRegion','0'),
                'server_url': msg.get('serverUrl','0'),
                'expires_at': time.time() + 25200
            }

            logger.info(f"✅ Token OK [{region}]")
    except Exception as e:
        logger.error(f"Error creating JWT for {region}: {e}")

async def initialize_tokens():
    logger.info("Initializing tokens for all regions...")
    await asyncio.gather(*[create_jwt(r) for r in SUPPORTED_REGIONS])

async def refresh_tokens_periodically():
    while True:
        await asyncio.sleep(25200)
        await initialize_tokens()

async def get_token_info(region: str) -> Tuple[str,str,str]:
    info = cached_tokens.get(region)

    if info and time.time() < info['expires_at']:
        return info['token'], info['region'], info['server_url']

    await create_jwt(region)
    info = cached_tokens[region]
    return info['token'], info['region'], info['server_url']

async def GetAccountInformation(uid, unk, region, endpoint):
    try:
        payload = await json_to_proto(
            json.dumps({'a': uid, 'b': unk}),
            main_pb2.GetPlayerPersonalShow()
        )

        data_enc = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, payload)
        token, lock, server = await get_token_info(region)

        headers = {
            'User-Agent': USERAGENT,
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'Authorization': token,
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION
        }

        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(server + endpoint, data=data_enc, headers=headers)
            
            if resp.status_code != 200:
                logger.error(f"Account info failed: {resp.status_code}")
                return None

            decoded = decode_protobuf(resp.content, AccountPersonalShow_pb2.AccountPersonalShowInfo)
            if not decoded:
                return None
                
            return json.loads(json_format.MessageToJson(decoded))
    except Exception as e:
        logger.error(f"GetAccountInformation error: {e}")
        return None

# -------------- Cache Decorator --------------
def cached_endpoint(ttl=300):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*a, **k):
            key = (request.path, tuple(request.args.items()))
            if key in cache:
                return cache[key]

            res = fn(*a, **k)
            cache[key] = res
            return res

        return wrapper
    return decorator

# -------------- Routes Endpoints --------------
@app.route('/bmw', methods=['GET'])
@cached_endpoint()
def get_account_info():
    """Main endpoint: /bmw?uid=123456789"""
    uid = request.args.get('uid')

    if not uid:
        return jsonify({"error": "Please provide UID. Usage: /bmw?uid=123456789"}), 400

    # Create event loop safely
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Check if UID is cached with region
    if uid in uid_region_cache:
        try:
            data = loop.run_until_complete(
                GetAccountInformation(uid, "7", uid_region_cache[uid], "/GetPlayerPersonalShow")
            )
            if data:
                return jsonify(data)
        except Exception as e:
            logger.error(f"Cached region failed: {e}")

    # Try all regions
    for region in SUPPORTED_REGIONS:
        try:
            data = loop.run_until_complete(
                GetAccountInformation(uid, "7", region, "/GetPlayerPersonalShow")
            )
            
            if data:
                # Save detected region
                uid_region_cache[uid] = region
                return jsonify(data)
        except Exception as e:
            logger.debug(f"Region {region} failed for UID {uid}: {e}")
            continue

    return jsonify({"error": "UID not found or account doesn't exist"}), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "active",
        "regions": len(SUPPORTED_REGIONS),
        "cached_tokens": len(cached_tokens),
        "cache_size": len(cache)
    }), 200

@app.route('/refresh-tokens', methods=['GET', 'POST'])
def refresh_tokens_endpoint():
    """Force refresh tokens"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(initialize_tokens())
        return jsonify({'message': 'Tokens refreshed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "name": "FreeFire Auto-Region Finder API",
        "version": "2.0",
        "endpoints": {
            "/bmw": "Get account info - Usage: /bmw?uid=123456789",
            "/health": "Health check",
            "/refresh-tokens": "Force refresh tokens"
        },
        "status": "running"
    }), 200

# -------------- Error Handlers --------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# -------------- Async Startup --------------
started = False

def start_background_loop():
    global started
    if started:
        return
    started = True

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(initialize_tokens())
        loop.create_task(refresh_tokens_periodically())
        loop.run_forever()
    except Exception as e:
        logger.error(f"Background loop error: {e}")

def run_flask():
    """Run Flask app with proper settings for all platforms"""
    port = int(os.environ.get('PORT', 5000))
    
    # Determine host based on environment
    if os.environ.get('RENDER') or os.environ.get('VERCEL'):
        host = '0.0.0.0'
    else:
        host = '0.0.0.0'  # Works everywhere
    
    # Start background thread for token management
    thread = threading.Thread(target=start_background_loop, daemon=True)
    thread.start()
    
    # Run Flask with appropriate settings
    app.run(host=host, port=port, debug=False, threaded=True)

if __name__ == '__main__':
    # Check if running on Vercel
    if os.environ.get('VERCEL'):
        # Vercel handles the server
        app.config['ENV'] = 'production'
        app.config['DEBUG'] = False
        # Start background thread for Vercel
        threading.Thread(target=start_background_loop, daemon=True).start()
    else:
        # Regular Flask run
        run_flask()