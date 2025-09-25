import io, string, random
from PIL import Image
import requests

LETTERS = list(string.ascii_lowercase)
ALPHA_NUMER_STRINGS = {c: str(i+1) for i, c in enumerate(LETTERS)}

def calculate_anchor(year: int) -> int:
    r = year % 400
    if r < 100:   return 2
    if r < 200:   return 0
    if r < 300:   return 5
    return 3

def doomsday(year: int) -> int:
    anchor = calculate_anchor(year)
    y = year % 100
    a, b, c = y // 12, y % 12, (y % 12) // 4
    return ((a + b + c) % 7 + anchor) % 7

def mod7_mod10(num: int | str) -> int:
    s = str(num)
    total, power = 0, 0
    for ch in reversed(s):
        total += int(ch) * (7 ** power)
        power += 1
    return total

def text_to_number_first(text: str) -> str:
    return "".join(ALPHA_NUMER_STRINGS[ch.lower()] for ch in text if ch.isalpha())

def image_to_number_first(im: Image.Image) -> str:
    width, height = im.size
    mid = height // 2
    out = []
    for x in range(width):
        r, g, b = im.getpixel((x, mid))[:3]
        out.append(str(r + g + b))
    return "".join(out)

def number_to_years(number_string: str, n: int) -> list[str]:
    chunks = []
    for i in range(0, len(number_string), n):
        part = number_string[i:i+n]
        if len(part) == n:
            chunks.append(part)
    return chunks

def years_list_to_doomsdays(years_list: list[str]) -> list[int]:
    return [doomsday(int(y)) for y in years_list if y.isdigit()]

def ddays_modded_joined(ddays_list: list[int]) -> str:
    joined = "".join(str(d) for d in ddays_list)
    triples = number_to_years(joined, 3)
    mod10_list = [mod7_mod10(t) for t in triples]
    return "".join(str(m) for m in mod10_list)

def number_str_to_ascii(number_string: str) -> list[int]:
    doubles = [int(number_string[i:i+2]) for i in range(0, len(number_string), 2)
               if len(number_string[i:i+2]) == 2]
    doubles = [n for n in doubles if n <= 93]           # filter, don’t mutate-while-iterating
    return [n + 33 for n in doubles]                    # map to printable ASCII (33..126)

def ascii_codes_to_password(ascii_codes: list[int]) -> str:
    return "".join(chr(code) for code in ascii_codes)

def decode(input_val, complexity: int) -> str:
    first = text_to_number_first(input_val) if isinstance(input_val, str) else image_to_number_first(input_val)
    years = number_to_years(first, complexity)
    if not years:
        return ""
    ddays = years_list_to_doomsdays(years)
    modded = ddays_modded_joined(ddays)
    ascii_codes = number_str_to_ascii(modded)
    return ascii_codes_to_password(ascii_codes)

def decode_url(url: str, complexity: int) -> str:
    # Safe-ish fetch: timeout + simple size guard
    with requests.get(url, timeout=8, stream=True) as r:
        r.raise_for_status()
        content = io.BytesIO()
        max_bytes = 5 * 1024 * 1024  # 5MB
        for chunk in r.iter_content(8192):
            content.write(chunk)
            if content.tell() > max_bytes:
                raise ValueError("Image too large")
        content.seek(0)
    img = Image.open(content).convert("RGB")
    return decode(img, complexity)
