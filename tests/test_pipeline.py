import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.generator import generate_answer

# ── TEST CASES ────────────────────────────────────────────
# Format: (question, expected_keyword)
TEST_CASES = [
    (
        "What is the maximum limit for third party liability?",
        "40,000"
    ),
    (
        "What perils are covered under Section 1?",
        "Fire"
    ),
    (
        "What is the money limit if not stored in a safe?",
        "5,000"
    ),
    (
        "How many months is rent covered after a loss?",
        "Six"
    ),
    (
        "What is the maximum limit for family personal accident?",
        "30,000"
    ),
]

# ── EVALUATION ────────────────────────────────────────────
def evaluate():
    print("=" * 60)
    print("RAG PIPELINE EVALUATION")
    print("=" * 60)

    passed = 0
    failed = 0
    results = []

    for question, expected_keyword in TEST_CASES:
        result = generate_answer(question)
        answer = result["answer"]
        success = expected_keyword.lower() in answer.lower()

        status = "✅ PASS" if success else "❌ FAIL"
        if success:
            passed += 1
        else:
            failed += 1

        results.append({
            "question": question,
            "expected": expected_keyword,
            "answer": answer[:100],
            "status": status
        })

        print(f"\n{status}")
        print(f"Q: {question}")
        print(f"Expected keyword: '{expected_keyword}'")
        print(f"Answer: {answer[:120]}...")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{len(TEST_CASES)} passed")
    print(f"Accuracy: {round(passed/len(TEST_CASES)*100, 1)}%")
    print("=" * 60)

    return passed, failed


if __name__ == "__main__":
    evaluate()