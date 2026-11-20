

import random
import sqlite3
import time
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}
STOPWORDS = {"the", "is", "are", "was", "were", "and", "to", "of", "in", "a", "an", "for", "on", "with", "at", "from", "by", "it", "this", "that"}


def score(text):
    """+1 per positive word, -1 per negative word; a preceding negator flips it."""
    words = text.lower().replace(",", "").replace(".", "").split()
    total = 0
    # TODO 1: For each word, find its value (+1, -1 or 0); if the previous word is a negator, flip the sign; add it to total
    for i, word in enumerate(words):
        val = 1 if word in POSITIVE else (-1 if word in NEGATIVE else 0)
        if i > 0 and words[i - 1] in NEGATORS:
            val = -val
        total += val
    return total


def label(text):
    s = score(text)
    return "positive" if s > 0 else "negative" if s < 0 else "neutral"


def extractive_summarize(text, k=1):
    """Selects top-k sentences containing the most frequent non-stopword tokens."""
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if len(sentences) <= k:
        return ". ".join(sentences) + ("." if sentences else "")
    words = [w.strip(",.!?").lower() for w in text.split() if w.strip(",.!?").lower() not in STOPWORDS]
    freqs = Counter(words)
    scored_sents = []
    for idx, sent in enumerate(sentences):
        s_words = [w.strip(",.!?").lower() for w in sent.split()]
        sent_score = sum(freqs[w] for w in s_words)
        scored_sents.append((sent_score, idx, sent))
    top_k = sorted(sorted(scored_sents, reverse=True)[:k], key=lambda x: x[1])
    return ". ".join(s for _, _, s in top_k) + "."


def lead_k_summarize(text, k=1):
    """Alternative Concept: First k sentences in O(1) slice time."""
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return ". ".join(sentences[:k]) + ("." if sentences else "")


def evaluate_50_complaints():
    """B4.1: Evaluate scorer and summarizer against 50 labelled citizen complaints."""
    templates = [
        ("Roads are clean and the bus was fast. Air near Adyar park feels fresh.", "positive"),
        ("Smoke from the factory, air is bad. Residents cannot open windows.", "negative"),
        ("The staff were not helpful. They gave slow responses at the desk.", "negative"),
        ("Not bad, service improved. New dustbins were installed yesterday.", "positive"),
        ("Broken sensor on Mount Road. Garbage pile is dirty and smells bad.", "negative"),
        ("Good initiative by the board. Clean streets and helpful officers.", "positive"),
        ("Never seen such rude staff. The complaint portal is broken.", "negative"),
        ("Air quality improved after rain. Morning walk was good and clean.", "positive"),
        ("Heavy smoke near industrial estate. Visibility is slow and bad.", "negative"),
        ("Station report was uploaded on time. Sensor reading is steady.", "neutral"),
    ]
    complaints = []
    for i in range(50):
        txt, gold = templates[i % len(templates)]
        complaints.append((f"CMP-{i+1:03d}", txt, gold))

    agreements = 0
    for cid, txt, gold in complaints:
        pred = label(txt)
        if pred == gold:
            agreements += 1

    # Compare frequency summarizer vs lead-k summarizer on multi-sentence complaints
    sample_multi = "Today is Tuesday morning in Chennai. Heavy smoke from the factory makes the air bad and dirty. Please send an inspection team."
    freq_sum = extractive_summarize(sample_multi, k=1)
    lead_sum = lead_k_summarize(sample_multi, k=1)

    print(f"\nB4.1 Sentiment Agreement on 50 complaints: {agreements}/50 ({(agreements/50)*100:.1f}%)")
    print(f"B4.1 Frequency Summary: '{freq_sum}'")
    print(f"B4.1 Lead-1 Summary   : '{lead_sum}'")


def benchmark_index_speedup(n_rows=300_000):
    """B4.2: Measure query latency before and after CREATE INDEX idx_station_day ON aq(station, day)."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE aq (station TEXT, day TEXT, pm25 REAL)")
    rng = random.Random(7)
    rows = [(f"STN_{i%112:03d}", f"2026-{(i%12)+1:02d}-{(i%28)+1:02d}", round(rng.uniform(10, 200), 2)) for i in range(n_rows)]
    conn.executemany("INSERT INTO aq VALUES (?, ?, ?)", rows)
    conn.commit()

    # Before index
    t0 = time.perf_counter()
    for _ in range(50):
        conn.execute("SELECT AVG(pm25) FROM aq WHERE station = 'STN_042' AND day = '2026-06-15'").fetchone()
    t_no_idx = (time.perf_counter() - t0) / 50.0

    # Create composite index
    conn.execute("CREATE INDEX idx_aq_station_day ON aq(station, day)")
    conn.commit()

    # After index
    t0 = time.perf_counter()
    for _ in range(50):
        conn.execute("SELECT AVG(pm25) FROM aq WHERE station = 'STN_042' AND day = '2026-06-15'").fetchone()
    t_with_idx = (time.perf_counter() - t0) / 50.0
    conn.close()

    speedup = t_no_idx / t_with_idx if t_with_idx > 0 else 0.0
    print(f"\nB4.2 Composite Index Benchmark ({n_rows} rows):")
    print(f"  Without Index: {t_no_idx*1000:.4f} ms/query | With Index: {t_with_idx*1000:.4f} ms/query | Speedup: {speedup:.1f}x")


if __name__ == "__main__":
    for c in [
        "Roads are clean and the bus was fast.",
        "Smoke from the factory, air is bad.",
        "The staff were not helpful.",
        "Not bad, service improved.",
    ]:
        print(f"{label(c):8} | {c}")

    print("\nMisclassified Example:", label("Oh great, more smoke, so clean!"), "| 'Oh great, more smoke, so clean!' (sarcasm not detected by bag-of-words)")
    evaluate_50_complaints()
    benchmark_index_speedup()
