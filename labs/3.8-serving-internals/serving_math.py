"""Lab 3.8: the two pieces of serving arithmetic worth knowing by heart.

Part 1: KV cache size. Per token = 2 (K and V) x layers x KV heads x head dim x bytes.
Part 2: speculative decoding. With acceptance rate a, draft length g, and draft cost c (relative to one
target pass), expected tokens per target pass = (1 - a^(g+1)) / (1 - a)   (Leviathan et al., 2023),
and speed-up = that / (g*c + 1).
Standard library only. Model shapes are illustrative, loosely based on public 8B and 70B designs.
"""

def kv_bytes_per_token(layers, kv_heads, head_dim, bytes_):
    return 2 * layers * kv_heads * head_dim * bytes_

shapes = [
    ("8B, full multi-head attention (32 KV heads)", 32, 32, 128),
    ("8B, grouped-query attention (8 KV heads)",    32, 8, 128),
    ("70B, grouped-query attention (8 KV heads)",   80, 8, 128),
]
print("| Model shape | Cache bytes | Per token | 8k-token request | 128k-token request |")
print("|---|---|---|---|---|")
for name, L, H, D in shapes:
    for b, label in ((2, "16-bit"), (1, "8-bit")):
        per = kv_bytes_per_token(L, H, D, b)
        print(f"| {name} | {label} | {per/1024:.0f} KB | {per*8192/1e9:.2f} GB | {per*131072/1e9:.1f} GB |")

print("\n| Acceptance rate | Draft length | Tokens per target pass | Speed-up (draft cost 5%) | Speed-up (draft cost 20%) |")
print("|---|---|---|---|---|")
for a in (0.3, 0.5, 0.7, 0.85):
    for g in (3, 6):
        e = (1 - a ** (g + 1)) / (1 - a)
        print(f"| {a:.0%} | {g} | {e:.2f} | {e/(g*0.05+1):.2f}x | {e/(g*0.20+1):.2f}x |")
