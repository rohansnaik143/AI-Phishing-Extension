import re
from urllib.parse import urlparse
import math
from collections import Counter

TRUSTED_DOMAINS = [
    "amazon.com",
    "google.com",
    "microsoft.com",
    "apple.com",
    "facebook.com",
    "aws.amazon.com"
]

def calculate_entropy(s):
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    features = []

    # 1. Very long URL flag (instead of raw length)
    features.append(1 if len(url) > 75 else 0)

    # 2. Has IP address
    features.append(1 if re.match(r"\d+\.\d+\.\d+\.\d+", domain) else 0)

    # 3. Subdomain count
    features.append(domain.count(".") - 1)

    # 4. Suspicious words
    suspicious_words = ["login", "secure", "verify", "account", "update", "bank"]
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    # 5. HTTPS
    features.append(1 if parsed.scheme == "https" else 0)

    # 6. URL entropy
    features.append(calculate_entropy(domain))

    # 7. Trusted domain flag
    features.append(1 if any(trusted in domain for trusted in TRUSTED_DOMAINS) else 0)

    return features