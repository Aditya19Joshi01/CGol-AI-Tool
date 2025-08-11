import random
from .cgol_logic import run_game_of_life

def handle_prompt(prompt: str) -> str:
    prompt_lower = prompt.lower().strip()

    # Case 1: Specific word generation count
    if "how many generations" in prompt_lower and "word" in prompt_lower:
        import re
        match = re.search(r"word\s+'([^']+)'", prompt_lower)
        if not match:
            match = re.search(r"word\s+(\w+)", prompt_lower)
        if match:
            word = match.group(1)
            generations, score = run_game_of_life(word)
            return (f"The word '{word}' reached stability in {generations} generations "
                    f"with a score of {score}.")
        else:
            return "I couldn't find the word in your prompt."

    # Case 2: Random words, highest score
    if "generate 3 random words" in prompt_lower and "highest" in prompt_lower:
        words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot",
                 "golf", "hotel", "india", "juliet", "kilo", "lima",
                 "mike", "november", "oscar", "papa", "quebec", "romeo",
                 "sierra", "tango", "uniform", "victor", "whiskey", "xray",
                 "yankee", "zulu"]
        random_words = random.sample(words, 3)
        results = []
        for w in random_words:
            generations, score = run_game_of_life(w)
            results.append({"word": w, "generations": generations, "score": score})

        highest = max(results, key=lambda x: x["score"])
        return (f"Generated words: {', '.join(random_words)}.\n"
                f"Highest score: '{highest['word']}' "
                f"with {highest['score']} points in {highest['generations']} generations.")

    return "Sorry, I don't understand that prompt."
