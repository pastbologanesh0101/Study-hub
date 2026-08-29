"""
Lightweight extractive summarizer + quiz-question generator.

Deliberately dependency-free (no external LLM API key required) so the
project works instantly for anyone who clones the repo. Uses word-frequency
scoring to rank sentences, a classic and well-understood NLP technique.

Stretch goal (mentioned in README): swap this out for a real LLM API call
(OpenAI/Anthropic/etc.) for higher-quality summaries once you're comfortable
wiring up external APIs.
"""
import re
from collections import Counter

STOPWORDS = set("""
a an the is are was were be been being to of and or in on at for with
as by from that this these those it its it's i you he she we they them
his her their our your not no do does did doing have has had having
but if then so than too very can will would should could may might
""".split())


def _sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]


def _words(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())


def summarize(text: str, max_sentences: int = 4) -> str:
    sentences = _sentences(text)
    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    word_freq = Counter(w for w in _words(text) if w not in STOPWORDS)
    if not word_freq:
        return " ".join(sentences[:max_sentences])

    max_freq = max(word_freq.values())
    for w in word_freq:
        word_freq[w] /= max_freq

    scores = []
    for i, sent in enumerate(sentences):
        words = _words(sent)
        if not words:
            continue
        score = sum(word_freq.get(w, 0) for w in words) / len(words)
        # slight boost for earlier sentences (topic sentences tend to matter more)
        score *= 1.0 + (0.1 if i < 2 else 0)
        scores.append((score, i, sent))

    top = sorted(scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    top_in_order = [s for _, _, s in sorted(top, key=lambda x: x[1])]
    return " ".join(top_in_order)


def generate_quiz(text: str, num_questions: int = 3) -> list[str]:
    """
    Generates simple fill-in-the-blank style review questions by blanking
    out a key noun-like word from a few information-dense sentences.
    Basic but genuinely useful for quick self-testing, and a good example
    of rule-based NLP for a first project.
    """
    sentences = _sentences(text)
    word_freq = Counter(w for w in _words(text) if w not in STOPWORDS and len(w) > 3)

    questions = []
    for sent in sentences:
        words = _words(sent)
        candidates = [w for w in words if w in word_freq]
        if not candidates:
            continue
        key_word = max(candidates, key=lambda w: word_freq[w])
        pattern = re.compile(re.escape(key_word), re.IGNORECASE)
        blanked = pattern.sub("_____", sent, count=1)
        if blanked != sent:
            questions.append(blanked)
        if len(questions) >= num_questions:
            break

    return questions
